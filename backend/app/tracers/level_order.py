"""Level-order (breadth-first) traversal of a binary tree.

Where the three depth-first walks recurse, level order sweeps the tree top to
bottom, left to right, using a queue: visit a node, enqueue its children, repeat.
The queue is the whole idea — it holds exactly the frontier of the next level.
"""

from collections import deque

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
    counts = {"visits": 0, "enqueues": 0}
    marked: list[int] = []
    order: list[str] = []

    def add(note, current=None, tree=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": tree if tree is not None else [],
                "current": current,
                "marked": list(marked),
                "order": list(order),
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    if not values:
        add("An empty tree has nothing to walk.")
        return _result(values, steps, [])

    nodes, root = _build(values)
    _layout(nodes, root)
    snap = _snapshot(nodes)

    add(f"A binary tree built from {', '.join(_fmt(v) for v in values)}. "
        f"Level order reads it top to bottom, left to right — using a queue.",
        tree=snap)

    queue = deque([(root, 0)])
    counts["enqueues"] += 1
    levels: list[list[str]] = []

    while queue:
        nid, depth = queue.popleft()
        node = nodes[nid]
        counts["visits"] += 1
        marked.append(nid)
        order.append(_fmt(node["value"]))
        while len(levels) <= depth:
            levels.append([])
        levels[depth].append(_fmt(node["value"]))
        children = [cid for cid in (node["left"], node["right"]) if cid is not None]
        tail = (f" Enqueue its {'child' if len(children) == 1 else 'children'} "
                f"{', '.join(_fmt(nodes[c]['value']) for c in children)}."
                if children else " It is a leaf — nothing to enqueue.")
        add(f"Dequeue {_fmt(node['value'])} (level {depth}) — visit it.{tail}",
            current=nid, tree=snap)
        for cid in children:
            queue.append((cid, depth + 1))
            counts["enqueues"] += 1

    grouped = "; ".join("[" + ", ".join(lv) + "]" for lv in levels)
    add(f"Level order: {' → '.join(order)}. By level: {grouped}. Every node "
        f"visited exactly once — O(n), and the queue never held more than one "
        f"level at a time.", tree=snap)
    return _result(values, steps, levels)


def _result(values, steps, levels):
    return {
        "meta": {
            "algorithm": "level_order",
            "view": "tree",
            "language": "python",
            "levels": levels,
        },
        "array": values,
        "steps": steps,
    }
