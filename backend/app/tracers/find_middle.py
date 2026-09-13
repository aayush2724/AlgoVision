"""Find the middle of a linked list in one pass — two runners, one twice as
fast as the other.

The fast pointer moves two nodes for every one the slow pointer takes. By the
time fast runs off the end, slow has covered exactly half the distance, so it
is sitting on the middle node — found without ever learning the length first,
and without a second traversal.

Reuses the `list` view: nodes are the carriages, the `next` arrows are static,
and two named `pointers` (slow, fast) walk the chain. No new renderer.
"""

MAX_LIST_LEN = 12


def _fmt(v):
    return f"{v:g}"


def trace(array: list):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    steps: list = []
    counts = {"slow_steps": 0, "fast_steps": 0}
    slow = 0 if n else None
    fast = 0 if n else None

    def add(note):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "pointers": ([["slow", slow], ["fast", fast]]
                             if slow is not None else []),
                "counts": dict(counts),
            },
            "highlight": {"index": slow},
            "note": note,
        })

    if n == 0:
        add("An empty list has no middle.")
        return _result(values, None, steps)

    add(f"Two runners start at the head. The fast one takes two steps for every "
        f"one the slow one takes — so when fast reaches the end, slow is exactly "
        f"halfway: the middle.")

    # Advance fast by two and slow by one until fast (or fast.next) runs out.
    while fast is not None and nxt[fast] is not None:
        slow = nxt[slow]
        counts["slow_steps"] += 1
        fast = nxt[nxt[fast]]
        counts["fast_steps"] += 2
        if fast is not None:
            add(f"Slow steps to node {slow}; fast leaps to node {fast}. "
                f"Fast is always about twice as far along.")
        else:
            add(f"Slow steps to node {slow}; fast leaps off the end. That is the "
                f"stop signal.")

    add(f"Fast has reached the end, so slow stops on the middle: node {slow} "
        f"holding {_fmt(values[slow])}. One pass, no length counted first — "
        f"for {n} nodes slow moved {counts['slow_steps']} time(s).")
    return _result(values, slow, steps)


def _result(values, middle, steps):
    return {
        "meta": {
            "algorithm": "find_middle",
            "view": "list",
            "language": "python",
            "middle_index": middle,
            "middle_value": (values[middle] if middle is not None else None),
        },
        "array": values,
        "steps": steps,
    }
