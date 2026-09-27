"""Binary-tree properties computed on the way back up (or out) of a traversal.

* balanced_tree — postorder heights; a subtree reports −1 as soon as its two
  sides differ by more than 1, and that −1 short-circuits upward.
* symmetric_tree — compare mirror pairs: left.left with right.right, left.right
  with right.left.
* max_path_sum — at each node, the best downward gain is val + max(0, best
  child gain); a path *through* the node uses both sides.
* root_to_leaf_paths — DFS carrying the path; a leaf closes one path.
* children_sum — make every node equal the sum of its children using only
  increments: push a big parent value down, then pull sums back up.
* nodes_at_distance_k — record parents, then BFS outward from the target in
  all three directions (left, right, up) for k steps.
* burn_tree — the same outward BFS from a start node; the number of rounds is
  the time to burn everything.
* count_complete_nodes — in a complete tree, equal left/right edge heights
  mean a perfect subtree (2^h − 1 nodes) — no need to walk it.

Uses the `tree` view via bt_common: current node orange, confirmed nodes green.
Extra numbers come after a '|': "tree | target k" or "tree | start".
"""

from collections import deque

from app.tracers import bt_common as bt

TITLES = {
    "balanced_tree": "Check for a Balanced Binary Tree",
    "symmetric_tree": "Symmetric Binary Tree",
    "max_path_sum": "Maximum Path Sum",
    "root_to_leaf_paths": "Root-to-Leaf Paths",
    "children_sum": "Children Sum Property",
    "nodes_at_distance_k": "All Nodes at Distance K",
    "burn_tree": "Minimum Time to Burn a Binary Tree",
    "count_complete_nodes": "Count Nodes in a Complete Binary Tree",
}


def run(algo, text, target=None):
    tree_text, extra = bt.split_query(text)
    vals = bt.parse(tree_text)
    nodes = bt.build(vals)
    need = {"nodes_at_distance_k": 2, "burn_tree": 1}.get(algo, 0)
    if len(extra) != need:
        raise ValueError("Add '| target k' after the tree, e.g. '… | 5 2'."
                         if need == 2 else "Add '| start' after the tree, e.g. '… | 3'."
                         if need == 1 else "This one takes only the tree.")
    if need and not any(n["value"] == extra[0] for n in nodes):
        raise ValueError(f"{extra[0]} is not in the tree.")
    if algo == "nodes_at_distance_k" and not (0 <= extra[1] <= 10):
        raise ValueError("k must be 0–10.")
    if algo == "count_complete_nodes":
        # Complete: no value may follow the first gap in level order.
        seen_gap = False
        for v in vals:
            if v is None:
                seen_gap = True
            elif seen_gap:
                raise ValueError("Give a complete tree: every level full except "
                                 "the last, filled from the left.")
    return trace(algo, nodes, extra)


def trace(algo, nodes, extra=()):
    s = bt.Stepper(nodes)
    s.counts = {"visits": 0}
    V = lambda i: bt.val(nodes, i)
    L = lambda i: nodes[i]["left"]
    R = lambda i: nodes[i]["right"]

    if algo == "balanced_tree":
        ok_nodes: list = []
        s.add("Balanced: at every node the two subtree heights differ by at most "
              "1. Compute heights bottom-up; −1 means 'already unbalanced'.")

        def h(n):
            if n is None:
                return 0
            s.counts["visits"] += 1
            lh = h(L(n))
            if lh == -1:
                return -1
            rh = h(R(n))
            if rh == -1:
                return -1
            if abs(lh - rh) > 1:
                s.add(f"At {V(n)}: left height {lh}, right height {rh} — they "
                      f"differ by {abs(lh - rh)} > 1. Unbalanced; stop.", n,
                      ok_nodes, found=False)
                return -1
            ok_nodes.append(n)
            s.add(f"At {V(n)}: left height {lh}, right height {rh} — fine. Its "
                  f"height is {1 + max(lh, rh)}.", n, ok_nodes)
            return 1 + max(lh, rh)
        res = h(0) != -1
        s.add("Balanced." if res else "Not balanced.", None, ok_nodes, found=res)
    elif algo == "symmetric_tree":
        matched: list = []
        s.add("Symmetric means the tree mirrors itself: compare the left subtree "
              "with the right one, outer pairs with outer, inner with inner.")

        def mirror(a, b):
            if a is None or b is None:
                ok = a is None and b is None
                if not ok:
                    present = a if a is not None else b
                    s.add(f"{V(present)} has no mirror partner — not symmetric.",
                          present, matched, found=False)
                return ok
            s.counts["visits"] += 1
            if V(a) != V(b):
                s.add(f"Mirror pair {V(a)} vs {V(b)} differ — not symmetric.",
                      a, matched, found=False)
                return False
            matched.extend([a, b])
            s.add(f"Mirror pair {V(a)} and {V(b)} match. Now compare outer "
                  f"children, then inner.", a, matched)
            return mirror(L(a), R(b)) and mirror(R(a), L(b))
        res = mirror(L(0), R(0))
        if res:
            matched.append(0)
        s.add("Symmetric." if res else "Not symmetric.", None, matched, found=res)
    elif algo == "max_path_sum":
        best = {"v": None, "at": None}
        done: list = []
        s.add("A path may bend at one node. Bottom-up, each node reports its best "
              "downward gain (val + the better child, negatives dropped); the "
              "path through it adds both sides.")

        def gain(n):
            if n is None:
                return 0
            s.counts["visits"] += 1
            lg, rg = max(0, gain(L(n))), max(0, gain(R(n)))
            through = V(n) + lg + rg
            if best["v"] is None or through > best["v"]:
                best.update(v=through, at=n)
            done.append(n)
            s.add(f"At {V(n)}: best gains left {lg}, right {rg}; a path bending "
                  f"here sums {through}. Best so far {best['v']}. Report "
                  f"{V(n) + max(lg, rg)} upward.", n, done)
            return V(n) + max(lg, rg)
        gain(0)
        res = best["v"]
        s.add(f"Maximum path sum: {res} (bending at {V(best['at'])}).",
              best["at"], done)
    elif algo == "root_to_leaf_paths":
        paths: list = []
        path: list = []
        s.add("Depth-first, carrying the path from the root. Each leaf closes "
              "one path.")

        def dfs(n):
            s.counts["visits"] += 1
            path.append(n)
            trail = "→".join(str(V(p)) for p in path)
            if not bt.kids(nodes, n):
                paths.append([V(p) for p in path])
                s.add(f"Leaf {V(n)} — path {trail}.", n, list(path))
            else:
                s.add(f"At {V(n)}, path so far {trail}.", n, list(path))
                for c in bt.kids(nodes, n):
                    dfs(c)
            path.pop()
        dfs(0)
        res = paths
        s.add(f"{len(paths)} root-to-leaf path(s): "
              + "; ".join("→".join(map(str, p)) for p in paths) + ".")
    elif algo == "children_sum":
        done: list = []
        s.add("Goal: every node equals the sum of its children, changing values "
              "only by increasing them. Going down, if the children sum to less "
              "than the parent, lift them to the parent's value; coming back "
              "up, set the parent to the (now big enough) children's sum.")

        def fix(n):
            if n is None:
                return
            s.counts["visits"] += 1
            ks = bt.kids(nodes, n)
            child_sum = sum(V(c) for c in ks)
            if ks and child_sum < V(n):
                for c in ks:
                    nodes[c]["value"] = V(n)
                s.add(f"Children of {V(n)} sum to {child_sum} < {V(n)} — lift "
                      f"them to {V(n)} on the way down.", n, done)
            elif ks:
                nodes[n]["value"] = child_sum
                s.add(f"Children already sum to {child_sum} — raise this node "
                      f"to {child_sum}.", n, done)
            fix(L(n))
            fix(R(n))
            if ks:
                total = sum(V(c) for c in ks)
                nodes[n]["value"] = total
                s.add(f"Back up: set this node to its children's sum, {total}.",
                      n, done + [n])
            done.append(n)
        fix(0)
        res = [n["value"] for n in nodes]
        s.add("Every internal node now equals the sum of its children.", None, done)
    elif algo == "count_complete_nodes":
        s.counts = {"calls": 0}
        counted: list = []
        s.add("In a complete tree, if the leftmost and rightmost edges have the "
              "same height h, the subtree is perfect: 2^h − 1 nodes, no walking "
              "needed. Otherwise count the two children recursively.")

        def edge(n, side):
            h = 0
            while n is not None:
                h += 1
                n = nodes[n][side]
            return h

        def sub(n):
            out, stack = [], [n]
            while stack:
                m = stack.pop()
                out.append(m)
                stack.extend(bt.kids(nodes, m))
            return out

        def count(n):
            if n is None:
                return 0
            s.counts["calls"] += 1
            lh, rh = edge(n, "left"), edge(n, "right")
            if lh == rh:
                counted.extend(sub(n))
                s.add(f"At {V(n)}: left edge {lh} = right edge {rh} — perfect "
                      f"subtree, 2^{lh} − 1 = {2 ** lh - 1} nodes.", n, counted)
                return 2 ** lh - 1
            s.add(f"At {V(n)}: left edge {lh} ≠ right edge {rh} — count "
                  f"1 + left + right.", n, counted)
            total = 1 + count(L(n)) + count(R(n))
            counted.append(n)
            return total
        res = count(0)
        s.add(f"{res} nodes, from {s.counts['calls']} calls — O(log² n) instead "
              f"of visiting all of them.", None, counted)
    else:  # nodes_at_distance_k, burn_tree — outward BFS through parents too
        parent = {0: None}
        q = deque([0])
        while q:
            n = q.popleft()
            for c in bt.kids(nodes, n):
                parent[c] = n
                q.append(c)
        start = next(n["id"] for n in nodes if n["value"] == extra[0])
        k = extra[1] if algo == "nodes_at_distance_k" else None
        seen = {start}
        frontier = [start]
        rounds = 0
        s.add("Record every node's parent first, so the search can also move "
              "upward. Then spread from "
              + (f"{V(start)} one ring at a time, for {k} step(s)." if k is not None
                 else f"the fire at {V(start)} — each minute it reaches every "
                      f"neighbour (children and parent)."), start, [start])
        while frontier and (k is None or rounds < k):
            nxt = []
            for n in frontier:
                for m in (L(n), R(n), parent[n]):
                    if m is not None and m not in seen:
                        seen.add(m)
                        nxt.append(m)
                        s.counts["visits"] += 1
            if not nxt:
                break
            rounds += 1
            frontier = nxt
            s.add(f"{'Distance' if k is not None else 'Minute'} {rounds}: "
                  f"{sorted(V(n) for n in nxt)}.", nxt[0], sorted(seen))
        if k is not None:
            res = sorted(V(n) for n in frontier) if rounds == k else []
            s.add(f"Nodes exactly {k} away from {V(start)}: {res}.", None,
                  frontier if rounds == k else [])
        else:
            res = rounds
            s.add(f"Everything has burned after {rounds} minute(s).", None,
                  sorted(seen))
    return bt.result(algo, s.steps, res)
