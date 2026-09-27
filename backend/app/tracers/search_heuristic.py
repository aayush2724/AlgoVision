"""Informed grid search (batch 70) on the `grid` view.

* a_star_grid — pop the open cell with the smallest f = g + h, where g is
  the steps so far and h the Manhattan distance to the goal. h never
  overestimates, so the first time the goal is popped its path is shortest.
* best_first_grid — greedy: pop by h alone. It usually reaches the goal in
  fewer pops, but the path it finds can be longer than the shortest.
* zero_one_bfs — edges cost 0 or 1 (entering a cell costs its value): a
  deque replaces the heap — 0-cost moves go to the front, 1-cost to the back.

Maze cells: S start, G goal, # wall, . open. Tinted cells are the open set;
green cells are closed (expanded), then the final path.
"""

import heapq
from collections import deque

from app.tracers.grid_common import DIRS4, Grid, parse_matrix

TITLES = {
    "a_star_grid": "A* Search on a Grid",
    "best_first_grid": "Greedy Best-First Search on a Grid",
    "zero_one_bfs": "0-1 BFS (Minimum Cost Path)",
}


def run(algo, text, target=None):
    if algo == "zero_one_bfs":
        g = parse_matrix(text, max_side=7)
        if any(v not in (0, 1) for r in g for v in r):
            raise ValueError("Cells must be 0 or 1 (the cost to enter them).")
        return _zero_one(g)
    raw = (text or "").replace(" ", "").upper()
    if "," not in raw:                     # compact rows: S..#/.#.G
        raw = "/".join(",".join(r) for r in raw.split("/") if r)
    g = parse_matrix(raw, allowed="S.#G", max_side=8)
    cells = [c for r in g for c in r]
    if cells.count("S") != 1 or cells.count("G") != 1:
        raise ValueError("Mark exactly one S (start) and one G (goal).")
    return _informed(g, algo)


def _find(g, ch):
    return next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == ch)


def _trace_path(parent, end):
    path = [end]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def _informed(g, algo):
    R, C = len(g), len(g[0])
    star = algo == "a_star_grid"
    s, t = _find(g, "S"), _find(g, "G")
    h = lambda p: abs(p[0] - t[0]) + abs(p[1] - t[1])
    G = Grid(R, C)
    G.grid = [row[:] for row in g]
    G.counts = {"pops": 0, "pushes": 1}
    best_g = {s: 0}
    parent = {s: None}
    heap = [(h(s), h(s), s)]
    closed = []
    G.add(("A*: always expand the open cell with the smallest f = g + h (steps "
           "taken + Manhattan distance left). h never overestimates, so the "
           "first time G is expanded, its path is the shortest.") if star else
          ("Greedy best-first: expand the open cell that LOOKS closest to G "
           "(smallest h only), ignoring how far we have already walked."), *s)
    while heap:
        _, _, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.append(cur)
        G.counts["pops"] += 1
        gv = best_g[cur]
        if cur not in (s, t):
            G.grid[cur[0]][cur[1]] = gv
        if cur == t:
            path = _trace_path(parent, t)
            open_cells = sorted({p for _, _, p in heap if p not in closed})
            G.add(f"Expanded G after {G.counts['pops']} pops. Path length "
                  f"{len(path) - 1}" + ("" if star else
                                         " (greedy — not guaranteed shortest)") + ".",
                  *t, open_cells, path)
            return G.result(algo, len(path) - 1)
        for dr, dc in DIRS4:
            nr, nc = cur[0] + dr, cur[1] + dc
            if not (0 <= nr < R and 0 <= nc < C) or g[nr][nc] == "#":
                continue
            ng = gv + 1
            if (nr, nc) not in best_g or (star and ng < best_g[(nr, nc)]):
                best_g[(nr, nc)] = ng
                parent[(nr, nc)] = cur
                hn = h((nr, nc))
                heapq.heappush(heap, (ng + hn if star else hn, hn, (nr, nc)))
                G.counts["pushes"] += 1
        open_cells = sorted({p for _, _, p in heap if p not in closed})
        G.add(f"Expand ({cur[0]},{cur[1]}): g = {gv}, h = {h(cur)}"
              + (f", f = {gv + h(cur)}" if star else "")
              + f". Open set now {len(open_cells)} cell(s).", *cur, open_cells, closed)
    G.add("The open set emptied without reaching G — no path.", match=False)
    return G.result(algo, -1)


def _zero_one(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [row[:] for row in g]
    G.counts = {"front_pushes": 0, "back_pushes": 0}
    INF = float("inf")
    dist = [[INF] * C for _ in range(R)]
    dist[0][0] = g[0][0]
    parent = {(0, 0): None}
    dq = deque([(0, 0)])
    done = []
    G.add(f"Reach ({R - 1},{C - 1}) from (0,0); entering a cell costs its value "
          f"(0 or 1). With only 0/1 costs a deque is enough: a 0-cost move goes "
          f"to the FRONT (same distance), a 1-cost move to the BACK.", 0, 0)
    while dq:
        r, c = dq.popleft()
        if (r, c) in done:
            continue
        done.append((r, c))
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[r][c] + g[nr][nc] < dist[nr][nc]:
                dist[nr][nc] = dist[r][c] + g[nr][nc]
                parent[(nr, nc)] = (r, c)
                if g[nr][nc] == 0:
                    dq.appendleft((nr, nc))
                    G.counts["front_pushes"] += 1
                else:
                    dq.append((nr, nc))
                    G.counts["back_pushes"] += 1
        G.add(f"Pop ({r},{c}) at cost {dist[r][c]}; relax its neighbours "
              f"(0-cost → front, 1-cost → back).", r, c, list(dq), done)
    path = _trace_path(parent, (R - 1, C - 1))
    res = dist[R - 1][C - 1]
    G.add(f"Minimum cost to reach ({R - 1},{C - 1}): {res}.", R - 1, C - 1, path=path)
    return G.result("zero_one_bfs", res)
