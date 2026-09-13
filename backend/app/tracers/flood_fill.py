"""Flood fill — the paint-bucket tool, and the bones of "count the islands".

Every non-wall cell is canvas of one colour. Starting from one cell, the fill
spreads to its four orthogonal neighbours, and theirs, never crossing a wall
or the grid edge. What it reaches is exactly the connected region the start
sits in — the 2-D cousin of connected components.

Reuses the `grid` view: `structures.grid` holds a character per cell
(`#` wall, `·` canvas, `●` filled), `structures.path` lights the region filled
so far green, and `row`/`col` mark the cell under the brush. No new renderer.
"""

WALL = "#"
CANVAS = "·"
FILLED = "●"

MAX_SIDE = 8
# 4-connectivity, scanned in a fixed order so the trace is reproducible.
MOVES = [(-1, 0), (0, -1), (0, 1), (1, 0)]
MOVE_NAME = {(-1, 0): "up", (0, -1): "left", (0, 1): "right", (1, 0): "down"}


def trace(rows: int, cols: int, blocked: list | None = None,
          start: tuple[int, int] = (0, 0)):
    walls = {(int(r), int(c)) for r, c in (blocked or [])}
    sr, sc = int(start[0]), int(start[1])

    grid = [[WALL if (r, c) in walls else CANVAS for c in range(cols)]
            for r in range(rows)]
    filled: set = set()
    steps: list = []
    counts = {"filled": 0, "edge_checks": 0, "blocked": 0}

    def add(note, row=None, col=None, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": [],
                "match": match,
                "path": sorted([list(p) for p in filled]),
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"A {rows}×{cols} canvas. '#' cells are walls the paint cannot cross. "
        f"Drop the bucket on ({sr}, {sc}) and the colour spreads to every cell "
        f"reachable without stepping over a wall.")

    # A wall (or off-grid) start fills nothing — worth showing, not crashing.
    if not (0 <= sr < rows and 0 <= sc < cols):
        add(f"Start ({sr}, {sc}) is off the grid — nothing to fill.",
            match=False)
        return _result(rows, cols, walls, sr, sc, filled, steps)
    if (sr, sc) in walls:
        add(f"Start ({sr}, {sc}) is a wall — the bucket has nothing to paint.",
            row=sr, col=sc, match=False)
        return _result(rows, cols, walls, sr, sc, filled, steps)

    # Breadth-first so the spread reads as an expanding wavefront.
    queue = [(sr, sc)]
    grid[sr][sc] = FILLED
    filled.add((sr, sc))
    counts["filled"] += 1
    add(f"Paint the start cell ({sr}, {sc}).", row=sr, col=sc, match=True)

    head = 0
    while head < len(queue):
        r, c = queue[head]
        head += 1
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            counts["edge_checks"] += 1
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if (nr, nc) in walls:
                counts["blocked"] += 1
                continue
            if (nr, nc) in filled:
                continue
            grid[nr][nc] = FILLED
            filled.add((nr, nc))
            counts["filled"] += 1
            queue.append((nr, nc))
            add(f"From ({r}, {c}) the paint spreads {MOVE_NAME[(dr, dc)]} to "
                f"({nr}, {nc}).", row=nr, col=nc, match=True)

    total = len(filled)
    add(f"The bucket reached {total} cell(s) before walls and edges boxed it "
        f"in. That region is exactly the connected component of ({sr}, {sc}) "
        f"— flood fill is connected-components on a grid.",
        row=sr, col=sc, match=True)
    return _result(rows, cols, walls, sr, sc, filled, steps)


def _result(rows, cols, walls, sr, sc, filled, steps):
    return {
        "meta": {
            "algorithm": "flood_fill",
            "view": "grid",
            "language": "python",
            "rows": rows,
            "cols": cols,
            "blocked": [list(b) for b in sorted(walls)],
            "start": [sr, sc],
            "filled": sorted([list(p) for p in filled]),
            "filled_count": len(filled),
            "result": len(filled),
            "row_labels": [str(r) for r in range(rows)],
            "col_labels": [str(c) for c in range(cols)],
        },
        "steps": steps,
    }
