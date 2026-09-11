MAX_TEXT_LEN = 20
ALLOWED_CHARS = set("()[]{}")
_PAIRS = {")": "(", "]": "[", "}": "{"}


def trace(text: str):
    steps = []
    stack: list = []
    counts = {"pushes": 0, "pops": 0}
    balanced = None

    def add(note, pos=None, action=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "stack": list(stack),
                "pos": pos,
                "action": action,
                "balanced": balanced,
                "counts": dict(counts),
            },
            "highlight": {"index": pos},
            "note": note,
        })

    if not text:
        balanced = True
        add("An empty sequence has nothing to mismatch — balanced.", action="done")
        return _result(text, steps)

    add(f"Scan the {len(text)} symbols left to right. Openers wait on the stack "
        f"for their partner.")

    mismatched = False
    for idx, ch in enumerate(text):
        if ch in "([{":
            stack.append(ch)
            counts["pushes"] += 1
            add(f"'{ch}' opens — push it. Stack depth {len(stack)}.", idx, "push")
        else:
            if stack and stack[-1] == _PAIRS[ch]:
                opener = stack.pop()
                counts["pops"] += 1
                add(f"'{ch}' closes the most recent opener '{opener}' — pop. "
                    f"Depth {len(stack)}.", idx, "pop")
            else:
                balanced = False
                mismatched = True
                wrong = stack[-1] if stack else None
                add(
                    f"'{ch}' arrives but "
                    f"{'the stack is empty — nothing to close' if wrong is None else f'the top of the stack is {wrong!r}, not its partner'}"
                    f" — mismatch! Unbalanced.",
                    idx, "mismatch",
                )
                break

    if not mismatched:
        balanced = len(stack) == 0
        if balanced:
            add("Every opener found its partner and the stack is empty — balanced!",
                action="done")
        else:
            add(f"End of input, but {len(stack)} opener(s) still wait on the stack "
                f"— unbalanced.", action="done")

    return _result(text, steps)


def _result(text, steps):
    return {
        "meta": {"algorithm": "balanced_brackets", "view": "stack",
                 "language": "python", "text": text},
        "steps": steps,
    }
