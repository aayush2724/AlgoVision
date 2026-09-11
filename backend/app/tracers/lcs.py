MAX_LEN = 8


def trace(a: str, b: str):
    """Longest Common Subsequence DP table, with a traceback that reveals it."""
    n, m = len(a), len(b)
    grid = [[None] * (m + 1) for _ in range(n + 1)]
    steps = []
    counts = {"cells": 0, "matches": 0}
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

    add(f"Find the longest subsequence common to '{a}' and '{b}'. Each cell: "
        f"LCS length of the first i chars of one vs the first j of the other.")

    for c in range(m + 1):
        grid[0][c] = 0
    for r in range(n + 1):
        grid[r][0] = 0
    add("Row 0 and column 0 are base cases — against an empty string, "
        "the LCS is empty.", row=0)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            counts["cells"] += 1
            if a[i - 1] == b[j - 1]:
                grid[i][j] = grid[i - 1][j - 1] + 1
                counts["matches"] += 1
                add(f"'{a[i - 1]}' matches '{b[j - 1]}' — extend the diagonal: "
                    f"{grid[i - 1][j - 1]} + 1 = {grid[i][j]}.",
                    row=i, col=j, deps=[[i - 1, j - 1]], match=True)
            else:
                up, left = grid[i - 1][j], grid[i][j - 1]
                grid[i][j] = max(up, left)
                add(f"'{a[i - 1]}' vs '{b[j - 1]}' — no match. Carry the best "
                    f"neighbour: max({up}, {left}) = {grid[i][j]}.",
                    row=i, col=j, deps=[[i - 1, j], [i, j - 1]], match=False)

    # Traceback — walk from the bottom-right corner, collecting the LCS
    i, j = n, m
    chars: list = []
    add(f"Table complete — LCS length is {grid[n][m]}. Now walk back from the "
        f"corner to recover the actual letters.", row=n, col=m)
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            path.append([i, j])
            add(f"'{a[i - 1]}' is part of the LCS — step diagonally.",
                row=i, col=j, match=True)
            i -= 1
            j -= 1
        elif grid[i - 1][j] >= grid[i][j - 1]:
            i -= 1
            add("No match here — follow the larger neighbour upward.",
                row=i, col=j)
        else:
            j -= 1
            add("No match here — follow the larger neighbour leftward.",
                row=i, col=j)

    lcs_str = "".join(reversed(chars))
    add(f"Traceback done — the longest common subsequence is "
        f"'{lcs_str}' (length {grid[n][m]}).")

    return {
        "meta": {
            "algorithm": "lcs",
            "view": "grid",
            "language": "python",
            "a": a,
            "b": b,
            "result": lcs_str,
            "row_labels": ["∅"] + list(a),
            "col_labels": ["∅"] + list(b),
        },
        "steps": steps,
    }
