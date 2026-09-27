"""Fenwick-tree tricks and 2-D prefix sums (batch 84) on the `grid` view.

* bit_kth — a Fenwick tree over VALUES (1..16) counts how many of each
  value are present; the k-th smallest is found by binary lifting on the
  tree: try jumps of 8, 4, 2, 1 and take a jump whenever the count it skips
  is still below k. O(log n), no binary search on top.
* inversions_bit — scan from the right; before adding a[i], ask the tree
  how many smaller values are already to its right.
* prefix_sum_2d — P[r][c] = sum of the rectangle from (0,0) to (r−1,c−1);
  any rectangle's sum is P[r2+1][c2+1] − P[r1][c2+1] − P[r2+1][c1] + P[r1][c1]
  (inclusion–exclusion: add back the corner subtracted twice).
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "bit_kth": "K-th Smallest With a Fenwick Tree",
    "inversions_bit": "Count Inversions With a Fenwick Tree",
    "prefix_sum_2d": "2-D Prefix Sums (Rectangle Queries)",
}
N = 16


def run(algo, text, target=None):
    if algo == "inversions_bit":
        try:
            a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
        except ValueError:
            raise ValueError("Numbers only, separated by commas.") from None
        if not (1 <= len(a) <= 10) or any(not (1 <= v <= N) for v in a):
            raise ValueError(f"Give 1–10 values from 1 to {N}.")
        return _inversions(a)
    if algo == "prefix_sum_2d":
        if "|" not in (text or ""):
            raise ValueError("Give 'matrix | r1 c1 r2 c2, …', e.g. 1,2/3,4 | 0 0 1 1.")
        m_t, q_t = text.split("|", 1)
        g = parse_matrix(m_t, max_side=5)
        if any(abs(v) > 99 for r in g for v in r):
            raise ValueError("Cells within ±99.")
        qs = []
        for part in [p for p in q_t.split(",") if p.strip()]:
            try:
                r1, c1, r2, c2 = (int(x) for x in part.split())
            except ValueError:
                raise ValueError("Each query is 'r1 c1 r2 c2'.") from None
            if not (0 <= r1 <= r2 < len(g) and 0 <= c1 <= c2 < len(g[0])):
                raise ValueError(f"'{part.strip()}' is outside the matrix or reversed.")
            qs.append((r1, c1, r2, c2))
        if not (1 <= len(qs) <= 4):
            raise ValueError("Give 1–4 queries.")
        return _prefix2d(g, qs)
    ops = []
    for part in [p.strip() for p in (text or "").split(",") if p.strip()]:
        w = part.lower().split()
        try:
            name, x = w[0], int(w[1])
        except (IndexError, ValueError):
            raise ValueError("Operations look like 'add 5, add 2, kth 1, remove 5'.") from None
        if name not in ("add", "remove", "kth") or len(w) != 2:
            raise ValueError("Operations: add v, remove v, kth k.")
        if name != "kth" and not (1 <= x <= N):
            raise ValueError(f"Values are 1–{N}.")
        ops.append((name, x))
    if not (1 <= len(ops) <= 12):
        raise ValueError("Give 1–12 operations.")
    return _kth(ops)


def _lowbit(i):
    return i & -i


def _kth(ops):
    cnt, tree = [0] * (N + 1), [0] * (N + 1)
    G = Grid(2, N)
    G.grid = [cnt[1:], tree[1:]]
    G.counts = {"tree_steps": 0}
    out = []
    G.add(f"Row 0: how many copies of each value 1..{N}. Row 1: the Fenwick tree — "
          f"tree[i] sums the counts of a block ending at i whose length is the "
          f"lowest set bit of i.")

    def update(v, d):
        i, touched = v, []
        while i <= N:
            tree[i] += d
            touched.append((1, i - 1))
            G.counts["tree_steps"] += 1
            i += _lowbit(i)
        return touched

    for name, x in ops:
        if name in ("add", "remove"):
            if name == "remove" and cnt[x] == 0:
                G.add(f"remove {x}: there is no {x} to remove.", 0, x - 1, match=False)
                continue
            d = 1 if name == "add" else -1
            cnt[x] += d
            touched = update(x, d)
            G.grid = [cnt[1:], tree[1:]]
            G.add(f"{name} {x}: count[{x}] {'+' if d > 0 else '−'}1, and every tree "
                  f"node covering {x} changes (i += lowbit(i)).", 0, x - 1, touched)
            continue
        k, total = x, sum(cnt)
        if not (1 <= k <= total):
            out.append(None)
            G.add(f"kth {k}: only {total} value(s) stored.", match=False)
            continue
        pos, rem, jumps = 0, k, []
        step = 1 << (N.bit_length() - 1)
        while step:
            nxt = pos + step
            G.counts["tree_steps"] += 1
            if nxt <= N and tree[nxt] < rem:
                pos, rem = nxt, rem - tree[nxt]
                jumps.append((1, nxt - 1))
            step >>= 1
        out.append(pos + 1)
        G.add(f"kth {k}: binary lifting — jump by 16, 8, 4, 2, 1 whenever the block "
              f"skipped holds fewer than the remaining k. Landed after {pos}, so the "
              f"{k}-th smallest is {pos + 1}.", 0, pos, jumps, [(0, pos)])
    G.add(f"kth answers: {out}.")
    return G.result("bit_kth", out, ["count", "tree"], [str(i) for i in range(1, N + 1)])


def _inversions(a):
    tree, seen = [0] * (N + 1), [0] * (N + 1)
    G = Grid(2, N)
    G.grid = [[None] * N, tree[1:]]
    G.counts = {"inversions": 0}
    G.add(f"Scan {a} from the RIGHT. Before inserting a value v, the tree answers "
          f"'how many values already inserted (to its right) are smaller than v?' — "
          f"each is one inversion.")
    for i in range(len(a) - 1, -1, -1):
        v = a[i]
        q, j, cells = 0, v - 1, []
        while j > 0:
            q += tree[j]
            cells.append((1, j - 1))
            j -= _lowbit(j)
        G.counts["inversions"] += q
        j = v
        while j <= N:
            tree[j] += 1
            j += _lowbit(j)
        seen[v] += 1
        G.grid = [[seen[k] or None for k in range(1, N + 1)], tree[1:]]
        G.add(f"a[{i}] = {v}: prefix sum over 1..{v - 1} = {q} smaller value(s) to its "
              f"right. Total {G.counts['inversions']}. Then insert {v}.", 0, v - 1, cells)
    G.add(f"{G.counts['inversions']} inversion(s).")
    return G.result("inversions_bit", G.counts["inversions"], ["seen", "tree"],
                    [str(i) for i in range(1, N + 1)])


def _prefix2d(g, qs):
    R, C = len(g), len(g[0])
    P = [[0] * (C + 1) for _ in range(R + 1)]
    G = Grid(R + 1, C + 1)
    G.grid = [row[:] for row in P]
    G.counts = {"cells": 0}
    G.add("P has an extra zero row and column. P[r][c] = sum of everything above "
          "and left of (r, c) = g[r−1][c−1] + P[r−1][c] + P[r][c−1] − P[r−1][c−1].")
    for r in range(1, R + 1):
        for c in range(1, C + 1):
            P[r][c] = g[r - 1][c - 1] + P[r - 1][c] + P[r][c - 1] - P[r - 1][c - 1]
            G.counts["cells"] += 1
        G.grid = [row[:] for row in P]
        G.add(f"Row {r} of P filled.", r, None, [(r - 1, c) for c in range(C + 1)])
    out = []
    for r1, c1, r2, c2 in qs:
        a, b, c, d = P[r2 + 1][c2 + 1], P[r1][c2 + 1], P[r2 + 1][c1], P[r1][c1]
        s = a - b - c + d
        out.append(s)
        G.add(f"Rectangle ({r1},{c1})–({r2},{c2}): {a} − {b} − {c} + {d} = {s}. Four "
              f"lookups, whatever its size.", r2 + 1, c2 + 1,
              [(r1, c2 + 1), (r2 + 1, c1), (r1, c1)], [(r2 + 1, c2 + 1)])
    G.add(f"Answers: {out}.")
    return G.result("prefix_sum_2d", out, [str(r) for r in range(R + 1)],
                    [str(c) for c in range(C + 1)])
