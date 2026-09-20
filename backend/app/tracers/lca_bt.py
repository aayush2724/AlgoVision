"""Lowest Common Ancestor in a binary tree (the general algorithm).

Not the BST shortcut — this is the version that works on *any* binary tree.
Recurse from the root: if a node is one of the two targets, report it upward.
A node that hears back from BOTH of its subtrees is the split point — the
lowest node with both targets beneath it — so it is the LCA.
"""

from app.tracers.tree_traversal import _build, _layout, MAX_TREE_LEN  # noqa: F401


def _fmt(v: float) -> str:
    return f"{v:g}"


def _snapshot(nodes):
    return [{"id": n["id"], "value": n["value"], "depth": n["depth"],
             "x": n["x"], "left": n["left"], "right": n["right"]}
            for n in nodes]


def trace(array: list[float], a: float, b: float):
    values = list(array)
    steps: list = []
    counts = {"visits": 0}

    nodes, root = _build(values)
    _layout(nodes, root)
    snap = _snapshot(nodes)
    targets = {nid for nid, n in enumerate(nodes) if n["value"] in (a, b)}

    def add(note, current=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": snap,
                "current": current,
                "marked": list(targets),
                "found": found,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    add(f"Find the lowest common ancestor of {_fmt(a)} and {_fmt(b)} "
        f"(highlighted). Recurse from the root: a subtree reports back if a "
        f"target lives inside it.")

    def dfs(nid):
        if nid is None:
            return None
        node = nodes[nid]
        counts["visits"] += 1
        if node["value"] in (a, b):
            add(f"{_fmt(node['value'])} is one of the targets — report it up "
                f"to the parent.", current=nid)
            return nid
        add(f"At {_fmt(node['value'])} — neither target. Ask both subtrees.",
            current=nid)
        left = dfs(node["left"])
        right = dfs(node["right"])
        if left is not None and right is not None:
            add(f"{_fmt(node['value'])} hears a target from BOTH sides — it is "
                f"the lowest common ancestor.", current=nid, found=True)
            return nid
        found_side = left if left is not None else right
        if found_side is not None:
            add(f"Only one side of {_fmt(node['value'])} reported a target — "
                f"pass that answer ({_fmt(nodes[found_side]['value'])}) further "
                f"up.", current=nid)
        return found_side

    result = dfs(root)
    if result is not None:
        add(f"LCA of {_fmt(a)} and {_fmt(b)} is {_fmt(nodes[result]['value'])} "
            f"— the deepest node with both values in its subtree.",
            current=result, found=True)
    return _result(values, steps, None if result is None else nodes[result]["value"], a, b)


def _result(values, steps, lca_value, a, b):
    return {
        "meta": {
            "algorithm": "lca_bt",
            "view": "tree",
            "language": "python",
            "lca": lca_value,
            "targets": [a, b],
        },
        "array": values,
        "steps": steps,
    }
