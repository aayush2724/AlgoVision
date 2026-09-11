MAX_LIST_LEN = 10


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    values = list(array)
    n = len(values)
    # next-pointer per node index; None = end of list
    nxt: list = [i + 1 if i < n - 1 else None for i in range(n)]
    steps = []
    counts = {"flips": 0}
    prev: int | None = None
    curr: int | None = 0 if n else None
    saved: int | None = None

    def add(note):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "prev": prev,
                "curr": curr,
                "saved": saved,
                "counts": dict(counts),
            },
            "highlight": {"index": curr},
            "note": note,
        })

    if n == 0:
        add("An empty chain — nothing to reverse.")
        return _result(values, steps)
    if n == 1:
        add("A single carriage is its own reversal.")
        return _result(values, steps)

    add(
        f"A chain of {n} carriages, each coupled to the next. "
        f"Reverse every coupling using three pointers: prev, curr, next."
    )

    while curr is not None:
        saved = nxt[curr]
        nxt[curr] = prev
        counts["flips"] += 1
        add(
            f"Save the next carriage ({'none — end of chain' if saved is None else 'node ' + str(saved)}), "
            f"then flip node {curr}'s coupling to point back at "
            f"{'nothing (it becomes the tail)' if prev is None else 'node ' + str(prev)}."
        )
        prev, curr = curr, saved
        saved = None
        add(
            f"Advance: prev is now node {prev}, curr is "
            f"{'None — we ran off the end' if curr is None else 'node ' + str(curr)}."
        )

    add(f"curr is None — node {prev} ({_fmt(values[prev])}) is the new head. Chain fully reversed.")
    return _result(values, steps)


def _result(values, steps):
    return {
        "meta": {"algorithm": "linked_list_reverse", "view": "list", "language": "python"},
        "array": values,
        "steps": steps,
    }
