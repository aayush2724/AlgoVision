"""Prefix sums — pay O(n) once, then answer any range sum in O(1).

The build is the easy half; the lesson is the query at the end, where a whole
range collapses into a single subtraction.
"""

MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"additions": 0, "query_ops": 0}
    # prefix[i] = sum of arr[0..i-1]; prefix[0] = 0 so every range works.
    prefix = [0.0] * (n + 1)
    shown = [0.0] * n

    def add(note, placed=None, sorted_ranges=None, window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(shown),
                "placed": placed,
                "sorted_ranges": [list(r) for r in (sorted_ranges or [])],
                "merging": list(window) if window else None,
                "prefix": list(prefix),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("An empty array has no prefixes to build.")
        return _result(arr, steps)

    add(f"Original values: {', '.join(_fmt(v) for v in arr)}. Build a running "
        f"total so any range sum becomes one subtraction instead of a loop.")

    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
        shown[i] = prefix[i + 1]
        counts["additions"] += 1
        add(f"prefix[{i + 1}] = prefix[{i}] + {_fmt(arr[i])} = "
            f"{_fmt(prefix[i + 1])} — the total of everything up to index {i}.",
            placed=i, sorted_ranges=[[0, i]])

    add(f"Build done in {counts['additions']} additions. The cells now hold "
        f"running totals, not the original values.",
        sorted_ranges=[[0, n - 1]])

    if n < 2:
        add("With a single element there is no interesting range to query.")
        return _result(arr, steps)

    lo, hi = (1, n - 2) if n >= 3 else (0, n - 1)
    counts["query_ops"] += 1
    total = prefix[hi + 1] - prefix[lo]
    add(f"Now the payoff — sum of range [{lo}..{hi}]. Instead of adding "
        f"{hi - lo + 1} values, take prefix[{hi + 1}] − prefix[{lo}] = "
        f"{_fmt(prefix[hi + 1])} − {_fmt(prefix[lo])} = {_fmt(total)}.",
        window=[lo, hi], sorted_ranges=[[0, n - 1]])
    add(f"One subtraction, no matter how wide the range. That is why prefix "
        f"sums turn many O(n) queries into O(1) each after an O(n) build.",
        window=[lo, hi], sorted_ranges=[[0, n - 1]])
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {"algorithm": "prefix_sums", "view": "array", "language": "python"},
        "array": arr,
        "steps": steps,
    }
