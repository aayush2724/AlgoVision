"""The three depth-first tree walks, on one tree, back to back.

Seeing inorder / preorder / postorder over the same BST is the point: the
visit order changes entirely, but only the *position of the visit* inside the
recursion moves. Inorder on a BST comes out sorted, which is the punchline.
"""

MAX_TREE_LEN = 12


def _fmt(v: float) -> str:
    return f"{v:g}"


def _build(values):
    """Insert into a BST; returns nodes as {id, value, left, right}."""
    nodes: list[dict] = []

    def insert(root_id, value):
        if root_id is None:
            nodes.append({"id": len(nodes), "value": value,
                          "left": None, "right": None})
            return len(nodes) - 1
        node = nodes[root_id]
        if value < node["value"]:
            node["left"] = insert(node["left"], value)
        else:
            node["right"] = insert(node["right"], value)
        return root_id

    root = None
    for v in values:
        root = insert(root, v)
    return nodes, root


def _layout(nodes, root):
    """Assign depth and a 0..1 x position from the inorder rank."""
    order: list[int] = []

    def walk(nid, depth):
        if nid is None:
            return
        nodes[nid]["depth"] = depth
        walk(nodes[nid]["left"], depth + 1)
        order.append(nid)
        walk(nodes[nid]["right"], depth + 1)

    walk(root, 0)
    n = max(len(order), 1)
    for rank, nid in enumerate(order):
        nodes[nid]["x"] = (rank + 0.5) / n
    return nodes


def trace(array: list[float]):
    values = list(array)
    steps: list = []
    counts = {"visits": 0, "descents": 0}

    if not values:
        steps.append({
            "i": 0, "line": 0,
            "structures": {"tree": [], "current": None, "visited": [],
                           "order": [], "counts": dict(counts)},
            "highlight": {"index": None},
            "note": "An empty tree has nothing to walk.",
        })
        return _result(values, steps, {})

    nodes, root = _build(values)
    _layout(nodes, root)

    visited: list[int] = []
    emitted: list[str] = []

    def snapshot():
        return [{"id": n["id"], "value": n["value"], "depth": n["depth"],
                 "x": n["x"], "left": n["left"], "right": n["right"]}
                for n in nodes]

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": snapshot(),
                "current": current,
                "visited": list(visited),
                "order": list(emitted),
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    add(f"A BST built from {', '.join(_fmt(v) for v in values)}. Now walk it "
        f"three ways — the only thing that changes is *when* a node is read "
        f"relative to its children.")

    results = {}

    for mode, blurb in (
        ("inorder", "left subtree → read node → right subtree"),
        ("preorder", "read node → left subtree → right subtree"),
        ("postorder", "left subtree → right subtree → read node"),
    ):
        visited.clear()
        emitted.clear()
        add(f"{mode.upper()}: {blurb}.")

        def visit(nid, node, mode=mode):
            counts["visits"] += 1
            visited.append(nid)
            emitted.append(_fmt(node["value"]))
            add(f"Read {_fmt(node['value'])} — position {len(emitted)} in the "
                f"{mode} walk.", current=nid)

        def walk(nid, mode=mode):
            if nid is None:
                return
            counts["descents"] += 1
            node = nodes[nid]
            if mode == "preorder":
                visit(nid, node)
            walk(node["left"])
            if mode == "inorder":
                visit(nid, node)
            walk(node["right"])
            if mode == "postorder":
                visit(nid, node)

        walk(root)
        results[mode] = list(emitted)
        note = f"{mode.upper()} result: {' → '.join(emitted)}."
        if mode == "inorder":
            note += (" On a binary search tree that always comes out sorted — "
                     "which is exactly what makes a BST useful.")
        add(note)

    add(f"Same tree, same {len(nodes)} nodes, three different orders. Every "
        f"walk is O(n): each node is read exactly once per traversal.")
    return _result(values, steps, results)


def _result(values, steps, results):
    return {
        "meta": {
            "algorithm": "tree_traversal",
            "view": "tree",
            "language": "python",
            "results": results,
        },
        "array": values,
        "steps": steps,
    }
