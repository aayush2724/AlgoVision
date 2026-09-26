"""Delete All Occurrences of a Key in a Doubly Linked List.

Walk the list once. When a node holds the key, stitch its neighbours to each
other — prev.next skips forward past it, next.prev skips back past it — and if
it was the head, the head moves on. Because every node knows both neighbours,
no trailing "previous" pointer is needed, unlike the singly linked version.

Reuses the `list` view: solid `next` arrows, dashed `prev_links`, removed
nodes dimmed via `removed`, and `pointers` for head and temp.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def trace(array: list, key: float):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    prv = [i - 1 if i > 0 else None for i in range(n)]
    removed: list = []
    steps: list = []
    counts = {"visited": 0, "deleted": 0}
    ptr = {"head": 0 if n else None, "temp": 0 if n else None}

    def add(note):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "prev_links": list(prv),
                "removed": list(removed),
                "curr": ptr["temp"],
                "pointers": [[k, ptr[k]] for k in ("head", "temp")
                             if ptr[k] is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": ptr["temp"]},
            "note": note,
        })

    if n == 0:
        add("An empty list — nothing to delete.")
        return _result(values, steps, [])

    add(f"Delete every {_fmt(key)}. Walk once; at each match, point its "
        f"neighbours at each other so the node drops out of both directions.")

    while ptr["temp"] is not None:
        t = ptr["temp"]
        counts["visited"] += 1
        after = nxt[t]
        if values[t] != key:
            ptr["temp"] = after
            add(f"Node {t} holds {_fmt(values[t])}, not {_fmt(key)} — keep it "
                f"and move on.")
            continue
        before = prv[t]
        parts = []
        if t == ptr["head"]:
            ptr["head"] = after
            parts.append("it was the head, so the head moves to "
                         + ("nothing" if after is None else f"node {after}"))
        if before is not None:
            nxt[before] = after
            parts.append(f"node {before}.next skips to "
                         + ("nothing" if after is None else f"node {after}"))
        if after is not None:
            prv[after] = before
            parts.append(f"node {after}.prev skips back to "
                         + ("nothing" if before is None else f"node {before}"))
        nxt[t] = prv[t] = None
        removed.append(t)
        counts["deleted"] += 1
        ptr["temp"] = after
        add(f"Node {t} holds {_fmt(key)} — unlink it: "
            f"{'; '.join(parts) or 'it was the only node'}.")

    order = []
    k = ptr["head"]
    while k is not None:
        order.append(values[k])
        k = nxt[k]
    left = " ⇄ ".join(_fmt(v) for v in order) or "an empty list"
    add(f"Done: {counts['deleted']} node(s) removed in one pass over "
        f"{counts['visited']}. What's left: {left}.")
    return _result(values, steps, order)


def _result(values, steps, order):
    return {
        "meta": {
            "algorithm": "dll_delete_key",
            "view": "list",
            "language": "python",
            "result": order,
        },
        "array": values,
        "steps": steps,
    }
