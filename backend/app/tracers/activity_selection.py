"""Activity selection / N-meetings-in-one-room — the exchange-argument greedy.

The whole trick is the sort key: order meetings by *finish* time, not start
time or duration. Then greedily take the first meeting, and each next meeting
whose start is at or after the last chosen finish. Finishing earliest always
leaves the most room for what follows — that is the greedy-stays-ahead
argument, made visible.

Renders on the shared array view: each cell is a meeting "s–e". Chosen meetings
turn green (sorted_ranges), the meeting under consideration is highlighted
(placed), so no new renderer is needed.
"""

MAX_MEETINGS = 10


def _fmt(v: float) -> str:
    return f"{v:g}"


def _label(iv) -> str:
    return f"{_fmt(iv[0])}–{_fmt(iv[1])}"


def trace(intervals: list[list[float]]):
    given = [[float(a), float(b)] for a, b in intervals]
    steps: list = []
    counts = {"selected": 0, "skipped": 0, "comparisons": 0}

    # Order by finish time (tie-break on start) — the heart of the algorithm.
    ordered = sorted(given, key=lambda iv: (iv[1], iv[0]))
    chosen: list[int] = []

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": [_label(iv) for iv in ordered],
                # Each chosen index as a 1-wide range → the array view paints
                # it green; the current candidate is highlighted via `placed`.
                "sorted_ranges": [[i, i] for i in chosen],
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    if not given:
        add("No meetings — nothing to schedule.")
        return _result(ordered, steps, [])

    add(f"{len(given)} meetings. Sort them by *finish* time — the earlier a "
        f"room frees up, the more meetings can follow. Sorted: "
        f"{', '.join(_label(iv) for iv in ordered)}.")

    last_end = None
    for i, iv in enumerate(ordered):
        if last_end is None or iv[0] >= last_end:
            if last_end is not None:
                counts["comparisons"] += 1
            chosen.append(i)
            counts["selected"] += 1
            last_end = iv[1]
            add(f"Take {_label(iv)} — it starts at or after the last room "
                f"free-up, so it fits ({_fmt(last_end)} is the new busy-until). "
                f"{counts['selected']} booked so far.", current=i)
        else:
            counts["comparisons"] += 1
            counts["skipped"] += 1
            add(f"Skip {_label(iv)} — it starts before {_fmt(last_end)}, so it "
                f"clashes with a meeting already booked.", current=i)

    picks = ", ".join(_label(ordered[i]) for i in chosen)
    add(f"Done. {counts['selected']} meetings fit in one room: {picks}. "
        f"Choosing the earliest finish each time is provably optimal — no "
        f"schedule can fit more.")
    return _result(ordered, steps, chosen)


def _result(ordered, steps, chosen):
    return {
        "meta": {
            "algorithm": "activity_selection",
            "view": "array",
            "language": "python",
            "chosen": [[ordered[i][0], ordered[i][1]] for i in chosen],
            "count": len(chosen),
        },
        "array": [_label(iv) for iv in ordered],
        "steps": steps,
    }
