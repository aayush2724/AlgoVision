"""Candy — the two-pass greedy for a tricky constraint.

Every child needs at least one candy, and a child with a higher rating than a
neighbour must get more than that neighbour. One left-to-right pass fixes the
"higher than my left neighbour" rule; one right-to-left pass fixes "higher than
my right neighbour", taking the max so both hold at once. Trying to satisfy both
directions in a single pass is where people get stuck — the two passes are the
insight.

Renders on the array view: cells show the running candy counts, the child being
updated is highlighted (placed).
"""

MAX_LEN = 12


def trace(array: list[float]):
    ratings = [int(v) for v in array]
    steps: list = []
    n = len(ratings)
    counts = {"total": 0, "passes": 0}
    candy = [1] * n

    def add(note, current=None):
        counts["total"] = sum(candy)
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                # Show the candy counts, not the raw ratings — that is what the
                # algorithm is building.
                "array": list(candy),
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current, "found": None},
            "note": note,
        })

    if not n:
        add("No children — no candy to hand out.")
        return _result(ratings, steps, 0)

    add(f"Ratings {ratings}. Everyone starts with 1 candy.")

    counts["passes"] = 1
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candy[i] = candy[i - 1] + 1
            add(f"Left→right: child {i} (rating {ratings[i]}) outranks its left "
                f"neighbour, so give it {candy[i]}.", current=i)
    add("Left→right pass done — every 'higher than my left' rule now holds.",
        current=n - 1)

    counts["passes"] = 2
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            need = candy[i + 1] + 1
            if need > candy[i]:
                candy[i] = need
                add(f"Right→left: child {i} (rating {ratings[i]}) outranks its "
                    f"right neighbour — bump to {candy[i]} (keep the larger).",
                    current=i)
    add(f"Right→left pass done. Total candies: {sum(candy)} — the minimum that "
        f"satisfies both neighbours everywhere.", current=0)
    return _result(ratings, steps, sum(candy))


def _result(ratings, steps, total):
    return {
        "meta": {
            "algorithm": "candy",
            "view": "array",
            "language": "python",
            "total": total,
        },
        "array": list(ratings),
        "steps": steps,
    }
