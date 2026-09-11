MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    original = list(array)
    arr = list(array)
    steps = []
    sorted_ranges: list[list[int]] = []
    counts = {"comparisons": 0, "writes": 0, "merges": 0}

    def add(note, merging=None, comparing=None, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "merging": merging,
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

    def msort(lo: int, hi: int):  # sorts arr[lo:hi]
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        add(
            f"Split positions {lo}..{hi - 1} into halves "
            f"{lo}..{mid - 1} and {mid}..{hi - 1}.",
            merging=[lo, hi - 1],
        )
        msort(lo, mid)
        msort(mid, hi)

        left, right = arr[lo:mid], arr[mid:hi]
        i = j = 0
        merged: list[float] = []

        def commit():
            # Display = merged prefix + values still waiting in each half,
            # so every snapshot stays a permutation of the input.
            arr[lo:hi] = merged + left[i:] + right[j:]

        while i < len(left) and j < len(right):
            a, b = left[i], right[j]
            if a <= b:
                merged.append(a)
                i += 1
            else:
                merged.append(b)
                j += 1
            counts["comparisons"] += 1
            counts["writes"] += 1
            commit()
            k = lo + len(merged) - 1
            add(
                f"Compare {_fmt(a)} vs {_fmt(b)} — place {_fmt(merged[-1])} "
                f"at position {k}.",
                merging=[lo, hi - 1], comparing=[a, b], placed=k,
            )
        while i < len(left):
            merged.append(left[i])
            i += 1
            counts["writes"] += 1
            commit()
            k = lo + len(merged) - 1
            add(
                f"Right half exhausted — copy remaining {_fmt(merged[-1])} "
                f"to position {k}.",
                merging=[lo, hi - 1], placed=k,
            )
        while j < len(right):
            merged.append(right[j])
            j += 1
            counts["writes"] += 1
            commit()
            k = lo + len(merged) - 1
            add(
                f"Left half exhausted — copy remaining {_fmt(merged[-1])} "
                f"to position {k}.",
                merging=[lo, hi - 1], placed=k,
            )

        # This merged range supersedes any sub-ranges it contains.
        sorted_ranges[:] = [
            r for r in sorted_ranges if not (lo <= r[0] and r[1] <= hi - 1)
        ]
        sorted_ranges.append([lo, hi - 1])
        counts["merges"] += 1
        add(
            f"Positions {lo}..{hi - 1} merged — this section is now sorted.",
            merging=[lo, hi - 1],
        )

    msort(0, len(arr))
    add("Every section merged — the whole array is in order.")
    return _result(original, steps)


def _result(original, steps):
    return {
        "meta": {"algorithm": "merge_sort", "view": "array", "language": "python"},
        "array": original,
        "steps": steps,
    }
