"""Two more BST problems (Binary Search Trees), built by inserting the given
values in order, on the `tree` view.

* bst_min_max — the minimum is the leftmost node (keep going left), the
  maximum the rightmost. No searching: the BST rule points the way.
* bst_iterator — next() in O(1) amortised with O(h) memory: push the left
  spine onto a stack; pop gives the next value, then push the popped node's
  right child's left spine.
"""

from app.tracers import bt_common as bt
from app.tracers.tree_traversal import _build, _layout

TITLES = {
    "bst_min_max": "Minimum and Maximum in a BST",
    "bst_iterator": "BST Iterator (next / hasNext)",
}


def run(algo, text, target=None):
    tree_text, extra = bt.split_query(text)
    if extra:
        raise ValueError("This one takes only the values.")
    try:
        vals = [int(t) for t in tree_text.replace(" ", "").split(",") if t]
    except ValueError:
        raise ValueError("Give the values as numbers, e.g. 8,3,10,1,6.") from None
    if not (1 <= len(vals) <= bt.MAX_NODES) or any(abs(v) > 999 for v in vals):
        raise ValueError(f"Give 1–{bt.MAX_NODES} values within ±999.")
    if len(set(vals)) != len(vals):
        raise ValueError("BST values must be distinct.")
    nodes, root = _build(vals)
    _layout(nodes, root)
    return (_min_max if algo == "bst_min_max" else _iterator)(nodes, root)


def _min_max(nodes, root):
    s = bt.Stepper(nodes)
    s.counts = {"steps": 0}
    s.add("Smaller values live to the left, bigger to the right — so the minimum "
          "is as far left as you can go, the maximum as far right.", root)
    j, path = root, []
    while j is not None:
        path.append(j)
        s.counts["steps"] += 1
        nxt = nodes[j]["left"]
        s.add(f"At {bt.val(nodes, j)}: " + (f"there is a left child, go left." if nxt is not None
                                             else "no left child — this is the minimum."),
              j, path)
        j = nxt
    lo = path[-1]
    j, path2 = root, []
    while j is not None:
        path2.append(j)
        s.counts["steps"] += 1
        nxt = nodes[j]["right"]
        s.add(f"At {bt.val(nodes, j)}: " + (f"there is a right child, go right." if nxt is not None
                                             else "no right child — this is the maximum."),
              j, path + path2)
        j = nxt
    hi = path2[-1]
    s.add(f"min = {bt.val(nodes, lo)}, max = {bt.val(nodes, hi)}. O(height) each.",
          None, [lo, hi], found=True)
    return bt.result("bst_min_max", s.steps, [bt.val(nodes, lo), bt.val(nodes, hi)])


def _iterator(nodes, root):
    s = bt.Stepper(nodes)
    s.counts = {"pushes": 0, "pops": 0}
    stack: list = []
    out: list = []

    def push_left(j, why):
        nonlocal stack
        while j is not None:
            stack.append(j)
            s.counts["pushes"] += 1
            s.add(f"{why}push {bt.val(nodes, j)}; stack {[bt.val(nodes, k) for k in stack]}.",
                  j, out, stack=[bt.val(nodes, k) for k in stack])
            why = "Keep going left: "
            j = nodes[j]["left"]

    s.add("Constructor: push the whole left spine from the root. The stack top is "
          "the smallest value.", root)
    push_left(root, "Start: ")
    while stack:
        j = stack.pop()
        s.counts["pops"] += 1
        out.append(j)
        s.add(f"next() pops {bt.val(nodes, j)} → value #{len(out)} in order.", j, out,
              stack=[bt.val(nodes, k) for k in stack])
        if nodes[j]["right"] is not None:
            push_left(nodes[j]["right"], f"{bt.val(nodes, j)} has a right subtree — ")
        elif not stack:
            s.add("Stack empty — hasNext() is false.", None, out, stack=[])
    s.add(f"Visited in order: {[bt.val(nodes, k) for k in out]}. Memory O(height).",
          None, out, found=True)
    return bt.result("bst_iterator", s.steps, [bt.val(nodes, k) for k in out])
