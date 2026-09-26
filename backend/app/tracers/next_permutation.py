"""Next Permutation — rearrange the numbers into the next larger arrangement.

Three moves, all in place. (1) Scan from the right for the first "dip" — the
pivot i where arr[i] < arr[i+1]; everything to its right is descending and
already maximal. (2) In that descending tail, find the smallest value still
bigger than the pivot and swap them — the smallest possible bump. (3) The tail
is still descending, so reverse it into ascending order — the smallest suffix.
If there is no pivot, the array was the last permutation, so reversing the
whole thing wraps to the first.

Reuses the `array` view: the active cell is `placed`, the tail being reversed
is the window (`merging`), and the finished array shows green (`sorted_ranges`).
No new renderer.
"""

MAX_LEN = 12


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(nums: list):
    arr = list(nums)
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0, "swaps": 0}

    def add(note, placed=None, window=None, done=False):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "merging": window,
                "sorted_ranges": [[0, n - 1]] if done else [],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n < 2:
        add("Fewer than two numbers — only one arrangement exists.", done=True)
        return _result(arr, steps)

    add("Find the next-larger arrangement in place. Step 1: scan from the "
        "right for the first position that dips below its neighbour.")

    # 1. Find the pivot.
    i = n - 2
    while i >= 0:
        counts["comparisons"] += 1
        if arr[i] < arr[i + 1]:
            add(f"arr[{i}] = {_fmt(arr[i])} < arr[{i + 1}] = {_fmt(arr[i + 1])} "
                f"— this is the pivot. The tail to its right is already maximal.",
                placed=i)
            break
        add(f"arr[{i}] = {_fmt(arr[i])} >= arr[{i + 1}] = {_fmt(arr[i + 1])} "
            f"— still descending, keep scanning left.", placed=i)
        i -= 1

    if i >= 0:
        # 2. Find the rightmost value greater than the pivot and swap.
        j = n - 1
        while arr[j] <= arr[i]:
            counts["comparisons"] += 1
            j -= 1
        counts["comparisons"] += 1
        add(f"Step 2: in the tail, {_fmt(arr[j])} at {j} is the smallest value "
            f"still bigger than the pivot {_fmt(arr[i])} — swap them.", placed=j)
        arr[i], arr[j] = arr[j], arr[i]
        counts["swaps"] += 1
        add(f"Swapped — {_fmt(arr[i])} is now the pivot slot. The tail past "
            f"{i} is still descending.", placed=i, window=[i + 1, n - 1])
        lo, hi = i + 1, n - 1
    else:
        add("No pivot — the array is the largest permutation. Reversing the "
            "whole thing wraps around to the smallest.", window=[0, n - 1])
        lo, hi = 0, n - 1

    # 3. Reverse the suffix into ascending order.
    if lo < hi:
        add(f"Step 3: reverse positions {lo}..{hi} so the tail becomes the "
            f"smallest arrangement.", window=[lo, hi])
    while lo < hi:
        arr[lo], arr[hi] = arr[hi], arr[lo]
        counts["swaps"] += 1
        add(f"Reverse: swap positions {lo} and {hi}.", placed=lo,
            window=[lo, hi])
        lo += 1
        hi -= 1

    add(f"Next permutation is {', '.join(_fmt(v) for v in arr)} — reached with "
        f"one right-to-left scan and a reversal, no sorting.", done=True)
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {
            "algorithm": "next_permutation",
            "view": "array",
            "language": "python",
            "result": arr,
        },
        "array": arr,
        "steps": steps,
    }
