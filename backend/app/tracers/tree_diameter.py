"""Diameter of a binary tree — the longest path between any two nodes.

The trick that turns this from O(n²) into O(n): the same post-order pass that
computes each node's height also asks "what if the longest path *bends* here?"
That bending path is leftHeight + rightHeight edges. Track the biggest such
value seen and you have the diameter, all in one walk.
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
        add("An empty tree has diameter 0.")
        return _result(values, steps, 0)

    nodes, root = _build(values)
    _layout(nodes, root)
    snap = _snapshot(nodes)

    add(f"A binary tree built from {', '.join(_fmt(v) for v in values)}. "
        f"In one post-order pass we track each node's height and the longest "
        f"path that bends through it (leftHeight + rightHeight edges).",
        tree=snap)

    best = {"dia": 0}

    def dfs(nid):
        if nid is None:
            return 0
        node = nodes[nid]
        lh = dfs(node["left"])
        rh = dfs(node["right"])
        through = lh + rh
        counts["visits"] += 1
        marked.append(nid)
        improved = through > best["dia"]
        if improved:
            best["dia"] = through
        note = (f"{_fmt(node['value'])}: subtree heights L={lh}, R={rh} → a path "
                f"bending here spans {through} edge{'s' if through != 1 else ''}.")
        note += (f" New best diameter: {best['dia']}."
                 if improved else f" Best diameter stays {best['dia']}.")
        add(note, current=nid, tree=snap)
        return 1 + max(lh, rh)

    dfs(root)
    add(f"Diameter is {best['dia']} — the longest path between any two nodes "
        f"is {best['dia']} edge{'s' if best['dia'] != 1 else ''} long. One "
        f"O(n) pass, no recomputed heights.", tree=snap)
    return _result(values, steps, best["dia"])


def _result(values, steps, diameter):
    return {
        "meta": {
            "algorithm": "tree_diameter",
            "view": "tree",
            "language": "python",
            "diameter": diameter,
        },
        "array": values,
        "steps": steps,
    }
