def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], target: float):
    arr = list(array)
    steps = []
    low, high = 0, len(arr) - 1
    found_at = None

    def add(note, low_, high_, mid=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 1 if not steps else 3,
            "structures": {"low": low_, "high": high_, "mid": mid, "found": found},
            "highlight": {"index": mid},
            "note": note,
        })

    if not arr:
        add("The array is empty — nothing to search.", 0, -1, found=False)
        return _result(arr, target, steps)

    add(
        f"Search {len(arr)} sorted values for target {_fmt(target)}. "
        f"The whole range 0..{high} is in play.",
        low, high,
    )

    while low <= high:
        mid = (low + high) // 2
        add(
            f"Check the middle: position {mid} holds {_fmt(arr[mid])}.",
            low, high, mid=mid,
        )
        if arr[mid] == target:
            found_at = mid
            add(
                f"Found it — {_fmt(target)} is at position {mid}.",
                low, high, mid=mid, found=True,
            )
            break
        elif arr[mid] < target:
            low = mid + 1
            add(
                f"{_fmt(arr[mid])} is smaller than {_fmt(target)} — discard the "
                f"left half. Range narrows to {low}..{high}."
                if low <= high else
                f"{_fmt(arr[mid])} is smaller than {_fmt(target)} — nothing left "
                f"to search on the right.",
                low, high, mid=mid,
            )
        else:
            high = mid - 1
            add(
                f"{_fmt(arr[mid])} is larger than {_fmt(target)} — discard the "
                f"right half. Range narrows to {low}..{high}."
                if low <= high else
                f"{_fmt(arr[mid])} is larger than {_fmt(target)} — nothing left "
                f"to search on the left.",
                low, high, mid=mid,
            )

    if found_at is None:
        add(
            f"The range is empty — {_fmt(target)} is not in the array.",
            low, high, found=False,
        )

    return _result(arr, target, steps)


def _result(arr, target, steps):
    return {
        "meta": {
            "algorithm": "binary_search",
            "view": "array",
            "language": "python",
            "target": target,
        },
        "array": arr,
        "steps": steps,
    }
