"""Rat in a Maze — backtracking over a grid, collecting *every* escape route.

The rat starts top-left and must reach bottom-right, moving D/L/R/U through
open cells and never revisiting a cell on its current route. Recursion tries
each direction in that (alphabetical) order; when a route dead-ends or
reaches the exit, it steps back and un-marks the cell so other routes may use
it. That un-marking is the heart of backtracking — the same cell can belong
to many different answers.

Reuses the `grid` view: `#` walls, `·` open cells, the current route lit
green via `path`, and the rat's cell at `row`/`col`. No new renderer.

Open grids have thousands of routes, so the trace records the first
MAX_STEPS steps and then keeps searching silently; the final step always
reports the full count.
"""

WALL = "#"
OPEN = "·"

MAX_SIDE = 5
MAX_STEPS = 300
MAX_PATHS_LISTED = 50
# Alphabetical order, so the answers come out already sorted.
MOVES = [("D", 1, 0), ("L", 0, -1), ("R", 0, 1), ("U", -1, 0)]
MOVE_NAME = {"D": "down", "L": "left", "R": "right", "U": "up"}


def trace(side: int, blocked: list | None = None):
    n = int(side)
    walls = {(int(r), int(c)) for r, c in (blocked or [])}
    grid = [[WALL if (r, c) in walls else OPEN for c in range(n)]
            for r in range(n)]
    steps: list = []
    counts = {"moves": 0, "backtracks": 0, "paths": 0}
    route: list = []            # cells on the current route, in order
    on_route: set = set()
    paths: list = []
    elided = {"steps": 0}

    def add(note, row=None, col=None, match=None, final=False):
        if not final and len(steps) >= MAX_STEPS:
            elided["steps"] += 1
            return
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": [],
                "match": match,
                "path": [list(p) for p in route],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    end = (n - 1, n - 1)
    add(f"A {n}×{n} maze; '#' cells are blocked. Find every route from (0, 0) "
        f"to ({n - 1}, {n - 1}) moving D, L, R, U — never stepping on a cell "
        f"twice in one route.")

    if (0, 0) in walls or end in walls:
        add("The start or the exit is blocked — there is no route at all.",
            match=False, final=True)
        return _result(n, walls, paths, counts, steps)

    def solve(r, c, moves):
        if (r, c) == end:
            counts["paths"] += 1
            paths.append(moves)
            add(f"Reached the exit! Route #{counts['paths']}: "
                f"{moves or '(already there)'}. Record it, then step back to "
                f"look for more.", row=r, col=c, match=True)
            return
        for d, dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < n):
                continue
            if (nr, nc) in walls or (nr, nc) in on_route:
                continue
            counts["moves"] += 1
            route.append((nr, nc))
            on_route.add((nr, nc))
            add(f"From ({r}, {c}) try {d} ({MOVE_NAME[d]}) to ({nr}, {nc}). "
                f"Route so far: {moves + d}.", row=nr, col=nc, match=True)
            solve(nr, nc, moves + d)
            route.pop()
            on_route.discard((nr, nc))
            counts["backtracks"] += 1
            add(f"Back at ({r}, {c}) — un-mark ({nr}, {nc}) so other routes "
                f"can use it, and try the next direction.",
                row=r, col=c, match=False)

    route.append((0, 0))
    on_route.add((0, 0))
    add("The rat starts at (0, 0).", row=0, col=0, match=True)
    solve(0, 0, "")
    route.clear()
    on_route.clear()

    skipped = (f" (the trace shows the first {MAX_STEPS} steps; "
               f"{elided['steps']} more ran silently)" if elided["steps"] else "")
    if paths:
        shown = ", ".join(paths[:8]) + (" …" if len(paths) > 8 else "")
        add(f"Search complete: {len(paths)} route(s){skipped}: {shown}. "
            f"{counts['moves']} moves and {counts['backtracks']} backtracks.",
            match=True, final=True)
    else:
        add(f"Search complete: no route reaches the exit{skipped}. Every "
            f"branch dead-ended and was undone.", match=False, final=True)
    return _result(n, walls, paths, counts, steps)


def _result(n, walls, paths, counts, steps):
    return {
        "meta": {
            "algorithm": "rat_in_maze",
            "view": "grid",
            "language": "python",
            "rows": n,
            "cols": n,
            "blocked": [list(b) for b in sorted(walls)],
            "result": paths[:MAX_PATHS_LISTED],
            "path_count": len(paths),
            "row_labels": [str(r) for r in range(n)],
            "col_labels": [str(c) for c in range(n)],
        },
        "steps": steps,
    }
