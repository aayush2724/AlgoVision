"""Remove the Nth Node from the End — a fixed gap between two pointers.

You can't count backwards in a singly linked list. Instead, send `fast` N
nodes ahead, then move `fast` and `slow` together. The gap never changes, so
when fast reaches the last node, slow sits just *before* the node to delete —
exactly where you need to be to unlink it. One pass, no length count. If fast
runs off the end during the head start, the node to delete is the head.

Reuses the `list` view: named `pointers` (slow, fast), and the deleted node is
dimmed via `removed`.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def trace(array: list, n_from_end: int):
    values = list(array)
    size = len(values)
    k = int(n_from_end)
    nxt = [i + 1 if i < size - 1 else None for i in range(size)]
    removed: list = []
    steps: list = []
    counts = {"fast_steps": 0, "slow_steps": 0}
    ptr = {"slow": 0, "fast": 0}
    head = 0

    def add(note):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "removed": list(removed),
                "curr": ptr["slow"],
                "pointers": [[p, ptr[p]] for p in ("slow", "fast")
                             if ptr[p] is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": ptr["slow"]},
            "note": note,
        })

    add(f"Remove the {k}th node from the end without measuring the length: "
        f"give fast a {k}-node head start, then move both until fast hits the "
        f"last node.")

    for step in range(k):
        ptr["fast"] = nxt[ptr["fast"]]
        counts["fast_steps"] += 1
        where = "off the end" if ptr["fast"] is None else f"node {ptr['fast']}"
        add(f"Head start {step + 1}/{k}: fast moves to {where}.")

    if ptr["fast"] is None:
        # N equals the length: the head itself is the target.
        removed.append(head)
        head = nxt[head]
        nxt[removed[-1]] = None
        ptr["slow"] = None
        add(f"Fast ran off the end during its head start, so the list has "
            f"exactly {k} nodes — the node to remove is the head. The head "
            f"moves to {'nothing' if head is None else f'node {head}'}.")
    else:
        while nxt[ptr["fast"]] is not None:
            ptr["fast"] = nxt[ptr["fast"]]
            ptr["slow"] = nxt[ptr["slow"]]
            counts["fast_steps"] += 1
            counts["slow_steps"] += 1
            add(f"Move both: slow → node {ptr['slow']}, fast → node "
                f"{ptr['fast']}. The gap stays {k}.")
        s = ptr["slow"]
        target = nxt[s]
        nxt[s] = nxt[target]
        nxt[target] = None
        removed.append(target)
        add(f"Fast is on the last node, so slow (node {s}) is right before the "
            f"target. Unlink node {target} ({_fmt(values[target])}): node {s} "
            f"now points to "
            f"{'nothing' if nxt[s] is None else f'node {nxt[s]}'}.")

    order = []
    j = head
    while j is not None:
        order.append(values[j])
        j = nxt[j]
    add(f"Result: {' → '.join(_fmt(v) for v in order) or 'an empty list'}. "
        f"One pass: {counts['fast_steps']} fast steps, {counts['slow_steps']} "
        f"slow steps — never counting the length.")
    return {
        "meta": {
            "algorithm": "remove_nth_from_end",
            "view": "list",
            "language": "python",
            "result": order,
            "removed": removed[0],
        },
        "array": values,
        "steps": steps,
    }
