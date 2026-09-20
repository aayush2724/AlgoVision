"""Maximum depth (height) of a binary tree.

The recursion is the lesson: a node's depth is 1 + the deeper of its two
subtrees, and a missing child contributes 0. Because a node can only be
measured after its children, the answers land in post-order — leaves first,
the root last.
"""

from app.tracers.tree_traversal import _build, _layout, MAX_TREE_LEN  # noqa: F401


def _fmt(v: float) -> str:
    return f"{v:g}"


def _snapshot(nodes):
    return [{"id": n["id"], "value": n["value"], "depth": n["depth"],
             "x": n["x"], "left": n["left"], "right": n["right"]}
            for n in nodes]


def trace(array: list[float]):
    values = list(array)
    steps: list = []
    counts = {"visits": 0}
    marked: list[int] = []

    def add(note, current=None, tree=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": tree if tree is not None else [],
                "current": current,
                "marked": list(marked),
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    if not values:
        add("An empty tree has depth 0.")
        return _result(values, steps, 0)

    nodes, root = _build(values)
    _layout(nodes, root)
    snap = _snapshot(nodes)

    add(f"A binary tree built from {', '.join(_fmt(v) for v in values)}. "
        f"Depth of a node = 1 + the deeper of its two subtrees; an empty "
        f"child counts as 0.", tree=snap)

    best = {"depth": 0}

    def dfs(nid):
        if nid is None:
            return 0
        node = nodes[nid]
        lh = dfs(node["left"])
        rh = dfs(node["right"])
        h = 1 + max(lh, rh)
        counts["visits"] += 1
        marked.append(nid)
        best["depth"] = max(best["depth"], h)
        add(f"{_fmt(node['value'])}: left subtree depth {lh}, right {rh} → "
            f"depth here is 1 + max({lh}, {rh}) = {h}.", current=nid, tree=snap)
        return h

    depth = dfs(root)
    add(f"Maximum depth is {depth} — the longest root-to-leaf chain has "
        f"{depth} node{'s' if depth != 1 else ''}. Each node was measured "
        f"once, so this is O(n).", tree=snap)
    return _result(values, steps, depth)


def _result(values, steps, max_depth):
    return {
        "meta": {
            "algorithm": "tree_max_depth",
            "view": "tree",
            "language": "python",
            "max_depth": max_depth,
        },
        "array": values,
        "steps": steps,
    }
