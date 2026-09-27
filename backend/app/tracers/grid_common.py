"""Shared step collector for tracers that draw on the `grid` view.

Every grid tracer emits the same step shape: the full cell matrix, the cell
being worked on (`row`/`col`), cells it reads or that form the live region
(`deps`, tinted), cells that are settled/part of the answer (`path`, green),
and whether the current cell "matched" (green vs orange outline).
"""


class Grid:
    def __init__(self, rows, cols, fill=None):
        self.grid = [[fill] * cols for _ in range(rows)]
        self.steps: list = []
        self.counts: dict = {}

    def add(self, note, row=None, col=None, deps=(), path=(), match=True):
        self.steps.append({"i": len(self.steps), "line": 0,
                           "structures": {"grid": [r[:] for r in self.grid],
                                          "row": row, "col": col,
                                          "deps": [list(d) for d in deps],
                                          "match": match,
                                          "path": [list(p) for p in path],
                                          "counts": dict(self.counts)},
                           "highlight": {"index": col}, "note": note})

    def result(self, algo, res, row_labels=None, col_labels=None, **meta):
        rows, cols = len(self.grid), len(self.grid[0]) if self.grid else 0
        return {"meta": {"algorithm": algo, "view": "grid", "language": "python",
                         "result": res, **meta,
                         "row_labels": row_labels or [str(r) for r in range(rows)],
                         "col_labels": col_labels or [str(c) for c in range(cols)]},
                "steps": self.steps}


def parse_matrix(text, allowed=None, max_side=7, what="numbers"):
    """'1,0,1 / 0,1,1' → list of rows (ints, or single chars when `allowed`
    is a string of letters). Raises ValueError with a user-facing reason."""
    rows = [r for r in (text or "").replace(" ", "").split("/") if r]
    if not rows:
        raise ValueError("Give rows separated by '/', cells by ',' — e.g. 1,0/0,1.")
    grid = []
    for r in rows:
        cells = [c for c in r.split(",") if c != ""]
        if allowed:
            cells = [c.upper() for c in cells]
            if any(c not in allowed for c in cells):
                raise ValueError(f"Cells must be one of: {', '.join(allowed)}.")
            grid.append(cells)
        else:
            try:
                grid.append([int(c) for c in cells])
            except ValueError:
                raise ValueError(f"Only {what}, separated by commas.") from None
    if not grid[0] or any(len(r) != len(grid[0]) for r in grid):
        raise ValueError("Every row needs the same number of cells.")
    if len(grid) > max_side or len(grid[0]) > max_side:
        raise ValueError(f"Keep the grid within {max_side}×{max_side}.")
    return grid


DIRS4 = [(-1, 0), (0, 1), (1, 0), (0, -1)]
