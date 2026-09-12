"""Levenshtein edit distance — the DP grid behind spell-checkers.

Same grid shape as LCS so it reuses that renderer, but the recurrence is a
minimum over three neighbours instead of a maximum over two, and the
traceback names the actual edits.
"""

MAX_LEN = 8


def trace(a: str, b: str):
    n, m = len(a), len(b)
    grid = [[None] * (m + 1) for _ in range(n + 1)]
    steps: list = []
    counts = {"cells": 0, "free_matches": 0, "edits_charged": 0}
    path: list = []

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
                "path": [list(p) for p in path],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"How few single-character edits turn '{a}' into '{b}'? Each cell "
        f"answers that for a prefix pair — insert, delete, or substitute.")

    for c in range(m + 1):
        grid[0][c] = c
    for r in range(n + 1):
        grid[r][0] = r
    add(f"Base cases: turning '{a}' into an empty string costs one deletion "
        f"per character, and building '{b}' from empty costs one insertion "
        f"per character.", row=0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            counts["cells"] += 1
            if a[i - 1] == b[j - 1]:
                grid[i][j] = grid[i - 1][j - 1]
                counts["free_matches"] += 1
                add(f"'{a[i - 1]}' already matches '{b[j - 1]}' — no edit "
                    f"needed, carry the diagonal cost {grid[i][j]}.",
                    row=i, col=j, deps=[[i - 1, j - 1]], match=True)
            else:
                sub = grid[i - 1][j - 1]
                dele = grid[i - 1][j]
                ins = grid[i][j - 1]
                grid[i][j] = 1 + min(sub, dele, ins)
                counts["edits_charged"] += 1
                add(f"'{a[i - 1]}' vs '{b[j - 1]}' — one edit required. "
                    f"Cheapest route: 1 + min(substitute {sub}, delete "
                    f"{dele}, insert {ins}) = {grid[i][j]}.",
                    row=i, col=j,
                    deps=[[i - 1, j - 1], [i - 1, j], [i, j - 1]], match=False)

    distance = grid[n][m]
    add(f"Table complete — '{a}' becomes '{b}' in {distance} edit(s). Walk "
        f"back from the corner to name them.", row=n, col=m)

    i, j = n, m
    edits: list[str] = []
    while i > 0 or j > 0:
        path.append([i, j])
        if i > 0 and j > 0 and a[i - 1] == b[j - 1] and grid[i][j] == grid[i - 1][j - 1]:
            add(f"'{a[i - 1]}' was free — step diagonally, no edit.",
                row=i, col=j, match=True)
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and grid[i][j] == grid[i - 1][j - 1] + 1:
            edits.append(f"substitute '{a[i - 1]}'→'{b[j - 1]}'")
            add(f"Substitute '{a[i - 1]}' with '{b[j - 1]}'.", row=i, col=j)
            i -= 1
            j -= 1
        elif i > 0 and grid[i][j] == grid[i - 1][j] + 1:
            edits.append(f"delete '{a[i - 1]}'")
            add(f"Delete '{a[i - 1]}'.", row=i, col=j)
            i -= 1
        else:
            edits.append(f"insert '{b[j - 1]}'")
            add(f"Insert '{b[j - 1]}'.", row=i, col=j)
            j -= 1

    recipe = "; ".join(reversed(edits)) if edits else "nothing — the words match"
    add(f"Traceback done — the {distance}-edit recipe is: {recipe}.")

    return {
        "meta": {
            "algorithm": "edit_distance",
            "view": "grid",
            "language": "python",
            "a": a,
            "b": b,
            "result": distance,
            "row_labels": ["∅"] + list(a),
            "col_labels": ["∅"] + list(b),
        },
        "steps": steps,
    }
