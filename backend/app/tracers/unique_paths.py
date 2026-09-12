"""Unique paths on a grid — the gentlest possible introduction to DP.

Every cell is the sum of the cell above and the cell to its left, because
those are the only two ways to arrive. Blocked cells make the recurrence feel
earned rather than magic.
"""

MAX_SIDE = 7


def trace(rows: int, cols: int, blocked: list | None = None):
    blocked_set = {(r, c) for r, c in (blocked or [])}
    grid = [[None] * cols for _ in range(rows)]
    steps: list = []
    counts = {"cells": 0, "blocked": 0, "additions": 0}

    def add(note, row=None, col=None, deps=None, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": deps or [],
                "match": match,
                "path": [],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"A robot starts top-left and may only move right or down. How many "
        f"distinct routes reach the bottom-right of this {rows}×{cols} grid? "
        f"Each cell counts the ways to reach *it*."
        + (f" {len(blocked_set)} cell(s) are walls." if blocked_set else ""))

    for r in range(rows):
        for c in range(cols):
            counts["cells"] += 1
            if (r, c) in blocked_set:
                grid[r][c] = 0
                counts["blocked"] += 1
                add(f"({r}, {c}) is a wall — zero routes pass through it.",
                    row=r, col=c, match=False)
                continue
            if r == 0 and c == 0:
                grid[r][c] = 1
                add("The start counts as one route: standing still.",
                    row=r, col=c, match=True)
                continue
            up = grid[r - 1][c] if r > 0 else 0
            left = grid[r][c - 1] if c > 0 else 0
            grid[r][c] = up + left
            counts["additions"] += 1
            deps = []
            if r > 0:
                deps.append([r - 1, c])
            if c > 0:
                deps.append([r, c - 1])
            if r == 0 or c == 0:
                add(f"({r}, {c}) sits on an edge — only one direction leads "
                    f"here, so it inherits {grid[r][c]}.",
                    row=r, col=c, deps=deps)
            else:
                add(f"Arrive at ({r}, {c}) from above ({up}) or from the left "
                    f"({left}) — {up} + {left} = {grid[r][c]}.",
                    row=r, col=c, deps=deps)

    total = grid[rows - 1][cols - 1]
    if total == 0:
        add("The walls seal off the exit — there is no route at all.",
            row=rows - 1, col=cols - 1, match=False)
    else:
        add(f"{total} distinct route(s) reach the corner. Filling "
            f"{counts['cells']} cells once each is O(rows × cols); listing "
            f"every route one by one would be exponential.",
            row=rows - 1, col=cols - 1, match=True)

    return {
        "meta": {
            "algorithm": "unique_paths",
            "view": "grid",
            "language": "python",
            "rows": rows,
            "cols": cols,
            "blocked": [list(b) for b in sorted(blocked_set)],
            "result": total,
            "row_labels": [str(r) for r in range(rows)],
            "col_labels": [str(c) for c in range(cols)],
        },
        "steps": steps,
    }
