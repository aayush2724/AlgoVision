"""Jump Game I — can you reach the last index? The one-pass reachability greedy.

Each value is the maximum jump length from that cell. Walk left to right keeping
the *farthest* index reachable so far; if you ever stand on a cell beyond that
reach, you are stuck. No need to try individual jumps — the running maximum is
all the information that matters.

Renders on the array view: the reachable prefix glows green (sorted_ranges),
the current cell is highlighted (placed).
"""

MAX_LEN = 16


def trace(array: list[float]):
    nums = [int(v) for v in array]
    steps: list = []
    counts = {"reach": 0, "steps": 0}
    n = len(nums)

    def add(note, current=None, reach=0):
        counts["reach"] = reach
        counts["steps"] = (current + 1) if current is not None else 0
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(nums),
                "sorted_ranges": [[0, min(reach, n - 1)]] if n else [],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    if not n:
        add("Empty array — already at the end.")
        return _result(nums, steps, True)

    reach = 0
    add("Start at index 0. Farthest reachable so far: 0.", current=0, reach=0)
    ok = True
    for i in range(n):
        if i > reach:
            add(f"Index {i} sits beyond the farthest reach ({reach}) — stuck. "
                f"The last index is unreachable.", current=i, reach=reach)
            ok = False
            break
        new_reach = max(reach, i + nums[i])
        if new_reach > reach:
            reach = new_reach
            add(f"From index {i} (jump {nums[i]}) reach extends to {reach}.",
                current=i, reach=reach)
        else:
            add(f"Index {i} (jump {nums[i]}) does not extend the reach ({reach}).",
                current=i, reach=reach)
        if reach >= n - 1:
            add(f"Reach {reach} covers the last index ({n - 1}) — you can make it!",
                current=i, reach=reach)
            ok = True
            break

    return _result(nums, steps, ok)


def _result(nums, steps, ok):
    return {
        "meta": {
            "algorithm": "jump_game",
            "view": "array",
            "language": "python",
            "reachable": bool(ok),
        },
        "array": list(nums),
        "steps": steps,
    }
