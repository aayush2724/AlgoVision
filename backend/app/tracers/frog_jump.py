"""Frog Jump — the classic 1-D DP where each state has two choices.

A frog crosses a row of stones of different heights. From stone i it may hop
to i+1 or i+2, paying the height difference in energy. The cheapest way to
reach stone i is: dp[i] = min(dp[i-1] + |h[i]-h[i-1]|, dp[i-2] + |h[i]-h[i-2]|).

Reuses the `grid` view as a two-row table (row 0 = stone heights, row 1 = the
cheapest energy to reach each stone, filled left to right). The stones the
frog actually lands on light up green via `path`. No new renderer.
"""

MAX_STONES = 10


def trace(heights: list):
    h = [int(x) for x in heights]
    n = len(h)
    height_row = [str(v) for v in h]
    cost_row: list = [None] * n
    dp = [0] * n
    steps: list = []
    counts = {"stones": 0, "one_hops": 0, "two_hops": 0}

    def grid():
        return [height_row[:], cost_row[:]]

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

    add("A frog crosses stones of different heights, hopping one or two "
        "stones at a time and paying the height difference each hop. Row 1 "
        "fills with the cheapest energy to reach each stone.")

    if n == 0:
        add("No stones — nothing to cross.", match=False)
        return _result(h, [], 0, steps)

    dp[0] = 0
    cost_row[0] = 0
    counts["stones"] += 1
    add("Stone 0 is the start — it costs 0 energy to be here.", col=0,
        deps=[[0, 0]], match=True)

    for i in range(1, n):
        counts["stones"] += 1
        one = dp[i - 1] + abs(h[i] - h[i - 1])
        two = dp[i - 2] + abs(h[i] - h[i - 2]) if i >= 2 else None
        deps = [[0, i], [1, i - 1]]
        if i >= 2:
            deps.append([1, i - 2])
        if two is not None and two < one:
            dp[i] = two
            counts["two_hops"] += 1
            add(f"Stone {i}: a two-stone hop from {i - 2} costs {two}, cheaper "
                f"than the one-stone hop ({one}). Best: {dp[i]}.",
                col=i, deps=deps, match=True)
        else:
            dp[i] = one
            counts["one_hops"] += 1
            extra = f" (two-hop would cost {two})" if two is not None else ""
            add(f"Stone {i}: a one-stone hop from {i - 1} costs {one}{extra}. "
                f"Best: {dp[i]}.", col=i, deps=deps, match=True)
        cost_row[i] = dp[i]

    # Walk back through the same comparisons to recover the frog's route.
    route: list[int] = []
    i = n - 1
    while i > 0:
        route.append(i)
        one = dp[i - 1] + abs(h[i] - h[i - 1])
        two = dp[i - 2] + abs(h[i] - h[i - 2]) if i >= 2 else None
        if two is not None and dp[i] == two:
            i -= 2
        else:
            i -= 1
    route.append(0)
    route.reverse()

    path = [[0, s] for s in route]
    add(f"Cheapest crossing costs {dp[n - 1]} energy, landing on stones "
        f"{', '.join(map(str, route))}. Each stone was decided once — O(n).",
        col=n - 1, path=path, match=True)
    return _result(h, route, dp[n - 1], steps)


def _result(heights, route, best, steps):
    return {
        "meta": {
            "algorithm": "frog_jump",
            "view": "grid",
            "language": "python",
            "rows": 2,
            "cols": len(heights),
            "row_labels": ["height", "energy"],
            "col_labels": [str(i) for i in range(len(heights))],
            "route": route,
            "result": best,
        },
        "steps": steps,
    }
