"""Delete the Middle Node of a Linked List — tortoise and hare, one step early.

To delete a node you must stand on the node *before* it. Start fast two nodes
ahead (at head.next.next) instead of at the head: when fast runs out, slow is
exactly one before the middle (position ⌊n/2⌋, 0-indexed), so it can unlink it.
One pass, no length count.

Reuses the `list` view: named `pointers` (slow, fast), the deleted node is
dimmed via `removed`.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def trace(array: list):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    removed: list = []
    steps: list = []
    counts = {"slow_steps": 0, "fast_steps": 0}
    ptr = {"slow": None, "fast": None}

    def add(note, curr=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "removed": list(removed),
                "curr": curr,
                "pointers": [[p, v] for p, v in ptr.items() if v is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": curr},
            "note": note,
        })

    if n <= 1:
        removed.extend(range(n))
        add("A single node is its own middle — deleting it leaves an empty "
            "list." if n else "An empty list has no middle.")
        return _result(values, steps, [], 0 if n else None)

    ptr["slow"] = 0
    ptr["fast"] = nxt[nxt[0]] if nxt[0] is not None else None
    add("slow starts at the head, fast two nodes ahead — one step earlier "
        "than the plain find-middle, so slow stops *before* the middle.", 0)
    while ptr["fast"] is not None and nxt[ptr["fast"]] is not None:
        ptr["slow"] = nxt[ptr["slow"]]
        ptr["fast"] = nxt[nxt[ptr["fast"]]]
        counts["slow_steps"] += 1
        counts["fast_steps"] += 2
        where = "off the end" if ptr["fast"] is None else f"node {ptr['fast']}"
        add(f"slow → node {ptr['slow']}, fast → {where}.", ptr["slow"])

    s = ptr["slow"]
    mid = nxt[s]
    nxt[s] = nxt[mid]
    nxt[mid] = None
    removed.append(mid)
    add(f"Fast is done, so slow (node {s}) sits just before the middle. "
        f"Unlink node {mid} ({_fmt(values[mid])}): node {s} now points to "
        f"{'nothing' if nxt[s] is None else f'node {nxt[s]}'}.", s)

    out, j = [], 0
    while j is not None:
        out.append(values[j])
        j = nxt[j]
    ptr.update(slow=None, fast=None)
    add(f"Result: {' → '.join(_fmt(v) for v in out)}. One pass — the middle "
        f"of {n} nodes is position {n // 2}.")
    return _result(values, steps, out, mid)


def _result(values, steps, out, mid):
    return {
        "meta": {
            "algorithm": "delete_middle",
            "view": "list",
            "language": "python",
            "result": out,
            "removed": mid,
        },
        "array": values,
        "steps": steps,
    }
