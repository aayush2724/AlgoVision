"""House Robber — the gentlest 1-D DP with a real choice at every step.

A burglar walks a street of houses, each holding some loot, but the alarms
are wired so two *adjacent* houses can never both be robbed. At each house
the only decision is: skip it and keep last house's best, or rob it and add
its loot to the best from two houses back. dp[i] = max(dp[i-1],
nums[i] + dp[i-2]).

Reuses the `grid` view as a two-row table: row 0 is the loot on the street
(shown from the start), row 1 is the running best, filled left to right. The
final robbed houses light up green via `path`. No new renderer.
"""

MAX_HOUSES = 10


def trace(nums: list):
    nums = [int(x) for x in nums]
    n = len(nums)
    loot_row = [str(v) for v in nums]
    best_row: list = [None] * n
    dp = [0] * n
    steps: list = []
    counts = {"houses": 0, "robs": 0, "skips": 0}

    def grid():
        return [loot_row[:], best_row[:]]

    def add(note, col=None, deps=None, path=None, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": grid(),
                "row": 1 if col is not None else None,
                "col": col,
                "deps": deps or [],
                "match": match,
                "path": path or [],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add("A street of houses, each holding some loot — but robbing two houses "
        "next door to each other trips the alarm. At each house the choice is "
        "only: skip it, or rob it and add the best from two houses back.")

    if n == 0:
        add("No houses — nothing to rob.", match=False)
        return _result(nums, [], 0, steps)

    for i in range(n):
        counts["houses"] += 1
        skip = dp[i - 1] if i >= 1 else 0
        take = nums[i] + (dp[i - 2] if i >= 2 else 0)
        deps = []
        if i >= 1:
            deps.append([1, i - 1])
        if i >= 2:
            deps.append([1, i - 2])
        deps.append([0, i])
        if take >= skip:
            dp[i] = take
            counts["robs"] += 1
            back = f" + best from house {i - 2} ({dp[i - 2]})" if i >= 2 else ""
            add(f"House {i}: robbing it gives {nums[i]}{back} = {take}, which "
                f"beats skipping ({skip}). Best so far: {dp[i]}.",
                col=i, deps=deps, match=True)
        else:
            dp[i] = skip
            counts["skips"] += 1
            add(f"House {i}: robbing gives {take}, but skipping keeps the "
                f"better {skip}. Best so far: {dp[i]}.",
                col=i, deps=deps, match=False)
        best_row[i] = dp[i]

    # Reconstruct which houses were actually robbed, walking back through the
    # same comparisons — this is the answer, not just the number.
    robbed: list[int] = []
    i = n - 1
    while i >= 0:
        take = nums[i] + (dp[i - 2] if i >= 2 else 0)
        skip = dp[i - 1] if i >= 1 else 0
        if take >= skip:
            robbed.append(i)
            i -= 2
        else:
            i -= 1
    robbed.reverse()

    path = [[0, i] for i in robbed]
    add(f"The best haul is {dp[n - 1]}, robbing house(s) "
        f"{', '.join(map(str, robbed)) or 'none'} — none of them adjacent. "
        f"Each house was decided once, so this is O(n).",
        col=n - 1, path=path, match=True)
    return _result(nums, robbed, dp[n - 1], steps)


def _result(nums, robbed, best, steps):
    return {
        "meta": {
            "algorithm": "house_robber",
            "view": "grid",
            "language": "python",
            "rows": 2,
            "cols": len(nums),
            "row_labels": ["loot", "best"],
            "col_labels": [str(i) for i in range(len(nums))],
            "robbed": robbed,
            "result": best,
        },
        "steps": steps,
    }
