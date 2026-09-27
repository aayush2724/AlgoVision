"""Binary search tree operations (Step 14) — each one steers by the BST rule
(smaller left, bigger right) instead of visiting the whole tree.

Built by inserting values in order ("8,3,10,1,6 | x"):
* floor_ceil_bst — walk down once for the floor (largest ≤ x), once for the
  ceil (smallest ≥ x), remembering the best candidate on the way.
* kth_bst — inorder visits values in sorted order: the kth visited is the kth
  smallest; the kth largest is the (n−k+1)th smallest.
* lca_bst — both values smaller → go left, both bigger → go right; the first
  node where they split (or that equals one) is the lowest common ancestor.
* successor_predecessor — the smallest value > x and the largest value < x.
* two_sum_bst — inorder gives a sorted list; two pointers from both ends.
* bst_from_preorder — rebuild the tree from a preorder listing; each value is
  placed by walking down from the root.

Given as an arbitrary shape (level order, "5,3,8,null,4"):
* validate_bst — every node must fit the (low, high) window its ancestors set.
* recover_bst — inorder should be increasing; the two out-of-place values are
  the swapped pair.
* largest_bst — bottom-up, each subtree reports (is BST, size, min, max).

Uses the `tree` view via bt_common: the node being examined is orange; the
walked path / chosen nodes are green.
"""

from app.tracers import bt_common as bt
from app.tracers.tree_traversal import _build, _layout

TITLES = {
    "floor_ceil_bst": "Floor and Ceil in a BST",
    "kth_bst": "Kth Smallest and Largest in a BST",
    "lca_bst": "LCA in a BST",
    "successor_predecessor": "Inorder Successor / Predecessor in a BST",
    "two_sum_bst": "Two Sum in a BST",
    "bst_from_preorder": "Construct a BST From Preorder",
    "validate_bst": "Check if a Tree is a BST",
    "recover_bst": "Recover a BST With Two Swapped Nodes",
    "largest_bst": "Largest BST in a Binary Tree",
}
SHAPE = {"validate_bst", "recover_bst", "largest_bst"}
EXTRA = {"floor_ceil_bst": 1, "kth_bst": 1, "lca_bst": 2,
         "successor_predecessor": 1, "two_sum_bst": 1}


def run(algo, text, target=None):
    tree_text, extra = bt.split_query(text)
    if algo in SHAPE:
        if extra:
            raise ValueError("This one takes only the tree (level order).")
        return trace(algo, bt.build(bt.parse(tree_text)), [])
    try:
        vals = [int(t) for t in tree_text.replace(" ", "").split(",") if t]
    except ValueError:
        raise ValueError("Give the values as numbers, e.g. 8,3,10,1,6 | 5.") from None
    if not (1 <= len(vals) <= bt.MAX_NODES) or any(abs(v) > 999 for v in vals):
        raise ValueError(f"Give 1–{bt.MAX_NODES} values within ±999.")
    if len(set(vals)) != len(vals):
        raise ValueError("BST values must be distinct.")
    need = EXTRA.get(algo, 0)
    if len(extra) != need:
        raise ValueError({1: "Add '| x' after the values, e.g. '8,3,10 | 5'.",
                          2: "Add '| a b' after the values, e.g. '8,3,10 | 3 10'.",
                          0: "This one takes only the values."}[need])
    if algo == "kth_bst" and not (1 <= extra[0] <= len(vals)):
        raise ValueError(f"k must be 1–{len(vals)}.")
    if algo == "lca_bst" and any(v not in vals for v in extra):
        raise ValueError("Both values must be in the tree.")
    if algo == "bst_from_preorder":
        return _from_preorder(vals)
    nodes, root = _build(vals)
    _layout(nodes, root)
    return trace(algo, nodes, extra)


def _inorder(nodes):
    order, stack, cur = [], [], 0
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = nodes[cur]["left"]
        cur = stack.pop()
        order.append(cur)
        cur = nodes[cur]["right"]
    return order


def trace(algo, nodes, extra):
    s = bt.Stepper(nodes)
    s.counts = {"visits": 0}
    V = lambda i: nodes[i]["value"]
    L = lambda i: nodes[i]["left"]
    R = lambda i: nodes[i]["right"]

    def walk(x, keep, label):
        """Descend from the root, recording the best candidate per `keep`."""
        cur, best, path = 0, None, []
        while cur is not None:
            s.counts["visits"] += 1
            path.append(cur)
            v = V(cur)
            if v == x and label in ("floor", "ceil"):
                best = cur
                s.add(f"{label.capitalize()}: {v} equals {x} — that's it.", cur, path)
                break
            if keep(v):
                best = cur
            go_right = v < x if label in ("floor", "predecessor") else v <= x
            s.add(f"{label.capitalize()}: at {v}. "
                  + (f"{v} is a candidate; " if keep(v) else "")
                  + f"go {'right' if go_right else 'left'}.", cur, path)
            cur = R(cur) if go_right else L(cur)
        return None if best is None else V(best)

    if algo == "floor_ceil_bst":
        x = extra[0]
        s.add(f"Floor = largest value ≤ {x}; ceil = smallest value ≥ {x}. Each is "
              f"one walk down, keeping the best candidate seen.")
        res = [walk(x, lambda v: v <= x, "floor"), walk(x, lambda v: v >= x, "ceil")]
        s.add(f"Floor {res[0] if res[0] is not None else 'none'}, ceil "
              f"{res[1] if res[1] is not None else 'none'} — O(height), not O(n).")
    elif algo == "successor_predecessor":
        x = extra[0]
        s.add(f"Successor = smallest value > {x}; predecessor = largest value "
              f"< {x}. One walk each.")
        succ = walk(x, lambda v: v > x, "successor")
        pred = walk(x, lambda v: v < x, "predecessor")
        res = [pred, succ]
        s.add(f"Predecessor {pred if pred is not None else 'none'}, successor "
              f"{succ if succ is not None else 'none'}.")
    elif algo == "kth_bst":
        k = extra[0]
        order = _inorder(nodes)
        s.add("Inorder visits a BST in sorted order, so count visits: the kth "
              "visit is the kth smallest.")
        for i, nid in enumerate(order):
            s.counts["visits"] += 1
            s.add(f"Visit #{i + 1}: {V(nid)}.", nid, order[:i + 1])
        n = len(order)
        res = [V(order[k - 1]), V(order[n - k])]
        s.add(f"{k}th smallest = {res[0]}; {k}th largest = the {n - k + 1}th "
              f"smallest = {res[1]}.", order[k - 1], [order[k - 1], order[n - k]])
    elif algo == "lca_bst":
        a, b = extra
        cur, path = 0, []
        s.add(f"Find the lowest common ancestor of {a} and {b}: while both are on "
              f"the same side, go that way.")
        while True:
            s.counts["visits"] += 1
            path.append(cur)
            v = V(cur)
            if a < v and b < v:
                s.add(f"{a} and {b} are both smaller than {v} — go left.", cur, path)
                cur = L(cur)
            elif a > v and b > v:
                s.add(f"{a} and {b} are both bigger than {v} — go right.", cur, path)
                cur = R(cur)
            else:
                s.add(f"At {v} the two values split (or one of them is {v}) — "
                      f"{v} is the LCA.", cur, path, found=True)
                res = v
                break
    elif algo == "two_sum_bst":
        k = extra[0]
        order = _inorder(nodes)
        s.add(f"Inorder gives the values sorted: {[V(i) for i in order]}. Two "
              f"pointers from both ends look for a pair summing to {k}.")
        i, j, res = 0, len(order) - 1, False
        while i < j:
            s.counts["visits"] += 1
            total = V(order[i]) + V(order[j])
            pair = [order[i], order[j]]
            if total == k:
                res = True
                s.add(f"{V(order[i])} + {V(order[j])} = {k} — found.", order[i],
                      pair, found=True)
                break
            if total < k:
                s.add(f"{V(order[i])} + {V(order[j])} = {total} < {k} — move the "
                      f"left pointer up.", order[i], pair)
                i += 1
            else:
                s.add(f"{V(order[i])} + {V(order[j])} = {total} > {k} — move the "
                      f"right pointer down.", order[j], pair)
                j -= 1
        if not res:
            s.add(f"The pointers met — no pair sums to {k}.", found=False)
    elif algo == "validate_bst":
        ok_nodes: list = []
        s.add("A BST isn't just 'left child smaller, right child bigger': every "
              "node must fit the (low, high) window set by ALL its ancestors.")

        def check(n, lo, hi):
            if n is None:
                return True
            s.counts["visits"] += 1
            v = V(n)
            win = f"({'−∞' if lo is None else lo}, {'∞' if hi is None else hi})"
            if (lo is not None and v <= lo) or (hi is not None and v >= hi):
                s.add(f"{v} is outside its window {win} — not a BST.", n, ok_nodes,
                      found=False)
                return False
            ok_nodes.append(n)
            s.add(f"{v} fits its window {win}.", n, ok_nodes)
            return check(L(n), lo, v) and check(R(n), v, hi)
        res = check(0, None, None)
        s.add("It is a valid BST." if res else "Not a BST.", None, ok_nodes, found=res)
    elif algo == "recover_bst":
        order = _inorder(nodes)
        s.add(f"Inorder should be increasing: {[V(i) for i in order]}. Find where "
              f"it drops.")
        first = second = None
        for a, b in zip(order, order[1:]):
            s.counts["visits"] += 1
            if V(a) > V(b):
                if first is None:
                    first = a
                second = b
                s.add(f"Drop: {V(a)} > {V(b)}.", b,
                      [x for x in (first, second) if x is not None])
        if first is None:
            res = None
            s.add("Inorder is already increasing — nothing was swapped.")
        else:
            nodes[first]["value"], nodes[second]["value"] = V(second), V(first)
            res = sorted([V(first), V(second)])
            s.add(f"Swap back the first bad value and the last one: {res[0]} ↔ "
                  f"{res[1]}. Inorder is increasing again.", None, [first, second],
                  found=True)
    else:  # largest_bst
        best = {"size": 0, "root": None}
        good: list = []
        s.add("Bottom-up, every subtree reports: is it a BST, its size, its min "
              "and max. A node joins its children when left max < value < right "
              "min.")

        def post(n):
            if n is None:
                return True, 0, None, None
            s.counts["visits"] += 1
            lb, ls, lmin, lmax = post(L(n))
            rb, rs, rmin, rmax = post(R(n))
            v = V(n)
            if lb and rb and (lmax is None or lmax < v) and (rmin is None or v < rmin):
                size = ls + rs + 1
                if size > best["size"]:
                    best.update(size=size, root=n)
                good.append(n)
                s.add(f"Subtree at {v} is a BST of size {size}.", n, good)
                return (True, size, lmin if lmin is not None else v,
                        rmax if rmax is not None else v)
            s.add(f"Subtree at {v} is not a BST.", n, good)
            return False, 0, None, None
        post(0)
        res = best["size"]
        s.add(f"Largest BST: {res} node(s), rooted at {V(best['root'])}.",
              best["root"], good)
    return bt.result(algo, s.steps, res)


def _from_preorder(vals):
    nodes: list = []
    s = bt.Stepper(nodes)
    s.counts = {"placed": 0}
    s.add(f"Preorder is root, left subtree, right subtree: {vals}. Place each "
          f"value by walking down from the root, like an insertion.")
    for v in vals:
        parent, side = None, None
        if nodes:
            cur = 0
            while True:
                side = "left" if v < nodes[cur]["value"] else "right"
                if nodes[cur][side] is None:
                    parent = cur
                    break
                cur = nodes[cur][side]
        nodes.append({"id": len(nodes), "value": v, "left": None, "right": None})
        if parent is not None:
            nodes[parent][side] = len(nodes) - 1
        _layout(nodes, 0)
        s.counts["placed"] += 1
        where = ("the root" if parent is None
                 else f"the {side} child of {nodes[parent]['value']}")
        s.add(f"{v} becomes {where}.", len(nodes) - 1, list(range(len(nodes))))
    s.add("Every value placed — the BST whose preorder is exactly the input.",
          None, list(range(len(nodes))))
    return bt.result("bst_from_preorder", s.steps, [n["value"] for n in nodes])
