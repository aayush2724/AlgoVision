"""Shared plumbing for binary-tree tracers that take a *shape*, not a BST.

The older tree tracers build a BST by inserting values, which can't express
trees like "1,2,2,3,4,4,3" (symmetric) or a lopsided chain. These parse the
LeetCode level-order form instead: values left to right, level by level, with
`null` (or `-`, `#`, `x`) marking a missing child. Nodes are laid out with the
same inorder-rank layout as every other tree view, so they render identically.
"""

from app.tracers.tree_traversal import _layout

MAX_NODES = 15
NULLS = {"null", "none", "-", "#", "x", "n"}


def parse(text):
    """Level-order text → list of int|None. Raises ValueError with a reason."""
    tokens = [t for t in (text or "").replace(" ", "").split(",") if t != ""]
    if not tokens:
        raise ValueError("Give the tree in level order, e.g. 1,2,3,null,5.")
    vals = []
    for t in tokens:
        if t.lower() in NULLS:
            vals.append(None)
        else:
            try:
                v = int(t)
            except ValueError:
                raise ValueError(f"'{t}' is not a number or null.") from None
            if abs(v) > 999:
                raise ValueError("Keep node values within ±999.")
            vals.append(v)
    if vals[0] is None:
        raise ValueError("The root can't be null.")
    if sum(v is not None for v in vals) > MAX_NODES:
        raise ValueError(f"Max {MAX_NODES} nodes — the tree has to stay readable.")
    return vals


def build(vals):
    """LeetCode-style build: a queue hands out the next two slots per node."""
    nodes = [{"id": 0, "value": vals[0], "left": None, "right": None}]
    queue, i = [0], 1
    while queue and i < len(vals):
        parent = queue.pop(0)
        for side in ("left", "right"):
            if i >= len(vals):
                break
            if vals[i] is not None:
                nodes.append({"id": len(nodes), "value": vals[i],
                              "left": None, "right": None})
                nodes[parent][side] = len(nodes) - 1
                queue.append(len(nodes) - 1)
            i += 1
    _layout(nodes, 0)
    return nodes


def snapshot(nodes):
    return [{"id": n["id"], "value": n["value"], "depth": n["depth"],
             "x": n["x"], "left": n["left"], "right": n["right"]}
            for n in nodes]


class Stepper:
    """Collects tree steps: current (orange), marked (green) and any extras."""

    def __init__(self, nodes):
        self.nodes = nodes
        self.steps: list = []
        self.counts: dict = {}

    def add(self, note, current=None, marked=(), found=None, **extra):
        st = {"tree": snapshot(self.nodes), "current": current,
              "marked": list(marked), "counts": dict(self.counts)}
        if found is not None:
            st["found"] = found
        st.update(extra)
        self.steps.append({"i": len(self.steps), "line": 0, "structures": st,
                           "highlight": {"index": current}, "note": note})


def val(nodes, nid):
    return nodes[nid]["value"]


def kids(nodes, nid):
    return [c for c in (nodes[nid]["left"], nodes[nid]["right"]) if c is not None]


def split_query(text):
    """'tree | a b' → (tree_text, [a, b]) for tracers that need extra numbers."""
    if "|" not in (text or ""):
        return text, []
    tree, rest = text.split("|", 1)
    try:
        extra = [int(t) for t in rest.replace(",", " ").split()]
    except ValueError:
        raise ValueError("After '|', give whole numbers only.") from None
    return tree, extra


def result(algo, steps, res, **meta):
    return {"meta": {"algorithm": algo, "view": "tree", "language": "python",
                     "result": res, **meta},
            "steps": steps}
