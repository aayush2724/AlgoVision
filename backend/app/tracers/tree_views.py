"""What you see of a binary tree from different sides — all breadth-first.

* right_view — the last node of each level (the first node of each level is
  the left view; both are reported).
* top_view / bottom_view — give each node a horizontal distance (root 0, left
  −1, right +1). Top view keeps the first node seen at each distance in BFS
  order; bottom view keeps overwriting, so the last one wins.
* vertical_order — every node grouped by horizontal distance, top to bottom
  (ties at the same depth sorted by value).
* boundary_traversal — anticlockwise: root, the left edge (no leaves), every
  leaf left to right, then the right edge bottom-up (no leaves).
* max_width — number every slot in the level as if the tree were complete
  (left child 2i, right child 2i+1); width = last − first + 1.

Uses the `tree` view via bt_common: the node being looked at is orange, the
nodes that make it into the answer are green.
"""

from collections import deque

from app.tracers import bt_common as bt

TITLES = {
    "right_view": "Right / Left View of a Binary Tree",
    "top_view": "Top View of a Binary Tree",
    "bottom_view": "Bottom View of a Binary Tree",
    "vertical_order": "Vertical Order Traversal",
    "boundary_traversal": "Boundary Traversal",
    "max_width": "Maximum Width of a Binary Tree",
}


def run(algo, text, target=None):
    return trace(algo, bt.build(bt.parse(text)))


def trace(algo, nodes):
    s = bt.Stepper(nodes)
    s.counts = {"visits": 0}
    V = lambda i: bt.val(nodes, i)
    meta = {}

    if algo == "right_view":
        right, left, chosen = [], [], []
        q, level = deque([0]), 0
        s.add("Sweep level by level. The last node of each level is what you "
              "see from the right; the first is what you see from the left.")
        while q:
            ids = list(q)
            q.clear()
            for n in ids:
                s.counts["visits"] += 1
                q.extend(bt.kids(nodes, n))
            right.append(V(ids[-1]))
            left.append(V(ids[0]))
            chosen.append(ids[-1])
            s.add(f"Level {level}: {[V(n) for n in ids]} — rightmost {V(ids[-1])}, "
                  f"leftmost {V(ids[0])}.", ids[-1], chosen)
            level += 1
        res, meta["left"] = right, left
        s.add(f"Right view {right}; left view {left}.", None, chosen)
    elif algo in ("top_view", "bottom_view"):
        top = algo == "top_view"
        seen: dict = {}
        q = deque([(0, 0)])
        s.add("Give every node a horizontal distance: root 0, one left −1, one "
              "right +1. " + ("The first node met at each distance (in BFS "
                              "order) is visible from above." if top else
                              "The last node met at each distance is visible "
                              "from below — later levels overwrite earlier ones."))
        while q:
            n, hd = q.popleft()
            s.counts["visits"] += 1
            if top and hd in seen:
                s.add(f"{V(n)} at distance {hd} is hidden behind {V(seen[hd])}.",
                      n, sorted(seen.values()))
            else:
                prev = seen.get(hd)
                seen[hd] = n
                s.add(f"{V(n)} at distance {hd} "
                      + ("is the first there — visible." if top or prev is None
                         else f"replaces {V(prev)} — it is lower."),
                      n, sorted(seen.values()))
            if nodes[n]["left"] is not None:
                q.append((nodes[n]["left"], hd - 1))
            if nodes[n]["right"] is not None:
                q.append((nodes[n]["right"], hd + 1))
        res = [V(seen[h]) for h in sorted(seen)]
        s.add(f"{'Top' if top else 'Bottom'} view, left to right: {res}.",
              None, sorted(seen.values()))
    elif algo == "vertical_order":
        cols: dict = {}
        q = deque([(0, 0, 0)])
        s.add("Tag each node with (horizontal distance, depth). Columns are read "
              "left to right, each top to bottom; same spot → smaller value first.")
        while q:
            n, hd, d = q.popleft()
            s.counts["visits"] += 1
            cols.setdefault(hd, []).append((d, V(n), n))
            s.add(f"{V(n)} goes to column {hd} at depth {d}.", n,
                  [x[2] for x in cols[hd]])
            if nodes[n]["left"] is not None:
                q.append((nodes[n]["left"], hd - 1, d + 1))
            if nodes[n]["right"] is not None:
                q.append((nodes[n]["right"], hd + 1, d + 1))
        res = [[v for _, v, _ in sorted(cols[h])] for h in sorted(cols)]
        s.add(f"Vertical order: {res}.", None, list(range(len(nodes))))
    elif algo == "boundary_traversal":
        is_leaf = lambda n: not bt.kids(nodes, n)
        order: list = []
        chosen: list = []

        def take(n, why):
            order.append(V(n))
            chosen.append(n)
            s.counts["visits"] += 1
            s.add(f"{why}: {V(n)}. Boundary so far {order}.", n, chosen)

        s.add("Anticlockwise boundary: root, left edge (skip leaves), every leaf "
              "left to right, right edge bottom-up (skip leaves).")
        if not is_leaf(0):
            take(0, "Root")
        n = nodes[0]["left"]
        while n is not None:
            if not is_leaf(n):
                take(n, "Left edge")
            n = nodes[n]["left"] if nodes[n]["left"] is not None else nodes[n]["right"]

        def leaves(n):
            if is_leaf(n):
                take(n, "Leaf")
                return
            for c in bt.kids(nodes, n):
                leaves(c)
        leaves(0)
        right_edge = []
        n = nodes[0]["right"]
        while n is not None:
            if not is_leaf(n):
                right_edge.append(n)
            n = nodes[n]["right"] if nodes[n]["right"] is not None else nodes[n]["left"]
        for n in reversed(right_edge):
            take(n, "Right edge, bottom-up")
        res = order
        s.add(f"Boundary: {res}.", None, chosen)
    else:
        best, best_level = 0, 0
        q, level = deque([(0, 0)]), 0
        s.add("Number slots as in a complete tree — left child 2i, right child "
              "2i+1 — so gaps count. Width of a level = last − first + 1.")
        while q:
            items = list(q)
            q.clear()
            base = items[0][1]
            for n, i in items:
                s.counts["visits"] += 1
                i -= base          # re-base each level so numbers stay small
                if nodes[n]["left"] is not None:
                    q.append((nodes[n]["left"], 2 * i))
                if nodes[n]["right"] is not None:
                    q.append((nodes[n]["right"], 2 * i + 1))
            width = items[-1][1] - base + 1
            if width > best:
                best, best_level = width, level
            s.add(f"Level {level}: slots 0..{items[-1][1] - base} → width "
                  f"{width}. Widest so far {best} (level {best_level}).",
                  items[-1][0], [n for n, _ in items])
            level += 1
        res = best
        s.add(f"Maximum width: {best}, at level {best_level}.")
    return bt.result(algo, s.steps, res, **meta)
