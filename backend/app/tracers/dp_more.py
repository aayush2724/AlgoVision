"""More table DP (Step 16) — each cell is one small decision over earlier cells.

* frog_jump_k — dp[i] = min over j = 1..k of dp[i−j] + |h[i] − h[i−j]|.
* ninja_training — dp[day][task] = points[day][task] + best of the previous
  day's *other* tasks (no task two days running).
* min_falling_path — dp[r][c] = a[r][c] + min of the three cells above it.
* triangle_path — dp[r][c] = t[r][c] + min(dp[r−1][c−1], dp[r−1][c]); the
  answer is the smallest value in the last row.
* partition_equal_subset — the array splits into two equal halves exactly when
  some subset reaches total / 2 (an odd total never does).
* count_subsets_sum_k — dp[i][s] = ways to make s from the first i values:
  ways without the new value + ways that spend it.
* unbounded_knapsack / rod_cutting — like 0/1 knapsack, but taking an item
  looks left in the *same* row, because it may be taken again. Rod cutting is
  exactly that with piece lengths 1..n as weights.

Uses the `grid` view: the cell being filled is `row`/`col`, the cells it reads
are `deps`, and the optimal choices trace back green via `path`.
"""

TITLES = {
    "frog_jump_k": "Frog Jump With K Distances",
    "ninja_training": "Ninja's Training",
    "min_falling_path": "Minimum Falling Path Sum",
    "triangle_path": "Triangle (Minimum Path Sum)",
    "partition_equal_subset": "Partition Equal Subset Sum",
    "count_subsets_sum_k": "Count Subsets With Sum K",
    "unbounded_knapsack": "Unbounded Knapsack",
    "rod_cutting": "Rod Cutting",
}


def _nums(text):
    try:
        return [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None


def _rows(text):
    rows = [r for r in (text or "").replace(" ", "").split("/") if r]
    return [_nums(r) for r in rows]


def run(algo, text, target=None):
    if algo == "frog_jump_k":
        h = _nums(text)
        if not (2 <= len(h) <= 10) or any(not (0 <= v <= 999) for v in h):
            raise ValueError("Give 2–10 heights, each 0–999.")
        if target is None or target != int(target) or not (1 <= target <= len(h) - 1):
            raise ValueError(f"K must be 1–{len(h) - 1}.")
        return _frog(h, int(target))
    if algo in ("ninja_training", "min_falling_path", "triangle_path"):
        g = _rows(text)
        if not g or len(g) > 6 or any(abs(v) > 999 for r in g for v in r):
            raise ValueError("Up to 6 rows, values within ±999, rows separated by '/'.")
        if algo == "ninja_training" and any(len(r) != 3 for r in g):
            raise ValueError("Each day needs exactly 3 task scores, e.g. 10,40,70.")
        if algo == "min_falling_path" and (any(len(r) != len(g[0]) for r in g)
                                           or not 1 <= len(g[0]) <= 6):
            raise ValueError("A rectangular matrix, up to 6×6.")
        if algo == "triangle_path" and any(len(r) != i + 1 for i, r in enumerate(g)):
            raise ValueError("Row i must have i+1 numbers: 2/3,4/6,5,7/…")
        return {"ninja_training": _ninja, "min_falling_path": _falling,
                "triangle_path": _triangle}[algo](g)
    if algo in ("partition_equal_subset", "count_subsets_sum_k"):
        a = _nums(text)
        if not (1 <= len(a) <= 6) or any(not (1 <= v <= 12) for v in a):
            raise ValueError("Give 1–6 numbers, each 1–12.")
        if algo == "partition_equal_subset":
            if sum(a) > 24:
                raise ValueError("Keep the total at most 24 so the table fits.")
            return _partition(a)
        if target is None or target != int(target) or not (0 <= target <= 12):
            raise ValueError("K must be 0–12.")
        return _count_subsets(a, int(target))
    if algo == "unbounded_knapsack":
        parts = [p for p in (text or "").replace(" ", "").split(",") if p]
        try:
            items = [tuple(int(x) for x in p.split(":")) for p in parts]
        except ValueError:
            raise ValueError("Items as weight:value pairs — e.g. 2:5, 3:7.") from None
        if not (1 <= len(items) <= 5) or any(len(it) != 2 or not (1 <= it[0] <= 10)
                                             or not (1 <= it[1] <= 99) for it in items):
            raise ValueError("1–5 items as weight:value, weights 1–10, values 1–99.")
        if target is None or target != int(target) or not (1 <= target <= 12):
            raise ValueError("Capacity must be 1–12.")
        return _unbounded([w for w, _ in items], [v for _, v in items], int(target),
                          "unbounded_knapsack")
    prices = _nums(text)
    if not (1 <= len(prices) <= 8) or any(not (0 <= p <= 99) for p in prices):
        raise ValueError("Give 1–8 prices (0–99): the price of a piece of length 1, 2, …")
    return _unbounded(list(range(1, len(prices) + 1)), prices, len(prices),
                      "rod_cutting")


class _Grid:
    def __init__(self, rows, cols):
        self.grid = [[None] * cols for _ in range(rows)]
        self.steps: list = []
        self.counts = {"cells": 0}

    def add(self, note, row=None, col=None, deps=(), path=(), match=True):
        self.steps.append({"i": len(self.steps), "line": 0,
                           "structures": {"grid": [r[:] for r in self.grid],
                                          "row": row, "col": col,
                                          "deps": [list(d) for d in deps],
                                          "match": match,
                                          "path": [list(p) for p in path],
                                          "counts": dict(self.counts)},
                           "highlight": {"index": col}, "note": note})


def _out(algo, g, res, rows, cols, **extra):
    return {"meta": {"algorithm": algo, "view": "grid", "language": "python",
                     "result": res, "row_labels": rows, "col_labels": cols, **extra},
            "steps": g.steps}


def _frog(h, k):
    n = len(h)
    g = _Grid(2, n)
    g.grid[0] = h[:]
    dp = [0] * n
    prev = [None] * n
    g.grid[1][0] = 0
    g.add(f"The frog may jump 1 to {k} stones ahead; a jump costs the height "
          f"difference. dp[i] is the cheapest way to reach stone i.", 1, 0)
    for i in range(1, n):
        g.counts["cells"] += 1
        best, arg = None, None
        for j in range(1, k + 1):
            if i - j < 0:
                break
            c = dp[i - j] + abs(h[i] - h[i - j])
            if best is None or c < best:
                best, arg = c, i - j
        dp[i], prev[i] = best, arg
        g.grid[1][i] = best
        deps = [(1, i - j) for j in range(1, k + 1) if i - j >= 0]
        g.add(f"Stone {i}: try the last {len(deps)} stone(s); the best is from "
              f"stone {arg}: {dp[arg]} + |{h[i]} − {h[arg]}| = {best}.",
              1, i, deps)
    path, i = [], n - 1
    while i is not None:
        path.append((1, i))
        i = prev[i]
    g.add(f"Minimum energy to reach the last stone: {dp[-1]}. Green: the "
          f"stones it lands on.", path=path)
    return _out("frog_jump_k", g, dp[-1], ["height", "energy"],
                [str(i) for i in range(n)])


def _ninja(pts):
    n = len(pts)
    g = _Grid(n, 3)
    dp = [[0] * 3 for _ in range(n)]
    g.add("dp[day][task] = today's points for that task + the best of "
          "yesterday's other two tasks (no task two days in a row).")
    for d in range(n):
        for t in range(3):
            g.counts["cells"] += 1
            if d == 0:
                dp[d][t] = pts[d][t]
                g.grid[d][t] = dp[d][t]
                g.add(f"Day 0, task {t}: just its points, {pts[d][t]}.", d, t)
                continue
            others = [u for u in range(3) if u != t]
            u = max(others, key=lambda x: dp[d - 1][x])
            dp[d][t] = pts[d][t] + dp[d - 1][u]
            g.grid[d][t] = dp[d][t]
            g.add(f"Day {d}, task {t}: {pts[d][t]} + best of yesterday's other "
                  f"tasks ({dp[d - 1][u]}, task {u}) = {dp[d][t]}.", d, t,
                  [(d - 1, x) for x in others])
    best_t = max(range(3), key=lambda t: dp[-1][t])
    path, t = [], best_t
    for d in range(n - 1, -1, -1):
        path.append((d, t))
        if d:
            t = max((u for u in range(3) if u != t), key=lambda x: dp[d - 1][x])
    res = dp[-1][best_t]
    g.add(f"Best total: {res}. Green: the task chosen each day.", path=path)
    return _out("ninja_training", g, res, [f"day {d}" for d in range(n)],
                ["task 0", "task 1", "task 2"])


def _falling(a):
    R, C = len(a), len(a[0])
    g = _Grid(R, C)
    dp = [row[:] for row in a]
    g.grid[0] = a[0][:]
    g.add("dp[r][c] = a[r][c] + the smallest of the (up to) three cells above "
          "it. Row 0 starts as the matrix itself.", 0, 0)
    for r in range(1, R):
        for c in range(C):
            g.counts["cells"] += 1
            ups = [x for x in (c - 1, c, c + 1) if 0 <= x < C]
            m = min(dp[r - 1][x] for x in ups)
            dp[r][c] = a[r][c] + m
            g.grid[r][c] = dp[r][c]
            g.add(f"({r}, {c}): {a[r][c]} + min above {m} = {dp[r][c]}.", r, c,
                  [(r - 1, x) for x in ups])
    c = min(range(C), key=lambda x: dp[-1][x])
    res = dp[-1][c]
    path = []
    for r in range(R - 1, -1, -1):
        path.append((r, c))
        if r:
            c = min((x for x in (c - 1, c, c + 1) if 0 <= x < C),
                    key=lambda x: dp[r - 1][x])
    g.add(f"Minimum falling path sum: {res}. Green: the path.", path=path)
    return _out("min_falling_path", g, res, [str(r) for r in range(R)],
                [str(c) for c in range(C)])


def _triangle(t):
    n = len(t)
    g = _Grid(n, n)
    dp = [row[:] for row in t]
    g.grid[0][0] = t[0][0]
    g.add("Walk top to bottom, moving to the same or the next index. "
          "dp[r][c] = t[r][c] + min of the (up to) two cells above.", 0, 0)
    for r in range(1, n):
        for c in range(r + 1):
            g.counts["cells"] += 1
            ups = [x for x in (c - 1, c) if 0 <= x <= r - 1]
            m = min(dp[r - 1][x] for x in ups)
            dp[r][c] = t[r][c] + m
            g.grid[r][c] = dp[r][c]
            g.add(f"({r}, {c}): {t[r][c]} + min above {m} = {dp[r][c]}.", r, c,
                  [(r - 1, x) for x in ups])
    c = min(range(n), key=lambda x: dp[-1][x])
    res = dp[-1][c]
    path = []
    for r in range(n - 1, -1, -1):
        path.append((r, c))
        if r:
            c = min((x for x in (c - 1, c) if 0 <= x <= r - 1),
                    key=lambda x: dp[r - 1][x])
    g.add(f"Minimum path sum: {res}. Green: the path.", path=path)
    return _out("triangle_path", g, res, [str(r) for r in range(n)],
                [str(c) for c in range(n)])


def _subset_table(a, target, count, intro):
    n = len(a)
    g = _Grid(n + 1, target + 1)
    dp = [[0] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for s in range(target + 1):
        g.grid[0][s] = dp[0][s] if count else ("✓" if dp[0][s] else "·")
    g.add(intro + " Row 0 is the empty set: it makes a sum of 0 and nothing else.",
          0, 0)
    for i in range(1, n + 1):
        w = a[i - 1]
        for s in range(target + 1):
            g.counts["cells"] += 1
            skip = dp[i - 1][s]
            take = dp[i - 1][s - w] if s >= w else 0
            dp[i][s] = skip + take if count else int(bool(skip or take))
            g.grid[i][s] = dp[i][s] if count else ("✓" if dp[i][s] else "·")
            deps = [(i - 1, s)] + ([(i - 1, s - w)] if s >= w else [])
            if count:
                g.add(f"Sum {s} with {w} available: {skip} way(s) without it + "
                      f"{take} using it = {dp[i][s]}.", i, s, deps,
                      match=dp[i][s] > 0)
            else:
                g.add(f"Sum {s}: " + ("reachable" if dp[i][s] else "not reachable")
                      + (f" (by adding {w} to sum {s - w})." if take and not skip
                         else "."), i, s, deps, match=bool(dp[i][s]))
    return g, dp


def _partition(a):
    total = sum(a)
    if total % 2:
        g = _Grid(1, 1)
        g.add(f"The total is {total}, which is odd — two equal halves are "
              f"impossible. No table needed.", match=False)
        return _out("partition_equal_subset", g, False, ["-"], ["-"])
    half = total // 2
    g, dp = _subset_table(a, half, False,
                          f"Total {total}: an equal split needs one subset "
                          f"summing to {half} — subset sum with target {half}.")
    ok = bool(dp[len(a)][half])
    g.add(f"{'Yes' if ok else 'No'} — {'some' if ok else 'no'} subset reaches "
          f"{half}, so the array {'can' if ok else 'cannot'} be split into two "
          f"equal halves.", len(a), half, match=ok)
    return _out("partition_equal_subset", g, ok, ["∅"] + [str(v) for v in a],
                [str(s) for s in range(half + 1)])


def _count_subsets(a, k):
    g, dp = _subset_table(a, k, True, f"Count the subsets summing to {k}.")
    res = dp[len(a)][k]
    g.add(f"{res} subset(s) sum to {k}.", len(a), k, match=res > 0)
    return _out("count_subsets_sum_k", g, res, ["∅"] + [str(v) for v in a],
                [str(s) for s in range(k + 1)])


def _unbounded(ws, vs, cap, algo):
    n = len(ws)
    g = _Grid(n + 1, cap + 1)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    for c in range(cap + 1):
        g.grid[0][c] = 0
    what = "piece of length" if algo == "rod_cutting" else "item of weight"
    g.add("Row 0: nothing to use, value 0. Taking an item reads the same row "
          "(it can be taken again); skipping it reads the row above.", 0, 0)
    for i in range(1, n + 1):
        w, v = ws[i - 1], vs[i - 1]
        for c in range(cap + 1):
            g.counts["cells"] += 1
            skip = dp[i - 1][c]
            take = v + dp[i][c - w] if c >= w else None
            dp[i][c] = max(skip, take) if take is not None else skip
            g.grid[i][c] = dp[i][c]
            deps = [(i - 1, c)] + ([(i, c - w)] if c >= w else [])
            g.add(f"Capacity {c}, {what} {w} (value {v}): skip → {skip}"
                  + (f", take (again allowed) → {v} + {dp[i][c - w]} = {take}"
                     if take is not None else ", too big to take")
                  + f". Keep {dp[i][c]}.", i, c, deps)
    res = dp[n][cap]
    path, i, c = [], n, cap
    while i > 0 and c >= 0:
        path.append((i, c))
        if c >= ws[i - 1] and dp[i][c] == vs[i - 1] + dp[i][c - ws[i - 1]]:
            c -= ws[i - 1]
        else:
            i -= 1
    g.add(f"Best value: {res}. Green: the trace-back of choices.", path=path)
    labels = (["∅"] + [f"len {w}" for w in ws] if algo == "rod_cutting"
              else ["∅"] + [f"w{w}:v{v}" for w, v in zip(ws, vs)])
    return _out(algo, g, res, labels, [str(c) for c in range(cap + 1)])
