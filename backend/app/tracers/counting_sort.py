"""Counting sort — the sort that never compares two values.

Values must be small non-negative integers; the router enforces that. The
payoff for students is seeing O(n + k) beat O(n log n) by *counting* instead
of comparing, and seeing why k (the value range) is the hidden cost.
"""

MAX_ARRAY_LEN = 16
MAX_VALUE = 20


def trace(array: list[int]):
    arr = [int(v) for v in array]
    n = len(arr)
    steps: list = []
    counts = {"tallies": 0, "writes": 0, "comparisons": 0}
    work = list(arr)

    def add(note, placed=None, sorted_ranges=None, buckets=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(work),
                "placed": placed,
                "sorted_ranges": [list(r) for r in (sorted_ranges or [])],
                "buckets": list(buckets) if buckets is not None else None,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("An empty array is already sorted.")
        return _result(arr, steps)

    k = max(arr) + 1
    tally = [0] * k

    add(f"Counting sort never compares two values. Instead it tallies how many "
        f"times each value appears, then rebuilds the array in order. "
        f"Values here run 0..{k - 1}, so we need {k} buckets.",
        buckets=tally)

    for idx, v in enumerate(arr):
        tally[v] += 1
        counts["tallies"] += 1
        add(f"Saw {v} at index {idx} — bucket {v} is now {tally[v]}.",
            placed=idx, buckets=tally)

    add(f"Every value tallied in one pass: {_describe(tally)}. "
        f"That is the O(n) half of the cost.", buckets=tally)

    out_i = 0
    for value in range(k):
        if tally[value] == 0:
            add(f"No {value}s in the input — skip that bucket.", buckets=tally)
            continue
        for _ in range(tally[value]):
            work[out_i] = value
            counts["writes"] += 1
            add(f"Bucket {value} still has stock — write {value} into "
                f"position {out_i}.",
                placed=out_i, sorted_ranges=[[0, out_i]], buckets=tally)
            out_i += 1

    add(f"Array rebuilt in {counts['writes']} writes with {counts['comparisons']} "
        f"comparisons — none. Cost was O(n + k) = O({n} + {k}); when k dwarfs n, "
        f"a comparison sort wins instead.",
        sorted_ranges=[[0, n - 1]], buckets=tally)
    return _result(work, steps)


def _describe(tally):
    parts = [f"{v}×{c}" for v, c in enumerate(tally) if c]
    return ", ".join(parts)


def _result(arr, steps):
    return {
        "meta": {"algorithm": "counting_sort", "view": "array", "language": "python"},
        "array": arr,
        "steps": steps,
    }
