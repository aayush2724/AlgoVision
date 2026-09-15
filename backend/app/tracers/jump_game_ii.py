"""Jump Game II — the fewest jumps to reach the last index.

A greedy that reads like a breadth-first sweep over ranges: within the current
jump's reachable window, scan every cell and remember the farthest you could
land next. When you step past the end of the current window, you *must* spend a
jump, and the new window is everything you found. Each cell is read once.

Renders on the array view: the current jump window glows green (sorted_ranges),
the cell being scanned is highlighted (placed).
"""

MAX_LEN = 16


def trace(array: list[float]):
    nums = [int(v) for v in array]
    steps: list = []
    counts = {"jumps": 0, "reach": 0}
    n = len(nums)

    def add(note, current=None, lo=0, hi=0):
        counts["reach"] = hi
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(nums),
                "sorted_ranges": [[max(lo, 0), min(hi, n - 1)]] if n else [],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    if n <= 1:
        add("Already at (or past) the last index — zero jumps needed.", current=0)
        return _result(nums, steps, 0)

    jumps = 0
    cur_end = 0      # last index reachable with the jumps taken so far
    farthest = 0
    add("No jumps yet. The current window is just index 0.", current=0, lo=0, hi=0)

    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        add(f"From index {i} (jump {nums[i]}) you could reach {i + nums[i]}; "
            f"farthest next landing is {farthest}.", current=i, lo=0, hi=farthest)
        if i == cur_end:
            jumps += 1
            counts["jumps"] = jumps
            cur_end = farthest
            add(f"Reached the end of this window — spend jump #{jumps}. New "
                f"window extends to {min(cur_end, n - 1)}.",
                current=i, lo=i, hi=cur_end)
            if cur_end >= n - 1:
                break

    add(f"Last index reached in {jumps} jump(s) — the minimum possible.",
        current=n - 1, lo=0, hi=n - 1)
    return _result(nums, steps, jumps)


def _result(nums, steps, jumps):
    return {
        "meta": {
            "algorithm": "jump_game_ii",
            "view": "array",
            "language": "python",
            "jumps": jumps,
        },
        "array": list(nums),
        "steps": steps,
    }
