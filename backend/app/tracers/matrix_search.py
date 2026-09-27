"""Binary search in a 2-D matrix — three shapes of the same idea.

* search_2d_matrix — rows sorted and each row starts after the previous one
  ends, so the matrix is one sorted list read row by row. Binary-search a
  flat index 0..R·C−1 and turn it into (index // C, index % C).
* search_2d_matrix_ii — rows and columns sorted independently. Start at the
  top-right corner: bigger than x → that whole column is too big, step left;
  smaller → that whole row is too small, step down. O(R + C).
* row_max_ones — each row is sorted 0s then 1s. Per row, binary-search the
  first 1 (a lower bound); the row with the earliest first 1 has the most.

Reuses the `grid` view: the live search region is tinted (`deps`), the probed
cell is `row`/`col`, and the answer cell(s) light green (`path`).
"""

TITLES = {
    "search_2d_matrix": "Search in a Sorted 2D Matrix",
    "search_2d_matrix_ii": "Search in a Row/Column-Sorted Matrix",
    "row_max_ones": "Row With Maximum 1s",
}
MAX_SIDE = 6


def parse(text):
    rows = [r for r in (text or "").replace(" ", "").split("/") if r]
    try:
        return [[int(v) for v in r.split(",") if v != ""] for r in rows]
    except ValueError:
        return None


def validate(algo, grid, target):
    if not grid or not grid[0]:
        return "Give rows separated by '/', values by ',' — e.g. 1,3,5/7,9,11."
    if len(grid) > MAX_SIDE or any(len(r) != len(grid[0]) for r in grid) \
            or len(grid[0]) > MAX_SIDE:
        return f"The matrix must be rectangular, at most {MAX_SIDE}×{MAX_SIDE}."
    if any(abs(v) > 999 for r in grid for v in r):
        return "Keep values within ±999."
    flat = [v for r in grid for v in r]
    if algo == "search_2d_matrix":
        if any(b < a for a, b in zip(flat, flat[1:])):
            return "Read row by row, the values must never decrease."
    elif algo == "search_2d_matrix_ii":
        if any(b < a for r in grid for a, b in zip(r, r[1:])) or \
                any(grid[i + 1][j] < grid[i][j] for i in range(len(grid) - 1)
                    for j in range(len(grid[0]))):
            return "Every row and every column must be sorted ascending."
    else:
        if any(v not in (0, 1) for v in flat):
            return "Only 0s and 1s."
        if any(b < a for r in grid for a, b in zip(r, r[1:])):
            return "Each row must be its 0s followed by its 1s."
    if algo != "row_max_ones" and target is None:
        return "Give a target X to search for."
    return None


def trace(algo, grid, target=None):
    R, C = len(grid), len(grid[0])
    steps: list = []
    counts = {"comparisons": 0}

    def add(note, row=None, col=None, live=(), found=(), match=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"grid": [r[:] for r in grid], "row": row,
                                     "col": col, "deps": [list(c) for c in live],
                                     "match": match,
                                     "path": [list(c) for c in found],
                                     "counts": dict(counts)},
                      "highlight": {"index": col}, "note": note})

    meta_extra = {}
    if algo == "search_2d_matrix":
        x = target
        lo, hi = 0, R * C - 1

        def cells(a, b):
            return [(i // C, i % C) for i in range(a, b + 1)]

        add(f"Read row by row, this {R}×{C} matrix is one sorted list of "
            f"{R * C}. Binary-search the flat index 0..{hi}; index i lives at "
            f"row i // {C}, column i % {C}.", live=cells(lo, hi))
        result = False
        while lo <= hi:
            mid = (lo + hi) // 2
            r, c = divmod(mid, C)
            counts["comparisons"] += 1
            v = grid[r][c]
            if v == x:
                add(f"Index {mid} → ({r}, {c}) holds {v} — found.", r, c,
                    cells(lo, hi), [(r, c)], True)
                result = True
                break
            if v < x:
                add(f"Index {mid} → ({r}, {c}) holds {v} < {x:g} — search "
                    f"{mid + 1}..{hi}.", r, c, cells(lo, hi), match=False)
                lo = mid + 1
            else:
                add(f"Index {mid} → ({r}, {c}) holds {v} > {x:g} — search "
                    f"{lo}..{mid - 1}.", r, c, cells(lo, hi), match=False)
                hi = mid - 1
        if not result:
            add(f"The range is empty — {x:g} is not in the matrix. "
                f"{counts['comparisons']} comparisons for {R * C} cells.")
    elif algo == "search_2d_matrix_ii":
        x = target
        r, c = 0, C - 1

        def region():
            return [(i, j) for i in range(r, R) for j in range(0, c + 1)]

        add("Rows and columns are each sorted. Stand at the top-right corner: "
            "everything left is smaller, everything below is bigger.",
            live=region())
        result = False
        while r < R and c >= 0:
            counts["comparisons"] += 1
            v = grid[r][c]
            if v == x:
                add(f"({r}, {c}) holds {v} — found.", r, c, region(), [(r, c)], True)
                result = True
                break
            if v > x:
                add(f"({r}, {c}) holds {v} > {x:g} — the rest of column {c} is "
                    f"even bigger. Drop the column, step left.", r, c, region(),
                    match=False)
                c -= 1
            else:
                add(f"({r}, {c}) holds {v} < {x:g} — the rest of row {r} is even "
                    f"smaller. Drop the row, step down.", r, c, region(),
                    match=False)
                r += 1
        if not result:
            add(f"Walked off the matrix — {x:g} is not there. "
                f"{counts['comparisons']} comparisons, at most R + C = {R + C}.")
    else:
        best_row, best_count = -1, 0

        def best_cells():
            return ([(best_row, j) for j in range(C - best_count, C)]
                    if best_row >= 0 else [])

        add("Each row is 0s then 1s. Per row, binary-search the first 1 — "
            "the count of 1s is the columns from there to the end.")
        for i in range(R):
            lo, hi, first = 0, C - 1, C
            while lo <= hi:
                mid = (lo + hi) // 2
                counts["comparisons"] += 1
                live = [(i, j) for j in range(lo, hi + 1)]
                if grid[i][mid] == 1:
                    first = mid
                    add(f"Row {i}: column {mid} is 1 — the first 1 is here or "
                        f"to the left.", i, mid, live, best_cells(), True)
                    hi = mid - 1
                else:
                    add(f"Row {i}: column {mid} is 0 — the first 1 is to the "
                        f"right.", i, mid, live, best_cells(), False)
                    lo = mid + 1
            ones = C - first
            if ones > best_count:
                best_row, best_count = i, ones
            add(f"Row {i} has {ones} one(s). Best so far: "
                + (f"row {best_row} with {best_count}." if best_row >= 0
                   else "no 1s yet."), found=best_cells())
        result = best_row
        meta_extra["count"] = best_count
        add(f"Row with the most 1s: {best_row if best_row >= 0 else 'none'}"
            + (f" ({best_count})" if best_row >= 0 else "")
            + f". {counts['comparisons']} probes — O(R log C) instead of R·C.",
            found=best_cells())
    return {"meta": {"algorithm": algo, "view": "grid", "language": "python",
                     "result": result, **meta_extra,
                     "row_labels": [str(r) for r in range(R)],
                     "col_labels": [str(c) for c in range(C)]},
            "steps": steps}
