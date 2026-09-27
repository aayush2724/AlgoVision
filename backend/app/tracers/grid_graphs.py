"""Graph searches where the graph is a grid (Step 15) — cells are nodes,
up/down/left/right neighbours are edges.

* number_of_islands — every unvisited land cell starts a new island; a
  flood (BFS) stamps the whole island with its letter. Count = letters used.
* rotten_oranges — multi-source BFS: every rotten orange starts in the queue
  at minute 0; each minute the rot spreads one step. Any fresh orange left at
  the end can never rot (answer −1).
* nearest_one_distance — multi-source BFS from every 1 at once; the first
  time a cell is reached is its distance to the nearest 1.
* surrounded_regions — an 'O' region survives only if it touches the border.
  Flood from every border 'O' to mark the safe ones; flip the rest to 'X'.
* number_of_enclaves — the same border flood on land (1s); land the flood
  never reaches can't walk off the grid, and is counted.

Uses the `grid` view: the cell being processed is `row`/`col`, the BFS
frontier is tinted (`deps`), settled cells glow green (`path`).
"""

from collections import deque

from app.tracers.grid_common import Grid, parse_matrix, DIRS4

TITLES = {
    "number_of_islands": "Number of Islands",
    "rotten_oranges": "Rotten Oranges",
    "nearest_one_distance": "Distance of Nearest Cell Having 1",
    "surrounded_regions": "Surrounded Regions",
    "number_of_enclaves": "Number of Enclaves",
}


def run(algo, text, target=None):
    if algo == "surrounded_regions":
        return _surrounded(parse_matrix(text, allowed="XO"))
    g = parse_matrix(text)
    allowed = {0, 1, 2} if algo == "rotten_oranges" else {0, 1}
    if any(v not in allowed for r in g for v in r):
        raise ValueError("Cells must be " + ("0 (empty), 1 (fresh) or 2 (rotten)."
                                             if algo == "rotten_oranges" else "0 or 1."))
    if algo == "nearest_one_distance" and not any(v == 1 for r in g for v in r):
        raise ValueError("There must be at least one 1 to measure distance to.")
    return {"number_of_islands": _islands, "rotten_oranges": _rotten,
            "nearest_one_distance": _nearest, "number_of_enclaves": _enclaves}[algo](g)


def _inside(g, r, c):
    return 0 <= r < len(g) and 0 <= c < len(g[0])


def _islands(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [["·" if v == 0 else "1" for v in row] for row in src]
    G.counts = {"islands": 0, "cells_flooded": 0}
    seen: set = set()
    done: list = []
    G.add("Scan the grid. Each land cell (1) not yet seen starts a new island; "
          "flood it (up/down/left/right) and stamp every cell with its letter.")
    for r in range(R):
        for c in range(C):
            if src[r][c] != 1 or (r, c) in seen:
                continue
            label = chr(ord("A") + G.counts["islands"] % 26)
            G.counts["islands"] += 1
            q = deque([(r, c)])
            seen.add((r, c))
            G.grid[r][c] = label
            done.append((r, c))
            G.add(f"New land at ({r}, {c}) — island {label}. Flood it.", r, c,
                  path=done)
            while q:
                cr, cc = q.popleft()
                for dr, dc in DIRS4:
                    nr, nc = cr + dr, cc + dc
                    if _inside(src, nr, nc) and src[nr][nc] == 1 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))
                        G.grid[nr][nc] = label
                        done.append((nr, nc))
                        G.counts["cells_flooded"] += 1
                        G.add(f"({nr}, {nc}) joins island {label}.", nr, nc,
                              deps=list(q), path=done)
    n = G.counts["islands"]
    G.add(f"{n} island(s). Each cell was visited once — O(rows × cols).", path=done)
    return G.result("number_of_islands", n)


def _rotten(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    sym = {0: "·", 1: "F", 2: "R"}
    G.grid = [[sym[v] for v in row] for row in src]
    G.counts = {"minutes": 0, "rotted": 0}
    q = deque((r, c) for r in range(R) for c in range(C) if src[r][c] == 2)
    fresh = sum(v == 1 for row in src for v in row)
    rotten = [list(p) for p in q]
    G.add(f"F = fresh, R = rotten. Every rotten orange spreads at once "
          f"(multi-source BFS); each newly rotten cell shows the minute it "
          f"turned. {fresh} fresh orange(s) to reach.", deps=list(q), path=rotten)
    grid = [row[:] for row in src]
    minute = 0
    while q and fresh:
        minute += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in DIRS4:
                nr, nc = r + dr, c + dc
                if _inside(grid, nr, nc) and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
                    G.grid[nr][nc] = str(minute)
                    rotten.append([nr, nc])
                    G.counts["rotted"] += 1
        G.counts["minutes"] = minute
        G.add(f"Minute {minute}: the rot spreads one step — {len(q)} newly "
              f"rotten, {fresh} fresh left.", deps=list(q), path=rotten)
    res = minute if fresh == 0 else -1
    if fresh:
        G.add(f"{fresh} fresh orange(s) can never be reached — answer −1.",
              path=rotten, match=False)
    else:
        G.add(f"Every orange is rotten after {minute} minute(s).", path=rotten)
    return G.result("rotten_oranges", res)


def _nearest(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    dist = [[None] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if src[r][c] == 1:
                dist[r][c] = 0
                q.append((r, c))
                G.grid[r][c] = 0
    G.counts = {"cells": len(q)}
    done = [list(p) for p in q]
    G.add("Start a BFS from every 1 at the same time (distance 0). The first "
          "time a cell is reached, that is its distance to the nearest 1.",
          deps=list(q), path=done)
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if _inside(src, nr, nc) and dist[nr][nc] is None:
                dist[nr][nc] = dist[r][c] + 1
                G.grid[nr][nc] = dist[nr][nc]
                q.append((nr, nc))
                done.append([nr, nc])
                G.counts["cells"] += 1
                G.add(f"({nr}, {nc}) is first reached from ({r}, {c}) — "
                      f"distance {dist[nr][nc]}.", nr, nc, deps=list(q), path=done)
    G.add("Every cell holds its distance to the nearest 1 — one BFS, O(R × C).",
          path=done)
    return G.result("nearest_one_distance", dist)


def _border_flood(G, R, C, is_open, label):
    q = deque()
    safe: set = set()
    for r in range(R):
        for c in range(C):
            if (r in (0, R - 1) or c in (0, C - 1)) and is_open(r, c):
                q.append((r, c))
                safe.add((r, c))
    G.add(f"Every {label} on the border can escape. Flood inward from all of "
          f"them at once.", deps=list(q), path=sorted(safe))
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and is_open(nr, nc) and (nr, nc) not in safe:
                safe.add((nr, nc))
                q.append((nr, nc))
                G.add(f"({nr}, {nc}) touches a border-connected {label} — it can "
                      f"escape too.", nr, nc, deps=list(q), path=sorted(safe))
    return safe


def _surrounded(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [row[:] for row in src]
    G.counts = {"flipped": 0}
    safe = _border_flood(G, R, C, lambda r, c: src[r][c] == "O", "'O'")
    for r in range(R):
        for c in range(C):
            if src[r][c] == "O" and (r, c) not in safe:
                G.grid[r][c] = "X"
                G.counts["flipped"] += 1
                G.add(f"({r}, {c}) is an 'O' the border flood never reached — it "
                      f"is surrounded. Flip it to 'X'.", r, c, path=sorted(safe),
                      match=False)
    G.add(f"{G.counts['flipped']} cell(s) flipped; green 'O's survive because "
          f"they connect to the border.", path=sorted(safe))
    return G.result("surrounded_regions", G.grid)


def _enclaves(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [["·" if v == 0 else "1" for v in row] for row in src]
    G.counts = {"enclaves": 0}
    safe = _border_flood(G, R, C, lambda r, c: src[r][c] == 1, "land cell")
    trapped = [(r, c) for r in range(R) for c in range(C)
               if src[r][c] == 1 and (r, c) not in safe]
    for r, c in trapped:
        G.grid[r][c] = "E"
        G.counts["enclaves"] += 1
        G.add(f"({r}, {c}) is land the border flood never reached — it can't "
              f"walk off the grid. Count it.", r, c, path=sorted(safe), match=False)
    G.add(f"{len(trapped)} enclave cell(s), marked E. Green land can reach the "
          f"edge.", path=sorted(safe))
    return G.result("number_of_enclaves", len(trapped))
