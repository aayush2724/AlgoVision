"""Fractional knapsack — the greedy that 0/1 knapsack can't use.

Because you may take a *fraction* of an item, the optimal move is purely local:
sort by value-per-weight and take as much of the best ratio as fits, then the
next, splitting the last item to fill the bag exactly. (0/1 knapsack forbids
that split, which is why it needs DP instead.)

Renders on the shared array view: each cell is an item "w:v" sorted by ratio.
Fully-taken items go green (sorted_ranges); the item currently being taken —
possibly only in part — is highlighted (placed).
"""

MAX_ITEMS = 6
MAX_WEIGHT_VALUE = 500
MAX_CAPACITY = 200


def _fmt(v: float) -> str:
    return f"{v:g}"


def _num(x):
    """Return an int when the value is whole, else a rounded float — keeps the
    counter chips tidy."""
    xf = float(x)
    return int(xf) if xf == int(xf) else round(xf, 2)


def trace(items: list[list[float]], capacity: float):
    given = [[float(w), float(v)] for w, v in items]
    steps: list = []
    counts = {"taken": 0, "remaining": _num(capacity)}

    # Sort by value/weight ratio, descending — the whole idea.
    ordered = sorted(given, key=lambda it: (it[1] / it[0]), reverse=True)
    labels = [f"{_fmt(w)}:{_fmt(v)}" for w, v in ordered]
    taken_full: list[int] = []
    total = 0.0
    remaining = float(capacity)

    def add(note, current=None):
        counts["remaining"] = _num(remaining)
        counts["taken"] = _num(round(total, 2))
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(labels),
                "sorted_ranges": [[i, i] for i in taken_full],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    ratios = ", ".join(
        f"{labels[i]} (ratio {_fmt(round(ordered[i][1] / ordered[i][0], 2))})"
        for i in range(len(ordered)))
    add(f"Capacity {_fmt(capacity)}. Sort by value-per-weight, best first: "
        f"{ratios}. Now fill greedily.")

    for i, (w, v) in enumerate(ordered):
        if remaining <= 0:
            add(f"Bag full — skip {labels[i]} and everything after it.", current=i)
            break
        if w <= remaining:
            remaining -= w
            total += v
            taken_full.append(i)
            add(f"Take all of {labels[i]}: +{_fmt(v)} value, {_fmt(remaining)} "
                f"capacity left.", current=i)
        else:
            frac = remaining / w
            gained = v * frac
            total += gained
            remaining = 0.0
            add(f"Only a sliver of room left — take a {_fmt(round(frac, 2))} "
                f"slice of {labels[i]} for +{_fmt(round(gained, 2))} value. "
                f"That fills the bag exactly.", current=i)
            break

    add(f"Best value: {_fmt(round(total, 2))}. Greedy by ratio is optimal here "
        f"precisely because fractions are allowed — the last split wastes no "
        f"capacity.")
    return _result(labels, steps, round(total, 2))


def _result(labels, steps, total):
    return {
        "meta": {
            "algorithm": "fractional_knapsack",
            "view": "array",
            "language": "python",
            "total_value": total,
        },
        "array": list(labels),
        "steps": steps,
    }
