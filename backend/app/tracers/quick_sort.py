MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    original = list(array)
    arr = list(array)
    steps = []
    sorted_ranges: list[list[int]] = []  # locked pivot positions, as [p, p]
    counts = {"comparisons": 0, "swaps": 0, "partitions": 0}

    def add(note, merging=None, comparing=None, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "merging": merging,          # the range being partitioned
                "comparing": comparing,
                "placed": placed,
                "sorted_ranges": [list(r) for r in sorted_ranges],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if len(arr) <= 1:
        if arr:
            sorted_ranges.append([0, 0])
        add("Nothing to sort — a single value (or none) is already in order.")
        return _result(original, steps)

    add(f"Start with {len(arr)} unsorted values.")

    def qsort(lo: int, hi: int):  # inclusive bounds
        if lo > hi:
            return
        if lo == hi:
            sorted_ranges.append([lo, lo])
            add(f"Position {lo} holds a single value — locked in place.", placed=lo)
            return
        pivot = arr[hi]
        add(
            f"Partition positions {lo}..{hi}: pivot is {_fmt(pivot)} (position {hi}).",
            merging=[lo, hi], placed=hi,
        )
        i = lo - 1
        for j in range(lo, hi):
            counts["comparisons"] += 1
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    counts["swaps"] += 1
                    add(
                        f"{_fmt(arr[i])} <= pivot {_fmt(pivot)} — swap it into the "
                        f"small side (position {i}).",
                        merging=[lo, hi], comparing=[arr[i], pivot], placed=i,
                    )
                else:
                    add(
                        f"{_fmt(arr[j])} <= pivot {_fmt(pivot)} — already on the small side.",
                        merging=[lo, hi], comparing=[arr[j], pivot], placed=j,
                    )
            else:
                add(
                    f"{_fmt(arr[j])} > pivot {_fmt(pivot)} — stays on the big side.",
                    merging=[lo, hi], comparing=[arr[j], pivot], placed=j,
                )
        p = i + 1
        if p != hi:
            arr[p], arr[hi] = arr[hi], arr[p]
            counts["swaps"] += 1
        counts["partitions"] += 1
        sorted_ranges.append([p, p])
        add(
            f"Pivot {_fmt(pivot)} locked at its final position {p} — everything left "
            f"is smaller, everything right is bigger.",
            merging=[lo, hi], placed=p,
        )
        qsort(lo, p - 1)
        qsort(p + 1, hi)

    qsort(0, len(arr) - 1)
    add("Every pivot locked — the array is sorted.")
    return _result(original, steps)


def _result(original, steps):
    return {
        "meta": {"algorithm": "quick_sort", "view": "array", "language": "python"},
        "array": original,
        "steps": steps,
    }
