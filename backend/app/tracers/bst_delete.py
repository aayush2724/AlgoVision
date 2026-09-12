"""BST delete — the operation with three genuinely different cases.

Insert and search each have one story. Delete has three, and the third is the
one students get wrong: a node with two children can't just be unhooked,
because something has to take its place, and only one value qualifies — the
in-order successor (smallest value in the right subtree). This tracer walks
the search, names which case applies, and shows the successor being promoted.
"""

from app.tracers.bst_insert import MAX_TREE_LEN, build, serialize  # noqa: F401


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], target: float):
    values = list(array)
    nodes, root, _ = build(values)
    tgt = float(target)
    steps: list = []
    counts = {"comparisons": 0, "deletions": 0, "promotions": 0}

    def add(note, current=None, successor=None, removing=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": serialize(nodes, root),
                "current": current,
                "successor": successor,
                "removing": removing,
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    if root is None:
        add("The tree is empty — there is nothing to delete.")
        return _result(nodes, root, tgt, False, steps)

    add(f"Delete {_fmt(tgt)}. First find it, exactly like a search: at every "
        f"node go left if the target is smaller, right if it is bigger.",
        current=root)

    parent = None
    cur = root
    side = None
    while cur is not None:
        counts["comparisons"] += 1
        node = nodes[cur]
        if tgt == node["value"]:
            add(f"Found {_fmt(tgt)}. Now the real work — what replaces it?",
                current=cur, removing=cur)
            break
        if tgt < node["value"]:
            if node["left"] is None:
                add(f"{_fmt(tgt)} < {_fmt(node['value'])} — go left, but there "
                    f"is no left child. {_fmt(tgt)} is not in this tree, so "
                    f"there is nothing to delete.", current=cur)
                return _result(nodes, root, tgt, False, steps)
            add(f"{_fmt(tgt)} < {_fmt(node['value'])} — go left.",
                current=node["left"])
            parent, side, cur = cur, "left", node["left"]
        else:
            if node["right"] is None:
                add(f"{_fmt(tgt)} > {_fmt(node['value'])} — go right, but there "
                    f"is no right child. {_fmt(tgt)} is not in this tree, so "
                    f"there is nothing to delete.", current=cur)
                return _result(nodes, root, tgt, False, steps)
            add(f"{_fmt(tgt)} > {_fmt(node['value'])} — go right.",
                current=node["right"])
            parent, side, cur = cur, "right", node["right"]

    node = nodes[cur]
    left, right = node["left"], node["right"]

    def relink(child):
        nonlocal root
        if parent is None:
            root = child
        else:
            nodes[parent][side] = child

    # ── Case 1: leaf ──
    if left is None and right is None:
        add(f"Case 1 — {_fmt(tgt)} is a leaf, with no children at all. "
            f"Nothing depends on it, so it simply detaches.",
            current=cur, removing=cur)
        relink(None)
        del nodes[cur]
        counts["deletions"] += 1
        add(f"{_fmt(tgt)} removed. The easy case: no child had to be rehomed.")
        return _result(nodes, root, tgt, True, steps)

    # ── Case 2: exactly one child ──
    if left is None or right is None:
        child = left if right is None else right
        which = "left" if right is None else "right"
        add(f"Case 2 — {_fmt(tgt)} has exactly one child "
            f"({_fmt(nodes[child]['value'])}, on the {which}). That whole "
            f"subtree already sits on the correct side of everything above it, "
            f"so it just moves up into the empty spot.",
            current=cur, successor=child, removing=cur)
        relink(child)
        del nodes[cur]
        counts["deletions"] += 1
        counts["promotions"] += 1
        add(f"{_fmt(tgt)} removed and {_fmt(nodes[child]['value'])} promoted "
            f"into its place. The ordering still holds — nothing else moved.",
            current=child)
        return _result(nodes, root, tgt, True, steps)

    # ── Case 3: two children — promote the in-order successor ──
    add(f"Case 3 — {_fmt(tgt)} has two children. We cannot just unhook it: "
        f"something must take its place, and it has to be bigger than "
        f"everything on the left and smaller than everything on the right. "
        f"Exactly one value qualifies — the smallest in the right subtree.",
        current=cur, removing=cur)

    succ_parent, succ = cur, right
    add(f"Step into the right subtree at {_fmt(nodes[succ]['value'])}, then "
        f"keep going left as far as possible.", current=succ)
    while nodes[succ]["left"] is not None:
        counts["comparisons"] += 1
        succ_parent, succ = succ, nodes[succ]["left"]
        add(f"{_fmt(nodes[succ]['value'])} is further left — keep going.",
            current=succ)

    succ_val = nodes[succ]["value"]
    add(f"{_fmt(succ_val)} has no left child, so it is the smallest value "
        f"bigger than {_fmt(tgt)} — the in-order successor.",
        current=succ, successor=succ, removing=cur)

    # The successor has no left child, so at most a right subtree to rehome.
    if succ_parent == cur:
        nodes[cur]["right"] = nodes[succ]["right"]
    else:
        nodes[succ_parent]["left"] = nodes[succ]["right"]

    node["value"] = succ_val
    del nodes[succ]
    counts["deletions"] += 1
    counts["promotions"] += 1

    add(f"Copy {_fmt(succ_val)} into the deleted node's slot and remove the "
        f"successor from where it was. Only one value moved, and the tree is "
        f"still perfectly ordered — an in-order walk proves it.",
        current=cur)

    return _result(nodes, root, tgt, True, steps)


def _inorder(nodes, root):
    out: list = []

    def walk(nid):
        if nid is None:
            return
        walk(nodes[nid]["left"])
        out.append(nodes[nid]["value"])
        walk(nodes[nid]["right"])

    walk(root)
    return out


def _result(nodes, root, target, deleted, steps):
    return {
        "meta": {
            "algorithm": "bst_delete",
            "view": "tree",
            "language": "python",
            "target": target,
            "deleted": deleted,
            "inorder": _inorder(nodes, root),
        },
        "steps": steps,
    }
