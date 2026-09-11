MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    original = list(array)
    arr = list(array)
    n = len(arr)
    steps = []
    counts = {"comparisons": 0, "shifts": 0, "inserts": 0}
    sorted_upto = 0  # arr[0..sorted_upto] is the sorted prefix

    def add(note, comparing=None, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "merging": None,
                "comparing": comparing,
                "placed": placed,
                "sorted_ranges": [[0, sorted_upto]] if n else [],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n <= 1:
        add("Nothing to sort — a single value (or none) is already in order.")
        return _result(original, steps)

    add(f"Start with {n} values. The first one alone is a sorted hand of cards.")

    for i in range(1, n):
        key = arr[i]
        add(f"Pick up {_fmt(key)} (position {i}) — find its slot in the sorted hand.",
            placed=i)
        j = i
        while j > 0:
            counts["comparisons"] += 1
            if arr[j - 1] > key:
                # Shift the bigger card right; the picked-up card slides left
                # with the hole so every frame stays a true permutation.
                arr[j], arr[j - 1] = arr[j - 1], key
                counts["shifts"] += 1
                add(f"{_fmt(arr[j])} is bigger than {_fmt(key)} — shift it right; "
                    f"the card slides left.",
                    comparing=[arr[j], key], placed=j - 1)
                j -= 1
            else:
                break
        counts["inserts"] += 1
        sorted_upto = i
        add(f"{_fmt(key)} settles at position {j} — the hand grows to {i + 1} cards.",
            placed=j)

    add("Every card picked up and placed — the hand is fully sorted.")
    return _result(original, steps)


def _result(original, steps):
    return {
        "meta": {"algorithm": "insertion_sort", "view": "array", "language": "python"},
        "array": original,
        "steps": steps,
    }
