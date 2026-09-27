"""Range-query structures (batch 74) on the `grid` view. Input: an array,
then '|' and a script of operations.

* sparse_table — row k holds min(a[i .. i + 2^k − 1]); a query [l, r] is
  the min of two overlapping power-of-two blocks. O(n log n) build, O(1)
  per query (static array only).
* sqrt_decomposition — cut the array into blocks of ⌈√n⌉ and keep each
  block's sum: a range sum reads partial blocks cell by cell and whole
  blocks by their sum; a point update fixes one cell and one block sum.
* lazy_segment_tree — range add + range sum. A node fully inside an update
  takes the change and remembers it as `lazy` instead of touching its
  children; the debt is pushed down only when a later operation needs to go
  deeper.
"""

import math

from app.tracers.grid_common import Grid

TITLES = {
    "sparse_table": "Sparse Table (Range Minimum Query)",
    "sqrt_decomposition": "Sqrt Decomposition (Range Sum)",
    "lazy_segment_tree": "Segment Tree With Lazy Propagation",
}
OPS = {"sparse_table": {"min": 2},
       "sqrt_decomposition": {"sum": 2, "set": 2},
       "lazy_segment_tree": {"sum": 2, "add": 3}}


def run(algo, text, target=None):
    if "|" not in (text or ""):
        raise ValueError("Give 'array | operations', e.g. 5,2,4,7,1,3 | min 1 4, min 0 5.")
    arr_t, ops_t = text.split("|", 1)
    try:
        a = [int(t) for t in arr_t.replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("The array holds whole numbers, separated by commas.") from None
    if not (1 <= len(a) <= 8) or any(abs(v) > 99 for v in a):
        raise ValueError("Give 1–8 numbers within ±99.")
    usage = ", ".join(f"{k} " + " ".join("x" * v) for k, v in OPS[algo].items())
    ops = []
    for part in [p.strip() for p in ops_t.split(",") if p.strip()]:
        w = part.lower().split()
        want = OPS[algo].get(w[0])
        try:
            nums = [int(x) for x in w[1:]]
        except ValueError:
            nums = None
        if want is None or nums is None or len(nums) != want:
            raise ValueError(f"Operations: {usage}.")
        if w[0] in ("min", "sum", "add") and not (0 <= nums[0] <= nums[1] < len(a)):
            raise ValueError(f"'{part}': need 0 ≤ l ≤ r < {len(a)}.")
        if w[0] == "set" and not (0 <= nums[0] < len(a)):
            raise ValueError(f"'{part}': index out of range.")
        if any(abs(x) > 99 for x in nums):
            raise ValueError("Values within ±99.")
        ops.append((w[0], nums))
    if not (1 <= len(ops) <= 6):
        raise ValueError("Give 1–6 operations separated by commas.")
    return {"sparse_table": _sparse, "sqrt_decomposition": _sqrt,
            "lazy_segment_tree": _lazy}[algo](a, ops)


def _sparse(a, ops):
    n = len(a)
    LOG = n.bit_length()
    G = Grid(LOG, n)
    G.counts = {"cells": 0, "queries": 0}
    table = [a[:]]
    G.grid[0] = a[:]
    G.add("Row k, column i = min of the 2^k values starting at i. Row 0 is the "
          "array itself.", 0, None, [], [(0, i) for i in range(n)])
    for k in range(1, LOG):
        half = 1 << (k - 1)
        row = [min(table[k - 1][i], table[k - 1][i + half])
               for i in range(n - (1 << k) + 1)]
        table.append(row)
        G.grid[k] = row + [None] * (n - len(row))
        G.counts["cells"] += len(row)
        G.add(f"Row {k}: each block of {1 << k} = min of two blocks of {half} from "
              f"row {k - 1}.", k, None, [(k - 1, i) for i in range(n)],
              [(k, i) for i in range(len(row))])
    out = []
    for _, (l, r) in ops:
        k = (r - l + 1).bit_length() - 1
        x, y = table[k][l], table[k][r - (1 << k) + 1]
        out.append(min(x, y))
        G.counts["queries"] += 1
        G.add(f"min[{l}, {r}]: length {r - l + 1} → k = {k}. Two blocks of {1 << k} "
              f"(from {l} and from {r - (1 << k) + 1}) cover it; overlapping is "
              f"harmless for min: min({x}, {y}) = {out[-1]}.", k, l,
              [(0, i) for i in range(l, r + 1)], [(k, l), (k, r - (1 << k) + 1)])
    G.add(f"Answers: {out}.")
    return G.result("sparse_table", out, [f"2^{k}" for k in range(LOG)])


def _sqrt(a, ops):
    arr = a[:]
    n = len(arr)
    B = math.isqrt(n - 1) + 1 if n > 1 else 1        # ⌈√n⌉
    nb = (n + B - 1) // B
    sums = [sum(arr[b * B:(b + 1) * B]) for b in range(nb)]
    G = Grid(2, n)
    G.counts = {"cells_read": 0, "blocks_read": 0}

    def draw():
        G.grid[0] = arr[:]
        G.grid[1] = [sums[i // B] if i % B == 0 else None for i in range(n)]

    draw()
    G.add(f"Blocks of {B} (≈ √{n}). Row 1 holds each block's sum under its first "
          f"cell. A range sum = partial blocks cell by cell + whole blocks by sum.",
          None, None, [(1, b * B) for b in range(nb)])
    out = []
    for name, nums in ops:
        if name == "set":
            i, v = nums
            sums[i // B] += v - arr[i]
            arr[i] = v
            draw()
            G.add(f"set a[{i}] = {v}: fix the cell and its block sum (block {i // B}).",
                  0, i, [(1, (i // B) * B)])
            continue
        l, r = nums
        total, cells, blocks, i = 0, [], [], l
        while i <= r:
            if i % B == 0 and i + B - 1 <= r:
                total += sums[i // B]
                blocks.append((1, i))
                G.counts["blocks_read"] += 1
                i += B
            else:
                total += arr[i]
                cells.append((0, i))
                G.counts["cells_read"] += 1
                i += 1
        out.append(total)
        G.add(f"sum[{l}, {r}] = {total}: {len(cells)} single cell(s) + {len(blocks)} "
              f"whole block(s).", None, None, [(0, j) for j in range(l, r + 1)],
              cells + blocks)
    G.add(f"Answers: {out}.")
    return G.result("sqrt_decomposition", out, ["array", "block sums"])


def _lazy(a, ops):
    n = len(a)
    tree, lazy, rng, used = {}, {}, {}, []

    def build(node, lo, hi):
        rng[node] = (lo, hi)
        lazy[node] = 0
        used.append(node)
        if lo == hi:
            tree[node] = a[lo]
            return
        mid = (lo + hi) // 2
        build(2 * node, lo, mid)
        build(2 * node + 1, mid + 1, hi)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    build(1, 0, n - 1)
    used.sort()
    col = {node: c for c, node in enumerate(used)}
    G = Grid(3, len(used))
    G.counts = {"nodes_visited": 0, "pushdowns": 0}

    def draw():
        G.grid = [[f"{rng[x][0]}-{rng[x][1]}" for x in used],
                  [tree[x] for x in used], [lazy[x] or None for x in used]]

    draw()
    G.add("Each column is a tree node: its range, its sum, and any pending "
          "'lazy' add its children haven't received yet.", None, None, [],
          [(1, c) for c in range(len(used))])

    def push(node):
        if lazy[node] and 2 * node in rng:
            for ch in (2 * node, 2 * node + 1):
                lo, hi = rng[ch]
                tree[ch] += lazy[node] * (hi - lo + 1)
                if lo != hi:
                    lazy[ch] += lazy[node]
            G.counts["pushdowns"] += 1
            pending = lazy[node]
            lazy[node] = 0
            draw()
            G.add(f"Push node {rng[node][0]}-{rng[node][1]}'s pending +{pending} "
                  f"down to its children before going deeper.", 2, col[node],
                  [(1, col[2 * node]), (1, col[2 * node + 1])])

    def update(node, l, r, v):
        lo, hi = rng[node]
        G.counts["nodes_visited"] += 1
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            tree[node] += v * (hi - lo + 1)
            if lo != hi:
                lazy[node] += v
            draw()
            G.add(f"Node {lo}-{hi} lies inside [{l}, {r}]: sum += {v} × "
                  f"{hi - lo + 1}" + ("; record lazy +" + str(v) + " and stop here."
                                      if lo != hi else "."), 1, col[node])
            return
        push(node)
        update(2 * node, l, r, v)
        update(2 * node + 1, l, r, v)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
        draw()
        G.add(f"Node {lo}-{hi} partly overlaps: recompute sum = {tree[node]}.", 1,
              col[node], [(1, col[2 * node]), (1, col[2 * node + 1])])

    def query(node, l, r, hits):
        lo, hi = rng[node]
        G.counts["nodes_visited"] += 1
        if r < lo or hi < l:
            return 0
        if l <= lo and hi <= r:
            hits.append((1, col[node]))
            return tree[node]
        push(node)
        return query(2 * node, l, r, hits) + query(2 * node + 1, l, r, hits)

    out = []
    for name, nums in ops:
        if name == "add":
            l, r, v = nums
            G.add(f"add {v} to [{l}, {r}].")
            update(1, l, r, v)
        else:
            l, r = nums
            hits = []
            out.append(query(1, l, r, hits))
            G.add(f"sum[{l}, {r}] = {out[-1]}: the {len(hits)} node(s) that fit "
                  f"inside the range add up to it.", None, None, [], hits)
    G.add(f"Answers: {out}.")
    return G.result("lazy_segment_tree", out, ["range", "sum", "lazy"],
                    [str(x) for x in used])
