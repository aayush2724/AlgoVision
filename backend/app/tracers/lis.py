"""Longest Increasing Subsequence — the O(n²) DP, made watchable.

For each position, dp[i] is the length of the longest strictly-increasing
subsequence that *ends* at i. It is 1 plus the best dp[j] among all earlier
j whose value is smaller — or just 1 if none qualify. The answer is the
largest dp value anywhere.

Reuses the `grid` view as a two-row table: row 0 is the sequence (shown from
the start), row 1 is dp[i], filled left to right. When a position extends an
earlier one, that predecessor lights up as a dependency; the winning
subsequence lights green via `path` at the end. No new renderer.
"""

MAX_LEN = 10


def trace(nums: list):
    nums = [int(x) for x in nums]
    n = len(nums)
    value_row = [str(v) for v in nums]
    len_row: list = [None] * n
    dp = [1] * n
    prev = [-1] * n
    steps: list = []
    counts = {"positions": 0, "comparisons": 0, "extensions": 0}

    def grid():
        return [value_row[:], len_row[:]]

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

    add("For every position, how long is the longest increasing run that ends "
        "right here? It is 1, plus the best earlier position holding a smaller "
        "value. Scanning back each time is the n² — and it is worth watching.")

    if n == 0:
        add("Empty sequence — the longest increasing subsequence has length 0.",
            match=False)
        return _result(nums, [], 0, steps)

    for i in range(n):
        counts["positions"] += 1
        best_j = -1
        for j in range(i):
            counts["comparisons"] += 1
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                best_j = j
        prev[i] = best_j
        len_row[i] = dp[i]
        if best_j >= 0:
            counts["extensions"] += 1
            add(f"Position {i} (value {nums[i]}) extends position {best_j} "
                f"(value {nums[best_j]}, length {dp[best_j]}) → length {dp[i]}.",
                col=i, deps=[[1, best_j], [0, i]], match=True)
        else:
            add(f"Position {i} (value {nums[i]}) starts fresh — nothing smaller "
                f"before it — so its length is 1.",
                col=i, deps=[[0, i]], match=False)

    # Reconstruct one longest subsequence by following the back-pointers.
    end = max(range(n), key=lambda k: dp[k])
    chain: list[int] = []
    k = end
    while k != -1:
        chain.append(k)
        k = prev[k]
    chain.reverse()

    path = [[0, i] for i in chain]
    values = ", ".join(str(nums[i]) for i in chain)
    add(f"The longest increasing subsequence has length {dp[end]}: {values}. "
        f"Every position was solved once by scanning the positions before it.",
        col=end, path=path, match=True)
    return _result(nums, chain, dp[end], steps)


def _result(nums, chain, length, steps):
    return {
        "meta": {
            "algorithm": "lis",
            "view": "grid",
            "language": "python",
            "rows": 2,
            "cols": len(nums),
            "row_labels": ["seq", "LIS"],
            "col_labels": [str(i) for i in range(len(nums))],
            "subsequence": [nums[i] for i in chain],
            "indices": chain,
            "result": length,
        },
        "steps": steps,
    }
