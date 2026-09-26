"""Word Search — can a word be traced through adjacent letters of a grid?

Try every cell as a starting letter. From there, depth-first search extends
the word one letter at a time into an up/left/right/down neighbour that
matches the next letter and is not already used on this path. A mismatch or a
dead end undoes the last letter and tries another direction — backtracking.
The same cell may be reused by *other* attempts, just never twice in one.

Reuses the `grid` view: the letter grid is `structures.grid`, the letters
matched so far light green via `path`, and the cell being tested is
`row`/`col` (green if it matches, orange if not). No new renderer.

A grid of repeated letters can branch a lot, so the trace records the first
MAX_STEPS steps and then finishes the search silently; the final step always
states the true answer.
"""

MAX_SIDE = 5
MAX_WORD = 8
MAX_STEPS = 300
MOVES = [(-1, 0), (0, -1), (0, 1), (1, 0)]
MOVE_NAME = {(-1, 0): "up", (0, -1): "left", (0, 1): "right", (1, 0): "down"}


def trace(board: list, word: str):
    grid = [list(row) for row in board]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    steps: list = []
    counts = {"cells_tried": 0, "mismatches": 0, "backtracks": 0}
    path: list = []
    on_path: set = set()
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
                "path": [list(p) for p in path],
                "counts": dict(counts),
            },
            # A cell, not an array index — the library scene would otherwise
            # narrate the bare column number as if it were the position.
            "highlight": {"cell": [row, col] if row is not None else None},
            "note": note,
        })

    add(f"Find \"{word}\" in this {rows}×{cols} grid by walking between "
        f"up/down/left/right neighbours, using each cell at most once per "
        f"attempt. Try every cell as the first letter.")

    def dfs(r, c, k):
        """(r, c) already matches word[k] and sits on the path."""
        if k == len(word) - 1:
            return True
        need = word[k + 1]
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or (nr, nc) in on_path:
                continue
            counts["cells_tried"] += 1
            got = grid[nr][nc]
            if got != need:
                counts["mismatches"] += 1
                add(f"{MOVE_NAME[(dr, dc)].capitalize()} of ({r}, {c}) is "
                    f"'{got}', but letter {k + 2} must be '{need}' — no.",
                    row=nr, col=nc, match=False)
                continue
            path.append((nr, nc))
            on_path.add((nr, nc))
            add(f"{MOVE_NAME[(dr, dc)].capitalize()} of ({r}, {c}) is "
                f"'{need}' — matched \"{word[:k + 2]}\" so far.",
                row=nr, col=nc, match=True)
            if dfs(nr, nc, k + 1):
                return True
            path.pop()
            on_path.discard((nr, nc))
            counts["backtracks"] += 1
            add(f"Dead end after \"{word[:k + 2]}\" — release ({nr}, {nc}) "
                f"and try another direction from ({r}, {c}).",
                row=r, col=c, match=False)
        return False

    found = False
    for r in range(rows):
        for c in range(cols):
            counts["cells_tried"] += 1
            if grid[r][c] != word[0]:
                counts["mismatches"] += 1
                add(f"({r}, {c}) is '{grid[r][c]}', not '{word[0]}' — it can't "
                    f"start the word.", row=r, col=c, match=False)
                continue
            path.append((r, c))
            on_path.add((r, c))
            add(f"({r}, {c}) is '{word[0]}' — start a path here.",
                row=r, col=c, match=True)
            if dfs(r, c, 0):
                found = True
                break
            path.pop()
            on_path.discard((r, c))
            counts["backtracks"] += 1
            add(f"No way to finish from ({r}, {c}) — abandon this start.",
                row=r, col=c, match=False)
        if found:
            break

    skipped = (f" (the trace shows the first {MAX_STEPS} steps; "
               f"{elided['steps']} more ran silently)" if elided["steps"] else "")
    if found:
        cells = " → ".join(f"({r}, {c})" for r, c in path)
        add(f"Found \"{word}\": {cells}{skipped}. {counts['backtracks']} "
            f"backtrack(s) along the way.", match=True, final=True)
    else:
        path.clear()
        add(f"\"{word}\" is not in the grid{skipped} — every start and every "
            f"branch was tried and undone.", match=False, final=True)

    return {
        "meta": {
            "algorithm": "word_search",
            "view": "grid",
            "language": "python",
            "word": word,
            "result": found,
            "path": [list(p) for p in path] if found else [],
            "row_labels": [str(r) for r in range(rows)],
            "col_labels": [str(c) for c in range(cols)],
        },
        "steps": steps,
    }
