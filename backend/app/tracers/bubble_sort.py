MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    original = list(array)
    arr = list(array)
    n = len(arr)
    steps = []
    sorted_from = n  # everything from this index rightward is locked
    counts = {"comparisons": 0, "swaps": 0, "passes": 0}

    def add(note, comparing=None, placed=None):
        sorted_ranges = [[sorted_from, n - 1]] if sorted_from < n else []
        if sorted_from == 0 and n > 0:
            sorted_ranges = [[0, n - 1]]
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "merging": [0, sorted_from - 1] if sorted_from > 0 else None,
                "comparing": comparing,
                "placed": placed,
                "sorted_ranges": sorted_ranges,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n <= 1:
        sorted_from = 0
        add("Nothing to sort — a single value (or none) is already in order.")
        return _result(original, steps)

    add(f"Start with {n} unsorted values. Heavy values will sink to the right.")

    for end in range(n - 1, 0, -1):
        counts["passes"] += 1
        swapped = False
        for j in range(end):
            counts["comparisons"] += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                counts["swaps"] += 1
                swapped = True
                add(
                    f"{_fmt(arr[j + 1])} > {_fmt(arr[j])} — swap them; the heavier "
                    f"one bubbles right.",
                    comparing=[arr[j], arr[j + 1]], placed=j + 1,
                )
            else:
                add(
                    f"{_fmt(arr[j])} <= {_fmt(arr[j + 1])} — already in order, move on.",
                    comparing=[arr[j], arr[j + 1]], placed=j,
                )
        sorted_from = end
        add(f"Pass {counts['passes']} done — position {end} is locked with {_fmt(arr[end])}.",
            placed=end)
        if not swapped:
            sorted_from = 0
            add("No swaps in that pass — the array is already sorted. Early exit!")
            break

    if sorted_from != 0:
        sorted_from = 0
        add("Only one value left unlocked — it must be in place. Sorted.")

    return _result(original, steps)


def _result(original, steps):
    return {
        "meta": {"algorithm": "bubble_sort", "view": "array", "language": "python"},
        "array": original,
        "steps": steps,
    }
