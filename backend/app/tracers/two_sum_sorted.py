MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], target: float):
    arr = list(array)
    n = len(arr)
    steps = []
    counts = {"checks": 0, "moves": 0}

    def add(note, left=None, right=None, s=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"left": left, "right": right, "sum": s,
                           "found": found, "counts": dict(counts)},
            "highlight": {"index": left},
            "note": note,
        })

    if n < 2:
        add("Fewer than two values — no pair to find.", found=False)
        return _result(arr, target, steps)

    left, right = 0, n - 1
    add(
        f"Find two values summing to {_fmt(target)}. Start with pointers at "
        f"both ends — the sorted order does the thinking.",
        left, right,
    )

    while left < right:
        s = arr[left] + arr[right]
        counts["checks"] += 1
        if s == target:
            add(
                f"{_fmt(arr[left])} + {_fmt(arr[right])} = {_fmt(target)} — "
                f"pair found at positions {left} and {right}!",
                left, right, s, found=True,
            )
            return _result(arr, target, steps)
        if s < target:
            add(
                f"{_fmt(arr[left])} + {_fmt(arr[right])} = {_fmt(s)} — too small. "
                f"Only moving the left pointer right can grow the sum.",
                left, right, s,
            )
            left += 1
            counts["moves"] += 1
        else:
            add(
                f"{_fmt(arr[left])} + {_fmt(arr[right])} = {_fmt(s)} — too big. "
                f"Only moving the right pointer left can shrink the sum.",
                left, right, s,
            )
            right -= 1
            counts["moves"] += 1

    add(
        f"Pointers met — no pair sums to {_fmt(target)}. "
        f"Every candidate was ruled out in one pass.",
        left, right, found=False,
    )
    return _result(arr, target, steps)


def _result(arr, target, steps):
    return {
        "meta": {"algorithm": "two_sum_sorted", "view": "array",
                 "language": "python", "target": target},
        "array": arr,
        "steps": steps,
    }
