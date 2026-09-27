"""Expression conversions — infix / postfix / prefix, all with one stack.

Two different stack jobs cover all six conversions:

* Infix → postfix (and → prefix) stack the *operators*. Operands go straight
  to the output; an operator first pops every stacked operator that binds at
  least as tightly (^ is right-associative, so it only pops strictly tighter
  ones), and ')' pops back to its '('. Infix → prefix is the same scan run
  right-to-left with the parentheses' roles swapped and the tie rule flipped,
  then the output read backwards.
* Postfix / prefix → anything stack the *operands*: each operator pops its two
  sub-expressions and pushes the combined one. Postfix scans left-to-right
  (second pop is the left operand); prefix scans right-to-left (first pop is
  the left operand).

Reuses the `stack` view: the input row with the scan cursor, the stack along
the bottom (boxes now size to their text), and the optional `output` row and
`rtl` scan-direction flag.
"""

MAX_LEN = 15
OPERATORS = set("+-*/^")
PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

MODES = {
    "infix_to_postfix": ("infix", "postfix"),
    "infix_to_prefix": ("infix", "prefix"),
    "postfix_to_infix": ("postfix", "infix"),
    "postfix_to_prefix": ("postfix", "prefix"),
    "prefix_to_infix": ("prefix", "infix"),
    "prefix_to_postfix": ("prefix", "postfix"),
}


def is_operand(ch: str) -> bool:
    return ch.isalnum()


def validate(text: str, kind: str) -> str | None:
    """None when `text` is a well-formed `kind` expression, else a reason."""
    if not text:
        return "Type an expression."
    if len(text) > MAX_LEN:
        return f"Max {MAX_LEN} characters."
    allowed = OPERATORS | (set("()") if kind == "infix" else set())
    if any(not (is_operand(c) or c in allowed) for c in text):
        extra = " and ( )" if kind == "infix" else ""
        return (f"Use single letters/digits as operands, operators "
                f"+ - * / ^{extra} only.")
    if kind == "infix":
        depth, expect_operand = 0, True
        for c in text:
            if c == "(":
                if not expect_operand:
                    return "A '(' can't directly follow an operand."
                depth += 1
            elif c == ")":
                if expect_operand:
                    return "Something is missing before a ')'."
                depth -= 1
                if depth < 0:
                    return "Unmatched ')'."
            elif c in OPERATORS:
                if expect_operand:
                    return "Two operators in a row (or one at the start)."
                expect_operand = True
            else:
                if not expect_operand:
                    return "Two operands in a row — every operand needs an operator."
                expect_operand = False
        if depth:
            return "Unmatched '('."
        if expect_operand:
            return "The expression ends with an operator."
        return None
    seq = text if kind == "postfix" else text[::-1]
    size = 0
    for c in seq:
        if c in OPERATORS:
            if size < 2:
                return f"Not a valid {kind} expression — an operator lacks operands."
            size -= 1
        else:
            size += 1
    if size != 1:
        return f"Not a valid {kind} expression — operands and operators don't balance."
    return None


def trace(text: str, algorithm: str):
    src, dst = MODES[algorithm]
    steps: list = []
    counts = {"pushes": 0, "pops": 0}
    rtl = src == "prefix" or (src == "infix" and dst == "prefix")
    state = {"stack": [], "output": ""}

    def add(note, pos=None, action=None, final=False):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "stack": list(state["stack"]),
                "pos": pos,
                "action": action,
                "output": state["output"],
                "output_label": dst.upper() + (" (BUILT REVERSED)" if
                                                src == "infix" and dst == "prefix"
                                                and not final else ""),
                "rtl": rtl,
                "balanced": None,
                "counts": dict(counts),
            },
            "highlight": {"index": pos},
            "note": note,
        })

    def push(x):
        state["stack"].append(x)
        counts["pushes"] += 1

    def pop():
        counts["pops"] += 1
        return state["stack"].pop()

    if src == "infix":
        result = _operator_stack(text, rtl, add, push, pop, state)
    else:
        result = _operand_stack(text, src, dst, add, push, pop, state)

    return {
        "meta": {"algorithm": algorithm, "view": "stack", "language": "python",
                 "result": result, "from": src, "to": dst},
        "text": text,
        "steps": steps,
    }


def _operator_stack(text, rtl, add, push, pop, state):
    n = len(text)
    order = range(n - 1, -1, -1) if rtl else range(n)
    opener, closer = (")", "(") if rtl else ("(", ")")
    if rtl:
        add("Infix → prefix: scan right to left. That flips the roles of the "
            "brackets (')' opens, '(' closes) and writes the output backwards; "
            "reverse it at the end.")
    else:
        add("Infix → postfix: operands go straight to the output; operators "
            "wait on the stack until something weaker (or a ')') forces them out.")

    def must_pop(top, op):
        if top == opener:
            return False
        if rtl:
            # Scanning backwards, ties stay put — except ^, whose
            # right-associativity turns into popping on ties here.
            return PREC[top] > PREC[op] or (op == "^" and top == "^")
        return PREC[top] > PREC[op] or (PREC[top] == PREC[op] and op != "^")

    for i in order:
        c = text[i]
        if is_operand(c):
            state["output"] += c
            add(f"'{c}' is an operand — straight to the output.", i, "push")
        elif c == opener:
            push(c)
            add(f"'{c}' opens a group — push it as a wall.", i, "push")
        elif c == closer:
            flushed = []
            while state["stack"] and state["stack"][-1] != opener:
                flushed.append(pop())
                state["output"] += flushed[-1]
            pop()
            add(f"'{c}' closes the group — pop {', '.join(flushed) or 'nothing'} "
                f"to the output and drop the matching '{opener}'.", i, "pop")
        else:
            flushed = []
            while state["stack"] and must_pop(state["stack"][-1], c):
                flushed.append(pop())
                state["output"] += flushed[-1]
            push(c)
            why = (f"first pop {', '.join(flushed)} — they bind at least as tightly"
                   if flushed else "nothing on the stack binds tighter")
            add(f"Operator '{c}': {why}; then push '{c}'.", i, "push")

    rest = []
    while state["stack"]:
        rest.append(pop())
        state["output"] += rest[-1]
    if rest:
        add(f"Input finished — pop the rest ({', '.join(rest)}) to the output.")
    if rtl:
        state["output"] = state["output"][::-1]
        add(f"Reverse what was built: the prefix form is {state['output']}.",
            final=True)
    else:
        add(f"Postfix form: {state['output']}. No brackets needed — the order "
            f"of the operators now encodes the precedence.", final=True)
    return state["output"]


def _operand_stack(text, src, dst, add, push, pop, state):
    n = len(text)
    rtl = src == "prefix"
    order = range(n - 1, -1, -1) if rtl else range(n)
    direction = "right to left" if rtl else "left to right"
    add(f"{src.capitalize()} → {dst}: scan {direction}. Operands are pushed; "
        f"each operator pops two sub-expressions and pushes them combined.")
    for i in order:
        c = text[i]
        if is_operand(c):
            push(c)
            add(f"'{c}' is an operand — push it.", i, "push")
            continue
        first, second = pop(), pop()
        # Postfix: the second pop was written first (left operand).
        # Prefix (scanned backwards): the first pop is the left operand.
        left, right = (second, first) if src == "postfix" else (first, second)
        if dst == "infix":
            combined = f"({left}{c}{right})"
        elif dst == "prefix":
            combined = f"{c}{left}{right}"
        else:
            combined = f"{left}{right}{c}"
        push(combined)
        add(f"Operator '{c}': pop {first} and {second}; the left operand is "
            f"{left}. Push {combined}.", i, "pop")
    state["output"] = state["stack"][-1]
    add(f"One item left on the stack — that's the {dst} form: "
        f"{state['output']}.", final=True)
    return state["output"]
