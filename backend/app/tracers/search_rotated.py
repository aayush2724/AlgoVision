"""Search in a Rotated Sorted Array — binary search that first works out which
half is trustworthy.

A sorted array that has been rotated (e.g. 4,5,6,7,0,1,2) is no longer globally
sorted, so plain binary search breaks. The fix: at each step one half around
mid is still sorted. Detect which — `arr[low] <= arr[mid]` means the left half
is clean — then check whether the target falls inside that sorted half; if so
search it, otherwise search the other. Still O(log n).

Reuses the `array` view with the same low/high/mid window as binary search.
No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], target: float):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0}
    found_at = None

    def add(note, low_, high_, mid=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"low": low_, "high": high_, "mid": mid,
                           "found": found, "counts": dict(counts)},
            "highlight": {"index": mid},
            "note": note,
        })

    if not arr:
        add("The array is empty — nothing to search.", 0, -1, found=False)
        return _result(arr, target, steps)

    low, high = 0, n - 1
    add(f"Search the rotated array for {_fmt(target)}. It isn't globally "
        f"sorted, but around any middle one half always is. Range 0..{high}.",
        low, high)

    while low <= high:
        mid = (low + high) // 2
        counts["comparisons"] += 1
        add(f"Middle is position {mid} = {_fmt(arr[mid])}.", low, high, mid=mid)
        if arr[mid] == target:
            found_at = mid
            add(f"Found it — {_fmt(target)} is at position {mid}.",
                low, high, mid=mid, found=True)
            break
        if arr[low] <= arr[mid]:
            # left half [low..mid] is sorted
            if arr[low] <= target < arr[mid]:
                high = mid - 1
                add(f"Left half {_fmt(arr[low])}..{_fmt(arr[mid])} is sorted and "
                    f"holds {_fmt(target)} — search it. Range {low}..{high}.",
                    low, high, mid=mid)
            else:
                low = mid + 1
                add(f"Left half is sorted but {_fmt(target)} isn't in it — go "
                    f"right. Range {low}..{high}.", low, high, mid=mid)
        else:
            # right half [mid..high] is sorted
            if arr[mid] < target <= arr[high]:
                low = mid + 1
                add(f"Right half {_fmt(arr[mid])}..{_fmt(arr[high])} is sorted and "
                    f"holds {_fmt(target)} — search it. Range {low}..{high}.",
                    low, high, mid=mid)
            else:
                high = mid - 1
                add(f"Right half is sorted but {_fmt(target)} isn't in it — go "
                    f"left. Range {low}..{high}.", low, high, mid=mid)

    if found_at is None:
        add(f"The range is empty — {_fmt(target)} is not in the array.",
            low, high, found=False)
    return _result(arr, target, steps)


def _result(arr, target, steps):
    return {
        "meta": {
            "algorithm": "search_rotated",
            "view": "array",
            "language": "python",
            "target": target,
        },
        "array": arr,
        "steps": steps,
    }
