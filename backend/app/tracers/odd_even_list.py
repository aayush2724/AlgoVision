"""Segregate Odd and Even Positions in a Linked List — two chains, one pass.

Positions 1, 3, 5… go first, then 2, 4, 6…, each group keeping its order. Keep
an `odd` pointer and an `even` pointer that leapfrog: odd links to the node
after even, then even links to the node after the new odd. At the end, the odd
chain's tail is joined to the saved head of the even chain. O(n), no new
nodes — only arrows change.

Reuses the `list` view: watch the `next` arrows skip over neighbours as the
two chains separate. No new renderer.
"""

MAX_LIST_LEN = 10


def _fmt(v):
    return f"{v:g}"


def trace(array: list):
    values = list(array)
    n = len(values)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    steps: list = []
    counts = {"relinks": 0}
    ptr = {"odd": None, "even": None, "evenHead": None}

    def add(note, curr=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "curr": curr,
                "pointers": [[k, v] for k, v in ptr.items() if v is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": curr},
            "note": note,
        })

    def order():
        out, k = [], 0 if n else None
        while k is not None:
            out.append(values[k])
            k = nxt[k]
        return out

    if n <= 2:
        add("With two nodes or fewer, odd positions already come first.")
        return _result(values, steps, order())

    ptr.update(odd=0, even=1, evenHead=1)
    add("Positions 1, 3, 5… first, then 2, 4, 6…. `odd` starts at node 0, "
        "`even` at node 1; remember node 1 as the even chain's head.", curr=0)

    while ptr["even"] is not None and nxt[ptr["even"]] is not None:
        o, e = ptr["odd"], ptr["even"]
        nxt[o] = nxt[e]
        ptr["odd"] = nxt[o]
        counts["relinks"] += 1
        add(f"odd (node {o}) skips even and links to node {nxt[o]}; odd moves "
            f"there.", curr=ptr["odd"])
        nxt[e] = nxt[ptr["odd"]]
        ptr["even"] = nxt[e]
        counts["relinks"] += 1
        add(f"even (node {e}) skips the new odd and links to "
            f"{'nothing' if nxt[e] is None else f'node {nxt[e]}'}; even "
            f"moves there.", curr=ptr["even"])

    tail = ptr["odd"]
    nxt[tail] = ptr["evenHead"]
    counts["relinks"] += 1
    add(f"Chains separated. Join the odd chain's tail (node {tail}) to the "
        f"even chain's head (node {ptr['evenHead']}).", curr=tail)
    ptr.update(odd=None, even=None)
    result = order()
    add(f"Result: {' → '.join(_fmt(v) for v in result)}. {counts['relinks']} "
        f"arrow changes, no nodes created or moved.")
    return _result(values, steps, result)


def _result(values, steps, result):
    return {
        "meta": {
            "algorithm": "odd_even_list",
            "view": "list",
            "language": "python",
            "result": result,
        },
        "array": values,
        "steps": steps,
    }
