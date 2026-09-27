"""Shortest-path and union-find problems on grids (Step 15).

* binary_maze_path — unit-weight shortest path from the top-left to the
  bottom-right through 1-cells: plain BFS; distances are written into cells.
* min_effort_path — Dijkstra where a path's cost is its *largest* single step
  |h1 − h2|, so a cell's label is the smallest such worst step so far.
* swim_rising_water — Dijkstra where a path's cost is the highest cell on it
  (you can swim once the water reaches it).
* largest_island — label every island and its size (union-find), then try
  each 0: flipping it joins the distinct islands around it.
* islands_ii — land is added one cell at a time; union-find merges it with any
  land neighbours, and the island count is reported after every addition.

Uses the `grid` view: settled cells glow green (`path`), the frontier or the
neighbours being joined are tinted (`deps`), the current cell is outlined.
"""

import heapq
from collections import deque

from app.tracers.grid_common import Grid, parse_matrix, DIRS4

TITLES = {
    "binary_maze_path": "Shortest Path in a Binary Maze",
    "min_effort_path": "Path With Minimum Effort",
    "swim_rising_water": "Swim in Rising Water",
    "largest_island": "Making a Large Island",
    "islands_ii": "Number of Islands II (Online)",
}


def run(algo, text, target=None):
    if algo == "islands_ii":
        return _islands_ii(text)
    g = parse_matrix(text, max_side=6)
    if algo in ("binary_maze_path", "largest_island"):
        if any(v not in (0, 1) for r in g for v in r):
            raise ValueError("Cells must be 0 or 1.")
        if algo == "binary_maze_path" and (g[0][0] != 1 or g[-1][-1] != 1):
            raise ValueError("The start (top-left) and exit (bottom-right) must be 1.")
    elif any(not (0 <= v <= 99) for r in g for v in r):
        raise ValueError("Heights must be 0–99.")
    return {"binary_maze_path": _maze, "min_effort_path": _effort,
            "swim_rising_water": _swim, "largest_island": _largest}[algo](g)


def _maze(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [["·" if v == 1 else "#" for v in row] for row in src]
    G.counts = {"cells": 1}
    dist = {(0, 0): 0}
    prev = {}
    G.grid[0][0] = 0
    q = deque([(0, 0)])
    G.add("Every step costs 1, so BFS finds the shortest path: cells are "
          "reached in order of distance. '#' is a wall.", 0, 0, path=[(0, 0)])
    while q:
        r, c = q.popleft()
        if (r, c) == (R - 1, C - 1):
            break
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and src[nr][nc] == 1 and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                prev[(nr, nc)] = (r, c)
                G.grid[nr][nc] = dist[(nr, nc)]
                G.counts["cells"] += 1
                q.append((nr, nc))
                G.add(f"({nr}, {nc}) reached from ({r}, {c}) at distance "
                      f"{dist[(nr, nc)]}.", nr, nc, deps=list(q), path=list(dist))
    end = (R - 1, C - 1)
    if end not in dist:
        G.add("The exit is walled off — no path (−1).", match=False)
        return G.result("binary_maze_path", -1)
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    G.add(f"Shortest path length: {dist[end]}. Green: the route.", path=path)
    return G.result("binary_maze_path", dist[end])


def _dijkstra_grid(src, algo, cost, intro, unit):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    best = {(0, 0): cost(None, src[0][0])}
    prev = {}
    G.grid[0][0] = best[(0, 0)]
    G.counts = {"settled": 0}
    pq = [(best[(0, 0)], 0, 0)]
    settled: list = []
    G.add(intro, 0, 0)
    while pq:
        d, r, c = heapq.heappop(pq)
        if d != best.get((r, c)) or (r, c) in settled:
            continue
        settled.append((r, c))
        G.counts["settled"] += 1
        G.add(f"Settle ({r}, {c}) with {unit} {d} — the smallest on the queue.",
              r, c, deps=[(x, y) for _, x, y in pq], path=settled)
        if (r, c) == (R - 1, C - 1):
            break
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                nd = max(d, cost(src[r][c], src[nr][nc]))
                if nd < best.get((nr, nc), float("inf")):
                    best[(nr, nc)] = nd
                    prev[(nr, nc)] = (r, c)
                    G.grid[nr][nc] = nd
                    heapq.heappush(pq, (nd, nr, nc))
    end = (R - 1, C - 1)
    path, cur = [], end
    while cur is not None:
        path.append(cur)
        cur = prev.get(cur)
    G.add(f"Reached the bottom-right corner: {unit} {best[end]}. Green: the "
          f"route.", path=path)
    return G.result(algo, best[end])


def _effort(src):
    return _dijkstra_grid(
        src, "min_effort_path", lambda a, b: 0 if a is None else abs(a - b),
        "A path's effort is its steepest single step. Dijkstra, but a cell's "
        "label is the smallest worst-step found so far.", "effort")


def _swim(src):
    return _dijkstra_grid(
        src, "swim_rising_water", lambda a, b: b,
        "You can swim once the water reaches every cell on your route, so a "
        "route costs its highest cell. Dijkstra on that maximum.", "water level")


class _DSU:
    def __init__(self):
        self.p, self.size = {}, {}

    def add(self, x):
        self.p[x], self.size[x] = x, 1

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.p[b] = a
        self.size[a] += self.size[b]
        return True


def _largest(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [["·" if v == 0 else "1" for v in row] for row in src]
    G.counts = {"flips_tried": 0}
    d = _DSU()
    for r in range(R):
        for c in range(C):
            if src[r][c]:
                d.add((r, c))
    for r in range(R):
        for c in range(C):
            if src[r][c]:
                for dr, dc in ((1, 0), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if nr < R and nc < C and src[nr][nc]:
                        d.union((r, c), (nr, nc))
    for (r, c) in list(d.p):
        G.grid[r][c] = d.size[d.find((r, c))]
    best = max((d.size[d.find(x)] for x in d.p), default=0)
    land = list(d.p)
    G.add(f"Union-find groups the land into islands; each land cell shows its "
          f"island's size. Largest without flipping: {best}.", path=land)
    best_cell = None
    for r in range(R):
        for c in range(C):
            if src[r][c]:
                continue
            G.counts["flips_tried"] += 1
            roots = {d.find((r + dr, c + dc)) for dr, dc in DIRS4
                     if 0 <= r + dr < R and 0 <= c + dc < C and src[r + dr][c + dc]}
            size = 1 + sum(d.size[x] for x in roots)
            nb = [(x, y) for x, y in land if d.find((x, y)) in roots]
            if size > best:
                best, best_cell = size, (r, c)
            G.add(f"Flip ({r}, {c}): it joins {len(roots)} distinct island(s) → "
                  f"size {size}. Best so far {best}.", r, c, deps=nb, path=land,
                  match=size == best)
    br, bc = best_cell if best_cell else (None, None)
    G.add(f"Largest island after at most one flip: {best}"
          + (f" (flip {best_cell})." if best_cell else " (no flip helps)."),
          br, bc, path=land)
    return G.result("largest_island", best)


def _islands_ii(text):
    usage = "Give 'rows x cols | r:c r:c …', e.g. 3x3 | 0:0 0:1 1:2."
    if "|" not in (text or ""):
        raise ValueError(usage)
    size, ops = text.split("|", 1)
    try:
        R, C = (int(x) for x in size.lower().replace(" ", "").split("x"))
        cells = [tuple(int(v) for v in p.split(":")) for p in ops.split()]
    except ValueError:
        raise ValueError(usage) from None
    if not (1 <= R <= 6 and 1 <= C <= 6):
        raise ValueError("Keep the grid within 6×6.")
    if not cells or len(cells) > 20 or any(len(p) != 2 or not (0 <= p[0] < R and 0 <= p[1] < C)
                                           for p in cells):
        raise ValueError(f"1–20 positions, each inside the {R}×{C} grid.")
    G = Grid(R, C, "·")
    G.counts = {"islands": 0, "unions": 0}
    d = _DSU()
    counts = []
    G.add("Land appears one cell at a time. Each new cell is its own island "
          "until union-find merges it with land neighbours.")
    for (r, c) in cells:
        if (r, c) in d.p:
            counts.append(G.counts["islands"])
            G.add(f"({r}, {c}) is already land — the count stays "
                  f"{G.counts['islands']}.", r, c, path=list(d.p))
            continue
        d.add((r, c))
        G.counts["islands"] += 1
        merged = []
        for dr, dc in DIRS4:
            nb = (r + dr, c + dc)
            if nb in d.p and d.union((r, c), nb):
                G.counts["islands"] -= 1
                G.counts["unions"] += 1
                merged.append(nb)
        G.grid[r][c] = G.counts["islands"]
        counts.append(G.counts["islands"])
        G.add(f"Add land at ({r}, {c})"
              + (f" — it merges {len(merged)} neighbouring island(s) into one."
                 if merged else " — a new island.")
              + f" Islands now: {G.counts['islands']}.", r, c, deps=merged,
              path=list(d.p))
    G.add(f"Island counts after each addition: {counts}.", path=list(d.p))
    return G.result("islands_ii", counts)
