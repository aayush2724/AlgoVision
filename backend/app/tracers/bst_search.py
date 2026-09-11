from app.tracers.bst_insert import MAX_TREE_LEN, build, serialize  # noqa: F401


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], target: float):
    values = list(array)
    nodes, root, _ = build(values)
    steps = []
    counts = {"comparisons": 0}

    def add(note, current=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": serialize(nodes, root),
                "current": current,
                "inserting": None,
                "found": found,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    if root is None:
        add("The tree is empty — nothing to search.", found=False)
        return _result(values, target, steps)

    add(f"BST built from your {len(values)} values. "
        f"Search for {_fmt(target)} — each comparison discards a whole subtree.")

    cur = root
    while cur is not None:
        counts["comparisons"] += 1
        n = nodes[cur]
        if target == n["value"]:
            add(f"{_fmt(target)} equals this node — found it!", current=cur, found=True)
            return _result(values, target, steps)
        if target < n["value"]:
            nxt = n["left"]
            add(f"{_fmt(target)} < {_fmt(n['value'])} — the whole right subtree "
                f"can't contain it. Go left.", current=nxt if nxt is not None else cur)
        else:
            nxt = n["right"]
            add(f"{_fmt(target)} > {_fmt(n['value'])} — the whole left subtree "
                f"can't contain it. Go right.", current=nxt if nxt is not None else cur)
        cur = nxt

    add(f"Reached an empty branch — {_fmt(target)} is not in the tree.", found=False)
    return _result(values, target, steps)


def _result(values, target, steps):
    return {
        "meta": {"algorithm": "bst_search", "view": "tree", "language": "python",
                 "target": target},
        "array": values,
        "steps": steps,
    }
