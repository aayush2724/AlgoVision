"""Merge overlapping intervals — the interval pattern, start to finish.

The lesson is the sort: once intervals are ordered by start, a single pass
suffices, because anything that can overlap the block we're building must be
the very next interval. Students who skip the sort write an O(n^2) pairwise
check instead.
"""

MAX_INTERVALS = 10
MAX_VALUE = 100


def _fmt(v: float) -> str:
    return f"{v:g}"


def _label(iv) -> str:
    return f"{_fmt(iv[0])}–{_fmt(iv[1])}"


def trace(intervals: list[list[float]]):
    given = [[float(a), float(b)] for a, b in intervals]
    steps: list = []
    counts = {"comparisons": 0, "merges": 0, "kept": 0}

    ordered = sorted(given, key=lambda iv: (iv[0], iv[1]))
    merged: list[list[float]] = []

    def add(note, current=None, target=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                # The array view renders string cells, so intervals read as
                # "2–6" rather than a bare pair of numbers.
                "array": [_label(iv) for iv in ordered],
                "merged": [list(iv) for iv in merged],
                "merged_labels": [_label(iv) for iv in merged],
                "comparing": [i for i in (current,) if i is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": current, "target": target},
            "note": note,
        })

    if not given:
        add("No intervals — nothing to merge.")
        return _result(merged, ordered, steps)

    was_sorted = ordered == given
    add(
        f"{len(given)} intervals. "
        + ("They already arrive sorted by start time. "
           if was_sorted else
           "First sort them by start time — that is the whole trick. ")
        + "Once sorted, anything that can overlap the block we're building "
          "must be the very next interval, so one pass is enough."
    )

    merged.append(list(ordered[0]))
    counts["kept"] += 1
    add(f"Take {_label(ordered[0])} as the first block — nothing to its left "
        f"can overlap it.", current=0)

    for idx in range(1, len(ordered)):
        iv = ordered[idx]
        last = merged[-1]
        counts["comparisons"] += 1

        if iv[0] <= last[1]:
            before = _label(last)
            ends_at = last[1]
            last[1] = max(last[1], iv[1])
            counts["merges"] += 1
            add(f"{_label(iv)} starts at {_fmt(iv[0])}, which is not past "
                f"{_fmt(ends_at)} where the block ends — they touch, so "
                f"{before} absorbs it and becomes {_label(last)}.",
                current=idx, target=len(merged) - 1)
        else:
            merged.append(list(iv))
            counts["kept"] += 1
            add(f"{_label(iv)} starts at {_fmt(iv[0])}, after the block ends "
                f"at {_fmt(last[1])} — no overlap, so it opens a new block.",
                current=idx, target=len(merged) - 1)

    add(f"{len(given)} intervals collapsed into {len(merged)}: "
        f"{', '.join(_label(m) for m in merged)}. "
        f"One pass and {counts['comparisons']} comparisons after the sort — "
        f"O(n log n) overall, and the sort is the expensive half.",
        target=len(merged) - 1)

    return _result(merged, ordered, steps)


def _result(merged, ordered, steps):
    return {
        "meta": {
            "algorithm": "merge_intervals",
            "view": "array",
            "language": "python",
            "merged": [list(m) for m in merged],
            "sorted_input": [list(o) for o in ordered],
        },
        "array": [f"{_fmt(a)}-{_fmt(b)}" for a, b in merged],
        "steps": steps,
    }
