"""Reverse a Doubly Linked List — every node swaps its two pointers.

A singly linked list needs three pointers to reverse (prev, curr, next) because
each node only knows what is ahead. A doubly linked node already knows both
neighbours, so reversal is local: swap its prev and next, then move on to what
*used to be* next — which is now stored in prev. When the walk runs off the
end, the last node visited is the new head.

Reuses the `list` view: solid arrows are `next`, dashed arrows are
`prev_links`, and `pointers` name curr and last. No new view — the list
renderer only learned to draw the optional back-pointers.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def trace(array: list):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    prv = [i - 1 if i > 0 else None for i in range(n)]
    steps: list = []
    counts = {"swaps": 0}
    ptr = {"curr": 0 if n else None, "last": None, "head": 0 if n else None}

    def add(note):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "prev_links": list(prv),
                "curr": ptr["curr"],
                "pointers": [[k, ptr[k]] for k in ("head", "curr", "last")
                             if ptr[k] is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": ptr["curr"]},
            "note": note,
        })

    if n == 0:
        add("An empty list — nothing to reverse.")
        return _result(values, steps, [])

    add(f"A doubly linked list of {n} nodes: solid arrows point forward "
        f"(next), dashed ones point back (prev). To reverse it, every node "
        f"just swaps its two pointers.")

    while ptr["curr"] is not None:
        c = ptr["curr"]
        ptr["last"] = prv[c]
        prv[c], nxt[c] = nxt[c], prv[c]
        counts["swaps"] += 1
        fwd = "nothing" if nxt[c] is None else f"node {nxt[c]}"
        back = "nothing" if prv[c] is None else f"node {prv[c]}"
        add(f"Node {c} ({_fmt(values[c])}): swap its pointers — next now "
            f"points to {fwd}, prev to {back}.")
        ptr["curr"] = prv[c]          # the old next
        if ptr["curr"] is not None:
            add(f"Move to the old next, which now sits in prev: node "
                f"{ptr['curr']}.")

    # The last node swapped is the new head; `last` holds its new next's
    # predecessor, so the head is last's prev (or the only node).
    new_head = prv[ptr["last"]] if ptr["last"] is not None else 0
    ptr["head"], ptr["last"] = new_head, None
    order = []
    k = new_head
    while k is not None:
        order.append(values[k])
        k = nxt[k]
    add(f"Walked off the end. Node {new_head} ({_fmt(values[new_head])}) is the "
        f"new head: {' ⇄ '.join(_fmt(v) for v in order)}. {counts['swaps']} "
        f"swaps, one pass, no extra pointers beyond one temp.")
    return _result(values, steps, order)


def _result(values, steps, order):
    return {
        "meta": {
            "algorithm": "dll_reverse",
            "view": "list",
            "language": "python",
            "result": order,
        },
        "array": values,
        "steps": steps,
    }
