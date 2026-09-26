"""Find the Minimum in a Rotated Sorted Array — and so the rotation count.

A sorted array of distinct values rotated k times (e.g. 4,5,6,7,0,1,2) has its
minimum at index k. Binary search finds it by comparing mid with the *right
end*: if arr[mid] > arr[high], the drop (and the minimum) is to the right of
mid; otherwise mid itself could be the minimum, so keep it and look left.
O(log n).

Reuses the `array` view with the same low/high/mid window as binary search.
No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def is_rotated_sorted(arr: list) -> bool:
    """Distinct values that are sorted after one rotation."""
    n = len(arr)
    if len(set(arr)) != n:
        return False
    drops = sum(1 for i in range(n) if arr[i] > arr[(i + 1) % n])
    return drops <= 1


def trace(array: list):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0}

    def add(note, low, high, mid=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"low": low, "high": high, "mid": mid,
                           "found": found, "counts": dict(counts)},
            "highlight": {"index": mid},
            "note": note,
        })

    if not arr:
        add("The array is empty — no minimum.", 0, -1, found=False)
        return _result(arr, steps, None)

    low, high = 0, n - 1
    add(f"Find the smallest value. Its index is also how many times the "
        f"sorted array was rotated. Compare the middle with the right end "
        f"of the range 0..{high}.", low, high)

    while low < high:
        mid = (low + high) // 2
        counts["comparisons"] += 1
        if arr[mid] > arr[high]:
            add(f"Middle {_fmt(arr[mid])} (pos {mid}) > right end "
                f"{_fmt(arr[high])} — the drop is to the right of mid, so the "
                f"minimum is in {mid + 1}..{high}.", low, high, mid=mid)
            low = mid + 1
        else:
            add(f"Middle {_fmt(arr[mid])} (pos {mid}) ≤ right end "
                f"{_fmt(arr[high])} — mid..{high} is sorted, so the minimum "
                f"is mid or to its left: keep {low}..{mid}.", low, high, mid=mid)
            high = mid

    add(f"Range closed on position {low}: minimum {_fmt(arr[low])}. The array "
        f"was rotated {low} time(s). {counts['comparisons']} comparisons for "
        f"{n} values — O(log n).", low, high, mid=low, found=True)
    return _result(arr, steps, low)


def _result(arr, steps, idx):
    return {
        "meta": {
            "algorithm": "find_min_rotated",
            "view": "array",
            "language": "python",
            "index": idx,
            "result": arr[idx] if idx is not None else None,
            "rotations": idx,
        },
        "array": arr,
        "steps": steps,
    }
