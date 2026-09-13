"""Matrix-chain multiplication — where to put the parentheses so the chain of
matrix products costs the fewest scalar multiplications.

Interval DP: dp[i][j] is the cheapest way to multiply matrices i..j. For every
split point k the cost is dp[i][k] + dp[k+1][j] plus the price of the one
multiplication that joins the two halves. The grid fills diagonal by diagonal
— short chains first — because every longer chain is built from shorter ones
already solved.

Reuses the `grid` view: rows and columns are matrix indices, the upper triangle
holds dp[i][j], and the two sub-chains a split reads light up as dependencies.
No new renderer.
"""

MAX_MATRICES = 6


def trace(dims: list):
    # dims has n+1 entries; matrix m has shape dims[m] x dims[m+1].
    p = [int(x) for x in dims]
    n = len(p) - 1
    grid: list = [[None] * n for _ in range(n)]
    dp = [[0] * n for _ in range(n)]
    steps: list = []
    counts = {"cells": 0, "splits_tried": 0}

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

    add(f"{n} matrix(es) in a chain. dp[i][j] is the fewest scalar "
        f"multiplications to multiply matrices i..j. Short chains are solved "
        f"first, because every long one is split into two shorter ones.")

    # Diagonal: a single matrix costs nothing to "multiply".
    for i in range(n):
        grid[i][i] = 0
        counts["cells"] += 1
    add("A chain of one matrix costs 0 — fill the diagonal.", row=0, col=0,
        match=True)

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = None
            best_k = i
            for k in range(i, j):
                counts["splits_tried"] += 1
                cost = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if best is None or cost < best:
                    best = cost
                    best_k = k
            dp[i][j] = best
            grid[i][j] = best
            counts["cells"] += 1
            add(f"Matrices {i}..{j}: the cheapest split is after matrix "
                f"{best_k} — dp[{i}][{best_k}] + dp[{best_k + 1}][{j}] + "
                f"{p[i]}·{p[best_k + 1]}·{p[j + 1]} = {best}.",
                row=i, col=j, deps=[[i, best_k], [best_k + 1, j]], match=True)

    result = dp[0][n - 1] if n else 0
    add(f"The whole chain costs {result} scalar multiplications at best. "
        f"Filling {counts['cells']} cells once — O(n³) over "
        f"{counts['splits_tried']} split(s) tried — beats the exponential "
        f"number of ways to parenthesise by hand.",
        row=0, col=n - 1, match=True)

    return {
        "meta": {
            "algorithm": "matrix_chain",
            "view": "grid",
            "language": "python",
            "rows": n,
            "cols": n,
            "row_labels": [f"M{i}" for i in range(n)],
            "col_labels": [f"M{j}" for j in range(n)],
            "dims": p,
            "result": result,
        },
        "steps": steps,
    }
