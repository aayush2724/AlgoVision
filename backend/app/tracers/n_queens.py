"""N-Queens — backtracking made visible.

Placing and *removing* queens is the whole lesson: recursion explores a
branch, hits a dead end, and undoes its last decision. The trace records both
the placements and the retractions so the search tree is legible.
"""

MIN_N = 4
MAX_N = 6
QUEEN = "♛"


def trace(n: int):
    steps: list = []
    counts = {"placements": 0, "conflicts": 0, "backtracks": 0, "solutions": 0}
    # cols[r] = column of the queen in row r, or None
    cols: list = [None] * n
    solution: list = []

    def board():
        g = [[None] * n for _ in range(n)]
        for r, c in enumerate(cols):
            if c is not None:
                g[r][c] = QUEEN
        return g

    def add(note, row=None, col=None, deps=None, match=None, path=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": board(),
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

    def attackers(row, col):
        """Which already-placed queens attack this square."""
        hits = []
        for r in range(row):
            c = cols[r]
            if c == col or abs(c - col) == abs(r - row):
                hits.append([r, c])
        return hits

    add(f"Place {n} queens on a {n}×{n} board so none attack each other. One "
        f"queen per row is forced, so the only question per row is: which "
        f"column?")

    found = False

    def solve(row):
        nonlocal found
        if found:
            return True
        if row == n:
            counts["solutions"] += 1
            found = True
            solution.extend([[r, c] for r, c in enumerate(cols)])
            add(f"All {n} rows filled with no queen attacking another — that "
                f"is a valid solution.", path=solution, match=True)
            return True
        for col in range(n):
            hits = attackers(row, col)
            if hits:
                counts["conflicts"] += 1
                who = hits[0]
                add(f"Row {row}, column {col} is attacked by the queen at row "
                    f"{who[0]}, column {who[1]} — skip it.",
                    row=row, col=col, deps=hits, match=False)
                continue
            cols[row] = col
            counts["placements"] += 1
            add(f"Row {row}, column {col} is safe — place a queen and move to "
                f"row {row + 1}.", row=row, col=col, match=True)
            if solve(row + 1):
                return True
            cols[row] = None
            counts["backtracks"] += 1
            add(f"Row {row + 1} had no safe square at all — take the queen "
                f"back off row {row}, column {col} and try the next column. "
                f"That undo is the 'backtracking'.", row=row, col=col)
        return False

    solve(0)

    if found:
        placed = ", ".join(f"r{r}c{c}" for r, c in solution)
        add(f"Solved: {placed}. It took {counts['placements']} placements, "
            f"{counts['conflicts']} rejected squares and "
            f"{counts['backtracks']} backtracks — brute force would have "
            f"tried {n ** n} boards.", path=solution, match=True)
    else:
        add(f"No arrangement exists for n = {n}.")

    return {
        "meta": {
            "algorithm": "n_queens",
            "view": "grid",
            "language": "python",
            "n": n,
            "solution": solution,
            "row_labels": [str(r) for r in range(n)],
            "col_labels": [str(c) for c in range(n)],
        },
        "steps": steps,
    }
