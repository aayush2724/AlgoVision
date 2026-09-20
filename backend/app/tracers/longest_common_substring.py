"""Longest Common Substring — the LCS table's stricter cousin.

Subsequence allows gaps; *substring* does not. So the recurrence changes in
one telling way: a matching pair extends the diagonal (grid[i-1][j-1] + 1),
but a mismatch resets the cell to 0 — a run of shared characters cannot skip
a difference. The answer is the largest value anywhere in the table, not the
bottom-right corner.

Reuses the `grid` view (chars of A × chars of B), exactly like LCS/edit
distance. The winning run lights up green via `path`. No new renderer.
"""

MAX_LEN = 8


def trace(a: str, b: str):
    n, m = len(a), len(b)
    grid = [[0] * (m + 1) for _ in range(n + 1)]
    steps: list = []
    counts = {"cells": 0, "matches": 0, "resets": 0}
    best_len = 0
    best_end = (0, 0)  # (i, j) of the last matching cell of the best run

    def add(note, row=None, col=None, deps=None, match=None, path=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": deps or [],
                "match": match,
                "path": [list(p) for p in (path or [])],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"Find the longest *contiguous* block shared by '{a}' and '{b}'. Each "
        f"cell = the length of the common run ending exactly at these two "
        f"characters. Row 0 and column 0 are 0 — an empty string shares "
        f"nothing.", row=0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            counts["cells"] += 1
            if a[i - 1] == b[j - 1]:
                grid[i][j] = grid[i - 1][j - 1] + 1
                counts["matches"] += 1
                if grid[i][j] > best_len:
                    best_len = grid[i][j]
                    best_end = (i, j)
                add(f"'{a[i - 1]}' matches '{b[j - 1]}' — extend the diagonal "
                    f"run: {grid[i - 1][j - 1]} + 1 = {grid[i][j]}."
                    + (" Longest run so far!" if (i, j) == best_end else ""),
                    row=i, col=j, deps=[[i - 1, j - 1]], match=True)
            else:
                grid[i][j] = 0
                counts["resets"] += 1
                add(f"'{a[i - 1]}' != '{b[j - 1]}' — a substring can't skip a "
                    f"mismatch, so this cell resets to 0.",
                    row=i, col=j, match=False)

    # Recover the winning run by walking the diagonal back from its end.
    path: list = []
    substr = ""
    if best_len:
        i, j = best_end
        while i > 0 and j > 0 and grid[i][j] > 0:
            path.append([i, j])
            substr = a[i - 1] + substr
            i -= 1
            j -= 1
        path.reverse()

    shown = f'"{substr}"' if substr else "empty"
    add(f"Table complete — the longest common substring is {shown} "
        f"(length {best_len}). It is the biggest value anywhere in the grid, "
        f"O(n·m) to fill.",
        row=best_end[0] if best_len else None,
        col=best_end[1] if best_len else None, path=path)
    return _result(a, b, substr, best_len, steps)


def _result(a, b, substr, best_len, steps):
    return {
        "meta": {
            "algorithm": "longest_common_substring",
            "view": "grid",
            "language": "python",
            "a": a,
            "b": b,
            "result": substr,
            "length": best_len,
            "row_labels": ["∅"] + list(a),
            "col_labels": ["∅"] + list(b),
        },
        "steps": steps,
    }
