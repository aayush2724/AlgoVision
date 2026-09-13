"""Sliding window maximum — the largest value in every window of size k, with
a monotonic deque so no value is ever re-examined.

The deque holds indices whose values are still candidates, kept in decreasing
order. Before adding i, every smaller value at the back is discarded — it can
never be the max while i is around. The front is always the current window's
maximum; it is dropped once it slides out of range. Each index is pushed and
popped at most once, so the whole scan is O(n), not O(n·k).

Reuses the `array` view: cells are the numbers, `merging` is the current
window, `placed` marks the value entering, and the deque plus the window's max
ride in the note. No new renderer.
"""

from collections import deque

MAX_ARRAY_LEN = 14


def trace(nums: list, k: int):
    arr = [int(x) for x in nums]
    n = len(arr)
    k = int(k)
    dq: deque = deque()          # indices, values decreasing front→back
    maxes: list[int] = []
    steps: list = []
    counts = {"pushes": 0, "pops_small": 0, "pops_expired": 0, "windows": 0}

    def add(note, placed=None, window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "placed": placed,
                "merging": list(window) if window else None,
                "deque": [arr[j] for j in dq],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    add(f"Find the maximum of every window of size {k}. A deque keeps only the "
        f"indices that could still win, in decreasing value order — its front "
        f"is always the current window's maximum.")

    for i in range(n):
        # Drop smaller values at the back — i dominates them from now on.
        while dq and arr[dq[-1]] <= arr[i]:
            counts["pops_small"] += 1
            add(f"{arr[i]} enters and is ≥ {arr[dq[-1]]} at the back — that "
                f"older value can never be a maximum again, so drop it.",
                placed=i)
            dq.pop()
        dq.append(i)
        counts["pushes"] += 1
        # Drop the front if it has slid out of the window.
        if dq[0] <= i - k:
            counts["pops_expired"] += 1
            add(f"The front (index {dq[0]}) has slid out of the window — "
                f"remove it.", placed=i, window=[i - k + 1, i])
            dq.popleft()
        if i >= k - 1:
            counts["windows"] += 1
            maxes.append(arr[dq[0]])
            add(f"Window [{i - k + 1}, {i}] is full — its maximum is the deque "
                f"front, {arr[dq[0]]}.", placed=dq[0], window=[i - k + 1, i])
        else:
            add(f"Still filling the first window ({i + 1}/{k}). Deque front is "
                f"{arr[dq[0]]}.", placed=i, window=[0, i])

    add(f"Window maxima: {maxes}. Every index was pushed and popped at most "
        f"once, so the whole pass is O(n) — re-scanning each window would have "
        f"been O(n·k).")

    return {
        "meta": {
            "algorithm": "sliding_window_maximum",
            "view": "array",
            "language": "python",
            "k": k,
            "maxes": maxes,
            "result": maxes,
        },
        "array": list(arr),
        "steps": steps,
    }
