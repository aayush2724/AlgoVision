MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    original = list(array)
    arr = list(array)
    n = len(arr)
    steps = []
    counts = {"comparisons": 0, "swaps": 0}
    sorted_upto = -1  # arr[0..sorted_upto] is final

    def add(note, comparing=None, placed=None, scanning=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "merging": scanning,   # the range still being scanned
                "comparing": comparing,
                "placed": placed,
                "sorted_ranges": [[0, sorted_upto]] if sorted_upto >= 0 else [],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n <= 1:
        sorted_upto = n - 1
        add("Nothing to sort — a single value (or none) is already in order.")
        return _result(original, steps)

    add(f"Start with {n} values. Each round finds the champion of what's left.")

    for i in range(n - 1):
        min_idx = i
        add(f"Round {i + 1}: assume {_fmt(arr[i])} (position {i}) is the smallest so far.",
            placed=i, scanning=[i, n - 1])
        for j in range(i + 1, n):
            counts["comparisons"] += 1
            champion = arr[min_idx]
            if arr[j] < champion:
                min_idx = j
                add(f"{_fmt(arr[j])} beats {_fmt(champion)} — new champion at position {j}.",
                    comparing=[arr[j], champion], placed=j, scanning=[i, n - 1])
            else:
                add(f"{_fmt(arr[j])} is not smaller than {_fmt(champion)} — champion unchanged.",
                    comparing=[arr[j], champion], placed=j, scanning=[i, n - 1])
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            counts["swaps"] += 1
        sorted_upto = i
        add(f"Champion {_fmt(arr[i])} moves to position {i} — locked.", placed=i)

    sorted_upto = n - 1
    add("Last value stands alone — it must be the biggest. Sorted.")
    return _result(original, steps)


def _result(original, steps):
    return {
        "meta": {"algorithm": "selection_sort", "view": "array", "language": "python"},
        "array": original,
        "steps": steps,
    }
