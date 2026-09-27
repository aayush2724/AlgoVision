"""Is a Linked List a Palindrome? — middle, reverse half, compare, restore.

Without extra memory you can't read a singly linked list backwards. So:
(1) find the middle with slow/fast pointers, (2) reverse the second half in
place, (3) walk one pointer from the head and one from the reversed half,
comparing values, and (4) reverse the second half back so the caller's list
is unchanged. O(n) time, O(1) space.

Reuses the `list` view: `next` arrows visibly flip during the reversal, and
named `pointers` change per phase. No new renderer.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def _reverse(nxt, start, add, label):
    prev, curr = None, start
    while curr is not None:
        after = nxt[curr]
        nxt[curr] = prev
        add(f"{label}: flip node {curr}'s arrow to point at "
            f"{'nothing' if prev is None else f'node {prev}'}.",
            [["prev", prev], ["curr", curr]], curr)
        prev, curr = curr, after
    return prev


def trace(array: list):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    steps: list = []
    counts = {"pointer_moves": 0, "comparisons": 0, "flips": 0}

    def add(note, pointers=None, curr=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "curr": curr,
                "pointers": [[k, v] for k, v in (pointers or []) if v is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": curr},
            "note": note,
        })

    def counted_add(note, pointers=None, curr=None):
        counts["flips"] += 1
        add(note, pointers, curr)

    if n <= 1:
        add("Zero or one node reads the same both ways — a palindrome.")
        return _result(values, steps, True)

    add("Can't read a singly linked list backwards, so: find the middle, "
        "reverse the second half, compare the halves, then undo the reversal.")

    slow = fast = 0
    add("Phase 1 — slow moves one, fast moves two.",
        [["slow", slow], ["fast", fast]], slow)
    while nxt[fast] is not None and nxt[nxt[fast]] is not None:
        slow, fast = nxt[slow], nxt[nxt[fast]]
        counts["pointer_moves"] += 1
        add(f"slow → node {slow}, fast → node {fast}.",
            [["slow", slow], ["fast", fast]], slow)
    add(f"Fast can't take two more steps: slow (node {slow}) ends the first "
        f"half. Phase 2 — reverse everything after it.",
        [["slow", slow]], slow)

    second = _reverse(nxt, nxt[slow], counted_add, "Reverse")
    nxt[slow] = None
    add(f"Second half reversed; its new head is node {second}. The first half "
        f"now ends at node {slow}.", [["head", 0], ["tail", second]], second)

    first, sec, ok = 0, second, True
    while sec is not None:
        counts["comparisons"] += 1
        same = values[first] == values[sec]
        add(f"Phase 3 — compare node {first} ({_fmt(values[first])}) with node "
            f"{sec} ({_fmt(values[sec])}): "
            f"{'match' if same else 'MISMATCH — not a palindrome'}.",
            [["first", first], ["second", sec]], sec)
        if not same:
            ok = False
            break
        first, sec = nxt[first], nxt[sec]

    nxt[slow] = _reverse(nxt, second, counted_add, "Phase 4 — restore")
    add(f"{'Palindrome' if ok else 'Not a palindrome'}. The second half was "
        f"reversed back and re-attached, so the list is exactly as given. "
        f"O(n) time, O(1) extra space.")
    return _result(values, steps, ok)


def _result(values, steps, ok):
    return {
        "meta": {
            "algorithm": "ll_palindrome",
            "view": "list",
            "language": "python",
            "result": ok,
        },
        "array": values,
        "steps": steps,
    }
