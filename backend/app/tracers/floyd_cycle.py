"""Floyd's cycle detection — the tortoise and the hare.

The list is built from the given values; `link_to` is the index the tail
points back to (-1 for a normal, terminated list). Two pointers move at
different speeds: if a loop exists they must eventually collide inside it,
and a second walk from the head then finds where the loop begins.
"""

MAX_LIST_LEN = 10


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], link_to: int = -1):
    values = list(array)
    n = len(values)
    # next[i] = index of the following node, or None at the end of the chain
    nxt: list = [i + 1 if i < n - 1 else None for i in range(n)]
    if n and 0 <= link_to < n:
        nxt[n - 1] = link_to
    steps: list = []
    counts = {"slow_moves": 0, "fast_moves": 0}
    slow: int | None = None
    fast: int | None = None

    def _pointers():
        out = []
        if slow is not None:
            out.append(["S", slow])
        if fast is not None:
            out.append(["F", fast])
        return out

    def add(note, pointers=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "curr": slow,
                "prev": fast,
                "saved": None,
                "pointers": pointers or _pointers(),
                "counts": dict(counts),
            },
            "highlight": {"index": slow},
            "note": note,
        })

    if n == 0:
        add("An empty chain cannot loop.")
        return _result(values, steps, link_to, found=False, start=None)

    looped = 0 <= link_to < n
    add(f"A chain of {n} nodes"
        + (f", with the tail wired back to node {link_to}."
           if looped else ", ending in ∅.")
        + " Send a slow pointer one step at a time and a fast pointer two. "
          "If there is a loop, the fast one laps the slow one.")

    slow = 0
    fast = 0
    add("Both pointers start at the head.")

    while True:
        nxt_slow = nxt[slow]
        step1 = nxt[fast] if fast is not None else None
        step2 = nxt[step1] if step1 is not None else None
        if nxt_slow is None or step1 is None or step2 is None:
            fast = step1
            add("The fast pointer ran off the end of the chain. Only a "
                "terminated list lets that happen — there is no cycle.")
            return _result(values, steps, link_to, found=False, start=None)

        slow = nxt_slow
        counts["slow_moves"] += 1
        fast = step2
        counts["fast_moves"] += 2
        add(f"Slow steps to node {slow} ({_fmt(values[slow])}); fast takes two "
            f"and lands on node {fast} ({_fmt(values[fast])}).")

        if slow == fast:
            add(f"Both pointers are on node {slow} — the fast one has lapped "
                f"the slow one. That collision proves a cycle exists.")
            break

    # Phase two: the distance from head to loop start equals the distance
    # from the meeting point to loop start, so two 1-step walks converge on it.
    finder = 0
    add("Now find where the loop begins: reset one pointer to the head and "
        "advance both one step at a time. They meet at the loop's entrance.")
    while finder != slow:
        finder = nxt[finder]
        slow = nxt[slow]
        counts["slow_moves"] += 1
        fast = slow
        add(f"Both advance one step — head-walker at node {finder}, "
            f"loop-walker at node {slow}.")

    add(f"They meet at node {finder} ({_fmt(values[finder])}) — that is where "
        f"the loop starts. Found with two pointers and no extra memory: "
        f"O(n) time, O(1) space.")
    return _result(values, steps, link_to, found=True, start=finder)


def _result(values, steps, link_to, found, start):
    return {
        "meta": {
            "algorithm": "floyd_cycle",
            "view": "list",
            "language": "python",
            "link_to": link_to,
            "has_cycle": found,
            "cycle_start": start,
        },
        "array": values,
        "steps": steps,
    }
