"""Arithmetic on numbers stored as linked lists, one digit per node.

* add_two_numbers — both lists hold digits least-significant first (so
  342 is 2 → 4 → 3). Walk them together: digit + digit + carry; write the
  ones digit to the result, carry the tens. A leftover carry becomes one
  more node.
* add_one_list — the list holds digits most-significant first (1 → 9 → 9).
  The +1 enters at the tail, so recurse to the end first and let the carry
  ripple back toward the head; a carry out of the head needs a new head node.

Uses the `grid` view as the column-addition picture: one column per list
position, rows for each input list, the carry, and the result. The column
being added is `col`; finished result digits light green.
"""

TITLES = {
    "add_two_numbers": "Add Two Numbers (Linked Lists)",
    "add_one_list": "Add 1 to a Number as a Linked List",
}
MAX_DIGITS = 8


def parse(text):
    parts = [p for p in (text or "").replace(" ", "").split("/") if p]
    try:
        return [[int(d) for d in p.split(",") if d != ""] for p in parts]
    except ValueError:
        return None


def validate(algo, lists):
    want = 2 if algo == "add_two_numbers" else 1
    if not lists or len(lists) != want:
        return ("Give two lists separated by '/', e.g. 2,4,3/5,6,4."
                if want == 2 else "Give one list of digits, e.g. 1,9,9.")
    for ls in lists:
        if not ls or len(ls) > MAX_DIGITS or any(not (0 <= d <= 9) for d in ls):
            return f"Each list needs 1–{MAX_DIGITS} digits (0–9)."
    return None


def trace(algo, lists):
    return _add_two(*lists) if algo == "add_two_numbers" else _add_one(lists[0])


def _num(ds):
    return int("".join(map(str, reversed(ds))))


def _add_two(a, b):
    n = max(len(a), len(b)) + 1          # room for a final carry node
    grid = [[None] * n for _ in range(4)]
    for i, d in enumerate(a):
        grid[0][i] = d
    for i, d in enumerate(b):
        grid[1][i] = d
    steps: list = []
    counts = {"nodes_added": 0}
    done: list = []

    def add(note, col=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"grid": [r[:] for r in grid], "row": 3,
                                     "col": col, "deps": [], "match": True,
                                     "path": [[3, c] for c in done],
                                     "counts": dict(counts)},
                      "highlight": {"index": col}, "note": note})

    add(f"The lists store digits least-significant first: {_num(a)} and "
        f"{_num(b)}. Walk both together, adding column by column with a carry.")
    carry, i = 0, 0
    while i < len(a) or i < len(b) or carry:
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        total = x + y + carry
        grid[2][i] = carry
        grid[3][i] = total % 10
        counts["nodes_added"] += 1
        done.append(i)
        only_carry = not (i < len(a) or i < len(b))
        parts = f"{x} + {y}" + (f" + carry {carry}" if carry else "")
        add(f"Position {i}: {parts} = {total} → write {total % 10}"
            + (", carry 1." if total >= 10 else ", no carry.")
            + (" Only the carry was left — it becomes a new node." if only_carry else ""),
            i)
        carry = total // 10
        i += 1
    result = [grid[3][c] for c in done]
    add(f"Result list: {' → '.join(map(str, result))}, i.e. "
        f"{_num(a)} + {_num(b)} = {_num(result)}. One pass, O(max(m, n)).")
    return {"meta": {"algorithm": "add_two_numbers", "view": "grid",
                     "language": "python", "result": result,
                     "row_labels": ["list A", "list B", "carry in", "result"],
                     "col_labels": [str(c) for c in range(n)]},
            "steps": steps}


def _add_one(digits):
    n = len(digits)
    # Column 0 is reserved for a possible new head node.
    grid = [[None] + digits[:], [None] * (n + 1), [None] * (n + 1)]
    steps: list = []
    counts = {"calls": 0}
    done: list = []

    def add(note, col=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"grid": [r[:] for r in grid], "row": 2,
                                     "col": col, "deps": [], "match": True,
                                     "path": [[2, c] for c in done],
                                     "counts": dict(counts)},
                      "highlight": {"index": col}, "note": note})

    add(f"The list holds {''.join(map(str, digits))} most-significant first. "
        f"The +1 lands on the last node, so recurse all the way to the tail "
        f"and let the carry travel back.")

    def rec(i):
        counts["calls"] += 1
        if i == n:
            add("Past the tail — return carry 1 (that is the +1).")
            return 1
        add(f"Call on node {i} (digit {digits[i]}) — first recurse to the "
            f"rest of the list.", i + 1)
        carry = rec(i + 1)
        total = digits[i] + carry
        grid[1][i + 1] = carry
        grid[2][i + 1] = total % 10
        done.append(i + 1)
        add(f"Back at node {i}: {digits[i]} + carry {carry} = {total} → "
            f"digit {total % 10}, pass carry {total // 10} to the left.", i + 1)
        return total // 10

    carry = rec(0)
    if carry:
        grid[2][0] = 1
        done.append(0)
        add("A carry came out of the head — create a new head node holding 1.",
            0)
    result = [grid[2][c] for c in range(n + 1) if grid[2][c] is not None]
    add(f"Result: {' → '.join(map(str, result))}. The recursion visits each "
        f"node once — O(n).")
    return {"meta": {"algorithm": "add_one_list", "view": "grid",
                     "language": "python", "result": result,
                     "row_labels": ["digits", "carry in", "result"],
                     "col_labels": ["new"] + [str(c) for c in range(n)]},
            "steps": steps}
