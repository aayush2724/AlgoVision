MAX_ITEMS = 6
MAX_CAPACITY = 10
MAX_WEIGHT_VALUE = 20


def trace(items: list[tuple], capacity: int):
    """items: [(weight, value), ...]; classic 0/1 knapsack DP table."""
    n = len(items)
    W = int(capacity)
    grid = [[None] * (W + 1) for _ in range(n + 1)]
    steps = []
    counts = {"cells": 0, "takes": 0, "skips": 0}

    def add(note, row=None, col=None, deps=None, choice=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": deps or [],
                "choice": choice,
                "path": [],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"Pack a capacity-{W} bag from {n} items. Each cell answers: best value "
        f"using the first i items with capacity c?")

    for c in range(W + 1):
        grid[0][c] = 0
    add("Row 0 is the base case — with no items, every capacity holds value 0.",
        row=0)

    for i in range(1, n + 1):
        w, v = items[i - 1]
        for c in range(W + 1):
            counts["cells"] += 1
            if w > c:
                grid[i][c] = grid[i - 1][c]
                counts["skips"] += 1
                add(f"Item {i} (weight {w}) doesn't fit in capacity {c} — "
                    f"copy the answer from above: {grid[i][c]}.",
                    row=i, col=c, deps=[[i - 1, c]], choice="skip")
            else:
                skip_v = grid[i - 1][c]
                take_v = grid[i - 1][c - w] + v
                if take_v > skip_v:
                    grid[i][c] = take_v
                    counts["takes"] += 1
                    add(f"Capacity {c}: take item {i} (value {v} + best of "
                        f"remaining {c - w} = {take_v}) beats skipping ({skip_v}).",
                        row=i, col=c, deps=[[i - 1, c], [i - 1, c - w]],
                        choice="take")
                else:
                    grid[i][c] = skip_v
                    counts["skips"] += 1
                    add(f"Capacity {c}: skipping item {i} ({skip_v}) is at least "
                        f"as good as taking it ({take_v}).",
                        row=i, col=c, deps=[[i - 1, c], [i - 1, c - w]],
                        choice="skip")

    best = grid[n][W]
    add(f"Table complete — the bottom-right cell holds the answer: best value "
        f"{best} for capacity {W}. {counts['cells']} subproblems, each solved once.",
        row=n, col=W)

    return {
        "meta": {
            "algorithm": "knapsack_01",
            "view": "grid",
            "language": "python",
            "capacity": W,
            "result": best,
            "row_labels": ["no items"] + [f"w{w}·v{v}" for w, v in items],
            "col_labels": [str(c) for c in range(W + 1)],
        },
        "steps": steps,
    }
