"""Advanced DP patterns (batch 83).

* digit_dp (grid) — count x in [0, N] with digit sum S. ways[k][s] = number
  of k-digit strings (leading zeros allowed) with digit sum s. Walk N's
  digits from the left staying "tight": at each position, every smaller
  digit d frees the rest, contributing ways[remaining][S − sum − d].
* tree_robber (tree) — house robber on a tree: for each node keep (take,
  skip): take = v + skip(children), skip = Σ max(take, skip) of children.
* sos_dp (grid) — sum over subsets: F[mask] = Σ a[sub] for sub ⊆ mask. Add
  one bit at a time: after bit i, F[mask] also includes subsets that differ
  from mask in bit i. O(n·2ⁿ) instead of O(3ⁿ).
* sum_distances_tree (tree) — rerooting: one DFS gets subtree sizes and the
  root's answer; moving the root from p to child c brings size[c] nodes one
  step closer and the other n − size[c] one step farther.
"""

from app.tracers import bt_common as bt
from app.tracers.grid_common import Grid

TITLES = {
    "digit_dp": "Digit DP (Count Numbers With Digit Sum S)",
    "tree_robber": "House Robber on a Tree",
    "sos_dp": "Sum Over Subsets (SOS DP)",
    "sum_distances_tree": "Sum of Distances in a Tree (Rerooting)",
}


def run(algo, text, target=None):
    if algo == "digit_dp":
        try:
            n = int((text or "").strip())
        except ValueError:
            raise ValueError("Give N (0–99999).") from None
        if not (0 <= n <= 99999):
            raise ValueError("Give N (0–99999).")
        if target is None or target != int(target) or not (0 <= target <= 45):
            raise ValueError("S (the digit sum) must be 0–45.")
        return _digit(n, int(target))
    if algo == "sos_dp":
        try:
            a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
        except ValueError:
            raise ValueError("Numbers only, separated by commas.") from None
        if len(a) not in (2, 4, 8, 16) or any(abs(v) > 99 for v in a):
            raise ValueError("Give 2, 4, 8 or 16 values (one per mask) within ±99.")
        return _sos(a)
    vals = bt.parse(text)
    if algo == "tree_robber" and any(v is not None and not (0 <= v <= 99) for v in vals):
        raise ValueError("House values are 0–99.")
    return (_robber if algo == "tree_robber" else _reroot)(bt.build(vals))


def _digit(n, s):
    digits = [int(c) for c in str(n)]
    L = len(digits)
    ways = [[0] * (s + 1) for _ in range(L)]
    ways[0][0] = 1
    G = Grid(L, s + 1)
    G.counts = {"cells": 0, "count": 0}
    G.grid[0] = ways[0][:]
    G.add("ways[k][t] = how many k-digit strings (leading zeros allowed) have "
          "digit sum t. ways[0] is 1 for t = 0 only.", 0, 0)
    for k in range(1, L):
        for t in range(s + 1):
            ways[k][t] = sum(ways[k - 1][t - d] for d in range(10) if d <= t)
            G.counts["cells"] += 1
        G.grid[k] = ways[k][:]
        G.add(f"ways[{k}][t] = Σ over the first digit d of ways[{k - 1}][t − d].", k,
              None, [(k - 1, t) for t in range(s + 1)])
    total, so_far = 0, 0
    for i, top in enumerate(digits):
        left = L - 1 - i
        add, cells = 0, []
        for d in range(top):
            need = s - so_far - d
            if 0 <= need <= s:
                add += ways[left][need]
                cells.append((left, need))
        total += add
        G.counts["count"] = total
        G.add(f"Position {i} (N's digit {top}): choosing any smaller digit frees the "
              f"remaining {left} digit(s) — adds {add}. Stay tight with {top} "
              f"(sum so far {so_far + top}).", left, None, cells, cells)
        so_far += top
    if so_far == s:
        total += 1
        G.counts["count"] = total
        G.add(f"N itself ({n}) has digit sum {so_far} = {s} — count it too.")
    G.add(f"{total} number(s) in [0, {n}] have digit sum {s}.")
    return G.result("digit_dp", total, [f"{k} free" for k in range(L)],
                    [str(t) for t in range(s + 1)])


def _robber(nodes):
    for n in nodes:
        n["v"] = n["value"]
    S = bt.Stepper(nodes)
    S.counts = {"nodes_solved": 0}
    S.add("Rob houses on a tree without robbing two that are directly linked. "
          "Solve children first: take = value + (skip of each child); "
          "skip = Σ max(take, skip) of each child. Labels become v:take/skip.")
    done = []

    def solve(i):
        if i is None:
            return 0, 0
        lt, ls = solve(nodes[i]["left"])
        rt, rs = solve(nodes[i]["right"])
        take = nodes[i]["v"] + ls + rs
        skip = max(lt, ls) + max(rt, rs)
        nodes[i]["value"] = f"{nodes[i]['v']}:{take}/{skip}"
        done.append(i)
        S.counts["nodes_solved"] += 1
        S.add(f"Node {nodes[i]['v']}: take = {nodes[i]['v']} + {ls} + {rs} = {take}; "
              f"skip = {max(lt, ls)} + {max(rt, rs)} = {skip}.", i, done[:-1])
        return take, skip

    take, skip = solve(0)
    S.add(f"At the root: max(take {take}, skip {skip}) = {max(take, skip)}.", 0, done,
          found=True)
    return bt.result("tree_robber", S.steps, max(take, skip))


def _sos(a):
    n = len(a).bit_length() - 1
    size = len(a)
    F = a[:]
    G = Grid(size, n + 1)
    for m in range(size):
        G.grid[m][0] = a[m]
    G.counts = {"additions": 0}
    G.add("F[mask] should be the sum of a[sub] over every sub ⊆ mask. Column 0 "
          "is a itself; after processing bit i, F[mask] covers subsets that may "
          "differ from mask in bits 0..i.", None, 0, [], [(m, 0) for m in range(size)])
    for i in range(n):
        for m in range(size):
            if m >> i & 1:
                F[m] += F[m ^ 1 << i]
                G.counts["additions"] += 1
        for m in range(size):
            G.grid[m][i + 1] = F[m]
        G.add(f"Bit {i}: every mask with bit {i} set adds F[mask without bit {i}].",
              None, i + 1, [(m ^ 1 << i, i) for m in range(size) if m >> i & 1],
              [(m, i + 1) for m in range(size) if m >> i & 1])
    G.add(f"F = {F}.", path=[(m, n) for m in range(size)])
    return G.result("sos_dp", F, [format(m, f"0{n}b") for m in range(size)],
                    ["a"] + [f"bit {i}" for i in range(n)])


def _reroot(nodes):
    n = len(nodes)
    for x in nodes:
        x["v"] = x["value"]
    parent = [None] * n
    for x in nodes:
        for c in (x["left"], x["right"]):
            if c is not None:
                parent[c] = x["id"]
    kids = lambda i: [c for c in (nodes[i]["left"], nodes[i]["right"]) if c is not None]
    size, down, ans = [1] * n, [0] * n, [0] * n
    S = bt.Stepper(nodes)
    S.counts = {"passes": 0}
    S.add("Pass 1 (post-order): size[v] = nodes in v's subtree, down[v] = sum of "
          "distances from v to them. Labels show v:size.")
    order = []

    def post(i):
        for c in kids(i):
            post(c)
            size[i] += size[c]
            down[i] += down[c] + size[c]
        order.append(i)
        nodes[i]["value"] = f"{nodes[i]['v']}:{size[i]}"
        S.add(f"{nodes[i]['v']}: size {size[i]}, down {down[i]} (each child's distances "
              f"+ 1 per node in that child's subtree).", i, order[:-1])

    post(0)
    S.counts["passes"] = 1
    ans[0] = down[0]
    nodes[0]["value"] = f"{nodes[0]['v']}:Σ{ans[0]}"
    S.add(f"The root's answer is down[root] = {ans[0]}. Pass 2 (pre-order): moving "
          f"the root to child c, size[c] nodes get 1 closer and n − size[c] get 1 "
          f"farther: ans[c] = ans[p] − size[c] + ({n} − size[c]).", 0, [0])
    seen = [0]
    stack = kids(0)[::-1]
    while stack:
        c = stack.pop()
        p = parent[c]
        ans[c] = ans[p] - size[c] + (n - size[c])
        nodes[c]["value"] = f"{nodes[c]['v']}:Σ{ans[c]}"
        seen.append(c)
        S.add(f"{nodes[c]['v']}: {ans[p]} − {size[c]} + {n - size[c]} = {ans[c]}.", c,
              seen[:-1])
        stack += kids(c)[::-1]
    S.counts["passes"] = 2
    S.add("Every node's total distance, in O(n) overall.", None, list(range(n)))
    return bt.result("sum_distances_tree", S.steps, ans)
