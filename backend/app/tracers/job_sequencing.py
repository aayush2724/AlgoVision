"""Job sequencing with deadlines — profit-first greedy on a slot timeline.

Each job takes one unit of time and earns its profit only if it finishes by its
deadline. Sort jobs by profit (richest first) and place each in the *latest*
still-free slot at or before its deadline — running it as late as possible
keeps the earlier slots open for other jobs that may have tighter deadlines.

Renders on the shared array view as the slot timeline (slot 1..maxDeadline).
A filled slot shows the profit sitting there and turns green (sorted_ranges);
the slot just filled is highlighted (placed).
"""

MAX_JOBS = 8
MAX_DEADLINE = 8
MAX_PROFIT = 1000


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(jobs: list[list[float]]):
    given = [[int(d), int(p)] for d, p in jobs]
    steps: list = []
    counts = {"profit": 0, "scheduled": 0, "skipped": 0}

    max_d = max((d for d, _ in given), default=0)
    # slot t lives at array index t-1.
    slots = [None] * max_d  # each entry: profit placed there, or None
    order = sorted(range(len(given)), key=lambda i: (-given[i][1], given[i][0]))
    total = 0

    def labels():
        return [(_fmt(p) if p is not None else "·") for p in slots]

    def filled():
        return [[i, i] for i, p in enumerate(slots) if p is not None]

    def add(note, current=None):
        counts["profit"] = total
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": labels(),
                "sorted_ranges": filled(),
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    if not given:
        add("No jobs to schedule.")
        return _result(steps, 0, [])

    seq_desc = ", ".join(f"d{given[i][0]}:£{given[i][1]}" for i in order)
    add(f"{len(given)} jobs, deadlines up to {max_d}. Take the richest first: "
        f"{seq_desc}. Each goes in the latest free slot on or before its "
        f"deadline.")

    sequence = []
    for i in order:
        d, p = given[i]
        placed_at = None
        # Walk back from the deadline to the latest free slot.
        for t in range(min(d, max_d), 0, -1):
            if slots[t - 1] is None:
                slots[t - 1] = p
                placed_at = t
                break
        if placed_at is not None:
            total += p
            counts["scheduled"] += 1
            sequence.append([d, p])
            add(f"Job d{d}:£{p} — latest free slot by its deadline is slot "
                f"{placed_at}. Schedule it there (+£{p}).", current=placed_at - 1)
        else:
            counts["skipped"] += 1
            add(f"Job d{d}:£{p} — every slot up to deadline {d} is taken. "
                f"It misses out.", current=(d - 1 if d >= 1 else None))

    add(f"Total profit £{total} from {counts['scheduled']} jobs. Placing each "
        f"as late as its deadline allows is what leaves room for the rest.")
    return _result(steps, total, sequence)


def _result(steps, total, sequence):
    return {
        "meta": {
            "algorithm": "job_sequencing",
            "view": "array",
            "language": "python",
            "total_profit": total,
            "count": len(sequence),
        },
        "array": [],
        "steps": steps,
    }
