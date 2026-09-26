"""Find a Peak Element — binary search on an *unsorted* array.

A peak is bigger than its neighbours (the ends count as −∞ outside the array).
No sorting needed: look at mid and its right neighbour. If the slope goes up
(arr[mid] < arr[mid+1]) a peak must exist to the right — you are climbing and
the array must come down eventually. Otherwise a peak is at mid or to its
left. Halve and repeat: O(log n). Requires no two equal neighbours.

Reuses the `array` view with the same low/high/mid window as binary search.
No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


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
        add("The array is empty — no peak.", 0, -1, found=False)
        return _result(arr, steps, None)

    low, high = 0, n - 1
    add(f"Find any value bigger than both neighbours (outside the array "
        f"counts as −∞). The array isn't sorted — the slope at the middle "
        f"still tells you which half must hold a peak.", low, high)

    while low < high:
        mid = (low + high) // 2
        counts["comparisons"] += 1
        if arr[mid] < arr[mid + 1]:
            add(f"{_fmt(arr[mid])} (pos {mid}) < {_fmt(arr[mid + 1])} to its "
                f"right — uphill. Keep climbing: a peak is in "
                f"{mid + 1}..{high}.", low, high, mid=mid)
            low = mid + 1
        else:
            add(f"{_fmt(arr[mid])} (pos {mid}) > {_fmt(arr[mid + 1])} to its "
                f"right — downhill. A peak is at mid or to its left: "
                f"{low}..{mid}.", low, high, mid=mid)
            high = mid

    add(f"Range closed on position {low}: {_fmt(arr[low])} is a peak. "
        f"{counts['comparisons']} comparisons for {n} values — O(log n), "
        f"without ever sorting.", low, high, mid=low, found=True)
    return _result(arr, steps, low)


def _result(arr, steps, idx):
    return {
        "meta": {
            "algorithm": "find_peak",
            "view": "array",
            "language": "python",
            "result": idx,
            "value": arr[idx] if idx is not None else None,
        },
        "array": arr,
        "steps": steps,
    }
