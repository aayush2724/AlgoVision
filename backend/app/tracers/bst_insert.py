MAX_TREE_LEN = 12


def _fmt(v: float) -> str:
    return f"{v:g}"


def serialize(nodes: dict, root):
    """Flatten the tree for rendering: in-order rank gives x (0..1), depth gives y."""
    order = []

    def inorder(nid, depth):
        if nid is None:
            return
        n = nodes[nid]
        inorder(n["left"], depth + 1)
        order.append((nid, depth))
        inorder(n["right"], depth + 1)

    inorder(root, 0)
    total = max(len(order), 1)
    return [
        {
            "id": nid,
            "value": nodes[nid]["value"],
            "left": nodes[nid]["left"],
            "right": nodes[nid]["right"],
            "x": (rank + 0.5) / total,
            "depth": depth,
        }
        for rank, (nid, depth) in enumerate(order)
    ]


def build(values):
    """Build a BST (duplicates go right). Returns (nodes, root, comparisons)."""
    nodes: dict = {}
    root = None
    comparisons = 0
    for v in values:
        if root is None:
            nodes[0] = {"value": v, "left": None, "right": None}
            root = 0
            continue
        cur = root
        while True:
            comparisons += 1
            n = nodes[cur]
            side = "left" if v < n["value"] else "right"
            if n[side] is None:
                nid = len(nodes)
                nodes[nid] = {"value": v, "left": None, "right": None}
                n[side] = nid
                break
            cur = n[side]
    return nodes, root, comparisons


def _height(nodes, nid):
    if nid is None:
        return 0
    return 1 + max(_height(nodes, nodes[nid]["left"]),
                   _height(nodes, nodes[nid]["right"]))


def trace(array: list[float]):
    values = list(array)
    nodes: dict = {}
    root = None
    steps = []
    counts = {"comparisons": 0, "insertions": 0}

    def add(note, current=None, inserting=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": serialize(nodes, root),
                "current": current,
                "inserting": inserting,
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    if not values:
        add("No values — an empty tree.")
        return _result(values, steps)

    add(f"Insert {len(values)} values one at a time: smaller goes left, "
        f"bigger (or equal) goes right.")

    for v in values:
        if root is None:
            nodes[0] = {"value": v, "left": None, "right": None}
            root = 0
            counts["insertions"] += 1
            add(f"{_fmt(v)} is the first value — it becomes the root.", current=0)
            continue
        add(f"Insert {_fmt(v)} — start comparing at the root.",
            current=root, inserting=v)
        cur = root
        while True:
            counts["comparisons"] += 1
            n = nodes[cur]
            if v < n["value"]:
                if n["left"] is None:
                    nid = len(nodes)
                    nodes[nid] = {"value": v, "left": None, "right": None}
                    n["left"] = nid
                    counts["insertions"] += 1
                    add(f"{_fmt(v)} < {_fmt(n['value'])} and the left slot is free "
                        f"— attach as left child.", current=nid)
                    break
                add(f"{_fmt(v)} < {_fmt(n['value'])} — go left.",
                    current=n["left"], inserting=v)
                cur = n["left"]
            else:
                if n["right"] is None:
                    nid = len(nodes)
                    nodes[nid] = {"value": v, "left": None, "right": None}
                    n["right"] = nid
                    counts["insertions"] += 1
                    add(f"{_fmt(v)} >= {_fmt(n['value'])} and the right slot is free "
                        f"— attach as right child.", current=nid)
                    break
                add(f"{_fmt(v)} >= {_fmt(n['value'])} — go right.",
                    current=n["right"], inserting=v)
                cur = n["right"]

    h = _height(nodes, root)
    in_order = ", ".join(_fmt(n["value"]) for n in serialize(nodes, root))
    add(f"Tree built — height {h} for {len(values)} values "
        f"(a balanced tree would be ~{max(1, (len(values)).bit_length())}). "
        f"An in-order walk reads sorted: {in_order}.")
    return _result(values, steps)


def _result(values, steps):
    return {
        "meta": {"algorithm": "bst_insert", "view": "tree", "language": "python"},
        "array": values,
        "steps": steps,
    }
