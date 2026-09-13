"""Subset Sum — can any subset of these numbers hit an exact target?

The classic boolean DP: dp[i][s] is true when some subset of the first i
numbers adds up to exactly s. Each row either ignores the new number (inherit
the cell straight above) or uses it (look back w columns in the row above).
The answer lives in the bottom-right corner.

Reuses the `grid` view exactly like 0/1 knapsack: rows are items (with an
empty-set base row on top), columns are sums 0..target, and each cell shows
✓ (reachable) or · (not). The two cells a decision reads light up as
dependencies; the subset that proves the target lights green via `path`. No
new renderer.
"""

YES = "✓"
NO = "·"

MAX_ITEMS = 6
MAX_TARGET = 12
MAX_VALUE = 12


def trace(nums: list, target: int):
    nums = [int(x) for x in nums]
    target = int(target)
    n = len(nums)
    # (n + 1) rows × (target + 1) cols, all unknown (None) until computed.
    grid: list = [[None] * (target + 1) for _ in range(n + 1)]
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    steps: list = []
    counts = {"cells": 0, "reachable": 0, "uses_item": 0}

    def add(note, row=None, col=None, deps=None, path=None, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in grid],
                "row": row,
                "col": col,
                "deps": deps or [],
                "match": match,
                "path": path or [],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"Can any subset of these {n} number(s) add up to exactly {target}? "
        f"dp[i][s] is true when the first i numbers can make sum s. Each cell "
        f"either ignores the new number or spends it.")

    # Base row: the empty set makes only 0.
    dp[0][0] = True
    for s in range(target + 1):
        grid[0][s] = YES if dp[0][s] else NO
        counts["cells"] += 1
        if dp[0][s]:
            counts["reachable"] += 1
    add("Row 0 is the empty set: it can make a sum of 0 and nothing else.",
        row=0, col=0, match=True)

    for i in range(1, n + 1):
        w = nums[i - 1]
        for s in range(target + 1):
            counts["cells"] += 1
            skip = dp[i - 1][s]
            take = s >= w and dp[i - 1][s - w]
            dp[i][s] = skip or take
            grid[i][s] = YES if dp[i][s] else NO
            deps = [[i - 1, s]]
            if take:
                counts["uses_item"] += 1
                deps.append([i - 1, s - w])
            if dp[i][s]:
                counts["reachable"] += 1
            if take and not skip:
                add(f"Sum {s}: not reachable without {w}, but reachable by "
                    f"adding {w} to sum {s - w}. ✓", row=i, col=s, deps=deps,
                    match=True)
            elif skip:
                add(f"Sum {s}: already reachable without {w}, so it stays ✓.",
                    row=i, col=s, deps=deps, match=True)
            else:
                add(f"Sum {s}: unreachable with or without {w}. ·",
                    row=i, col=s, deps=deps, match=False)

    ok = dp[n][target]
    # Recover one witnessing subset by walking the take/skip choices back up.
    subset: list[int] = []
    path: list = []
    if ok:
        i, s = n, target
        path.append([i, s])
        while i > 0:
            if dp[i - 1][s]:            # we skipped item i
                i -= 1
            else:                       # we must have taken it
                w = nums[i - 1]
                subset.append(w)
                s -= w
                i -= 1
            path.append([i, s])
        subset.reverse()

    if ok:
        add(f"The corner is ✓: {' + '.join(map(str, subset))} = {target}. "
            f"Filling {counts['cells']} cells once is O(n × target) — far "
            f"cheaper than trying all 2^{n} subsets.",
            row=n, col=target, path=path, match=True)
    else:
        add(f"The corner is ·: no subset of these numbers sums to {target}. "
            f"The table proved it in O(n × target) without listing a single "
            f"subset.", row=n, col=target, match=False)

    return {
        "meta": {
            "algorithm": "subset_sum",
            "view": "grid",
            "language": "python",
            "rows": n + 1,
            "cols": target + 1,
            "row_labels": ["∅"] + [str(v) for v in nums],
            "col_labels": [str(s) for s in range(target + 1)],
            "target": target,
            "subset": subset,
            "result": ok,
        },
        "steps": steps,
    }
