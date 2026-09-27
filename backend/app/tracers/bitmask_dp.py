"""Bitmask DP (batch 73) on the `grid` view — each row is a subset, labelled
by its bitmask (bit i set ⇔ item i is in the set; item 0 is the RIGHTMOST
bit).

* tsp_bitmask — Held–Karp: dp[mask][j] = cheapest path that starts at city
  0, visits exactly the cities in mask and ends at j. Add one unvisited
  city at a time; the tour closes back to 0. O(2^n · n²) instead of n!.
* assignment_bitmask — person p = popcount(mask) takes one job not in mask:
  dp[mask] = min cost to give the first popcount(mask) people the jobs in
  mask.
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "tsp_bitmask": "Travelling Salesman (Bitmask DP)",
    "assignment_bitmask": "Job Assignment (Bitmask DP)",
}
INF = float("inf")


def run(algo, text, target=None):
    g = parse_matrix(text, max_side=5 if algo == "tsp_bitmask" else 4)
    n = len(g)
    if len(g[0]) != n or n < 2 or any(not (0 <= v <= 99) for r in g for v in r):
        raise ValueError("Give a square matrix (2 × 2 or larger) of costs 0–99.")
    return (_tsp if algo == "tsp_bitmask" else _assign)(g)


def _label(mask, n):
    return format(mask, f"0{n}b")


def _tsp(d):
    n = len(d)
    masks = [m for m in range(1 << n) if m & 1]          # tours start at city 0
    row = {m: r for r, m in enumerate(masks)}
    dp = {(1, 0): 0}
    G = Grid(len(masks), n)
    G.grid[0][0] = 0
    G.counts = {"transitions": 0}
    G.add(f"dp[mask][j] = cheapest path from city 0 through exactly the cities "
          f"in mask, ending at j. Start: dp[{_label(1, n)}][0] = 0. Each step adds "
          f"one unvisited city k: dp[mask | k][k] = min(dp[mask][j] + d[j][k]).", 0, 0)
    for m in masks:
        for j in range(n):
            if (m, j) not in dp:
                continue
            for k in range(n):
                if m >> k & 1:
                    continue
                nm = m | 1 << k
                cand = dp[(m, j)] + d[j][k]
                G.counts["transitions"] += 1
                if cand < dp.get((nm, k), INF):
                    dp[(nm, k)] = cand
                    G.grid[row[nm]][k] = cand
        if m != 1:
            filled = [(row[m], j) for j in range(n) if (m, j) in dp]
            ends = {j: dp[(m, j)] for j in range(n) if (m, j) in dp}
            G.add(f"Mask {_label(m, n)} (cities {[i for i in range(n) if m >> i & 1]}): "
                  f"best cost ending at each city {ends}.", row[m], None, [], filled)
    full = (1 << n) - 1
    best, last = min((dp[(full, j)] + d[j][0], j) for j in range(1, n))
    G.add(f"All cities visited: close the tour back to 0. min over j of "
          f"dp[{_label(full, n)}][j] + d[j][0] = {best} (last city {last}).",
          row[full], last, [(row[full], j) for j in range(1, n)], [(row[full], last)])
    return G.result("tsp_bitmask", best, [_label(m, n) for m in masks],
                    [f"end {j}" for j in range(n)])


def _assign(cost):
    n = len(cost)
    size = 1 << n
    dp = [INF] * size
    choice = [None] * size
    dp[0] = 0
    G = Grid(size, 3)
    G.grid[0] = [0, 0, "—"]
    G.counts = {"transitions": 0}
    G.add("Rows are subsets of JOBS already handed out. With p = popcount(mask) "
          "jobs taken, person p picks a free job j: dp[mask | j] = min(dp[mask] + "
          "cost[p][j]).", 0, 0)
    for m in range(size):
        p = bin(m).count("1")
        if dp[m] == INF or p == n:
            continue
        for j in range(n):
            if m >> j & 1:
                continue
            nm = m | 1 << j
            G.counts["transitions"] += 1
            if dp[m] + cost[p][j] < dp[nm]:
                dp[nm] = dp[m] + cost[p][j]
                choice[nm] = (p, j)
                G.grid[nm] = [dp[nm], p + 1, f"P{p}→J{j}"]
        G.add(f"From mask {_label(m, n)} (cost {dp[m]}): person {p} tries each free "
              f"job.", m, 0, [(m | 1 << j, 0) for j in range(n) if not m >> j & 1])
    full = size - 1
    plan, m = [], full
    while m:
        p, j = choice[m]
        plan.append((p, j))
        m ^= 1 << j
    plan.reverse()
    G.add(f"All jobs assigned: minimum cost {dp[full]} — "
          f"{', '.join(f'P{p}→J{j}' for p, j in plan)}.", full, 0,
          path=[(sum(1 << j for _, j in plan[:i + 1]), 2) for i in range(n)])
    return G.result("assignment_bitmask", dp[full], [_label(m, n) for m in range(size)],
                    ["cost", "people", "last pick"], plan=[list(x) for x in plan])
