"""Dutch National Flag — sort an array of 0s, 1s and 2s in one pass.

Three pointers carve the array into four regions: [0..low-1] are settled 0s,
[low..mid-1] are settled 1s, [mid..high] is unknown, [high+1..n-1] are settled
2s. Read arr[mid]: a 0 swaps down to the low boundary (both advance); a 1 is
already home (mid advances); a 2 swaps up to the high boundary (high retreats,
mid stays to re-check what arrived). One pass, no counting, in place.

Reuses the `array` view: settled 0s and 2s show green (`sorted_ranges`), the
unknown middle is the active window, and `mid` is the highlighted cell.
No new renderer.
"""

MAX_LEN = 16


def trace(nums: list):
    arr = [int(x) for x in nums]
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0, "swaps": 0}

    def settled():
        # green regions: the finalised 0s on the left, the finalised 2s on the
        # right. (Middle 1s are only truly settled at the very end.)
        ranges = []
        if low > 0:
            ranges.append([0, low - 1])
        if high < n - 1:
            ranges.append([high + 1, n - 1])
        return ranges

    def add(note, placed=None, done=False):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "sorted_ranges": ([[0, n - 1]] if done else settled()),
                "merging": None if done else [low, high],
                "placed": placed,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    low = mid = 0
    high = n - 1

    if not arr:
        add("An empty array is already sorted.", done=True)
        return _result(arr, steps)

    add("Sort 0s, 1s and 2s in one pass. low tracks the end of the 0s, high "
        "the start of the 2s; mid scans the unknown middle.", placed=mid)

    while mid <= high:
        counts["comparisons"] += 1
        v = arr[mid]
        if v == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            counts["swaps"] += 1
            add(f"arr[{mid}] = 0 — swap it down to the 0s region (position "
                f"{low}); advance both low and mid.", placed=mid)
            low += 1
            mid += 1
        elif v == 1:
            add(f"arr[{mid}] = 1 — already in the middle region; just advance "
                f"mid.", placed=mid)
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            counts["swaps"] += 1
            add(f"arr[{mid}] = 2 — swap it up to the 2s region (position "
                f"{high}); retreat high and re-check what landed at mid.",
                placed=mid)
            high -= 1

    add(f"Done in one pass — {counts['swaps']} swap(s). Every 0 then 1 then 2, "
        f"sorted in place with no counting.", done=True)
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {
            "algorithm": "dutch_flag",
            "view": "array",
            "language": "python",
            "result": arr,
        },
        "array": arr,
        "steps": steps,
    }
