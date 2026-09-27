"""Minimise the Largest Group Sum — book allocation, painter's partition,
split-array-largest-sum and ship-within-D-days are all this one problem.

Split the array into at most k contiguous groups so the biggest group sum is as
small as possible. Guess a limit L: greedily fill groups left to right, opening
a new group whenever the next item would push the sum past L. If that needs at
most k groups, L is achievable — and so is every bigger L. That monotonic
yes/no lets us binary-search L over max(arr)..sum(arr). O(n log sum).

Reuses the `array` view: the item being placed is `placed`, the group being
filled is the orange `merging` span, and the optional `answer` number line
shows the limit range shrinking.
"""

MAX_LEN = 10
MAX_VALUE = 500


def _answer(lo, hi, mid, best, a, b):
    return {"min": a, "max": b, "lo": lo, "hi": hi, "mid": mid,
            "best": best, "label": "MAX GROUP SUM"}


def trace(array: list, k: int):
    arr = [int(v) for v in array]
    k = int(k)
    a, b = max(arr), sum(arr)
    steps: list = []
    counts = {"guesses": 0, "item_checks": 0}

    def add(note, answer, placed=None, group=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "merging": list(group) if group else None,
                "answer": answer,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    lo, hi, best = a, b, None
    add(f"Split into at most {k} contiguous groups, minimising the largest "
        f"group sum. The answer is at least the biggest item ({a}) and at most "
        f"the total ({b}) — binary-search that range.",
        _answer(lo, hi, None, best, a, b))

    while lo <= hi:
        mid = (lo + hi) // 2
        counts["guesses"] += 1
        groups, run, start = 1, 0, 0
        add(f"Guess limit {mid}. Fill groups greedily, never exceeding it.",
            _answer(lo, hi, mid, best, a, b))
        for i, v in enumerate(arr):
            counts["item_checks"] += 1
            if run + v > mid:
                groups += 1
                start, run = i, v
                add(f"{v} would push the group past {mid} — start group "
                    f"#{groups} at item {i}.", _answer(lo, hi, mid, best, a, b),
                    placed=i, group=(start, i))
                if groups > k:
                    break
            else:
                run += v
                add(f"Add {v}: group #{groups} sums to {run}.",
                    _answer(lo, hi, mid, best, a, b), placed=i,
                    group=(start, i))
        if groups <= k:
            best = mid
            add(f"{groups} group(s) ≤ {k} — limit {mid} works. Try a smaller "
                f"limit: {lo}..{mid - 1}.", _answer(lo, mid - 1, mid, best, a, b))
            hi = mid - 1
        else:
            add(f"Needed more than {k} groups — limit {mid} is too tight, and "
                f"so is anything smaller. Search {mid + 1}..{hi}.",
                _answer(mid + 1, hi, mid, best, a, b))
            lo = mid + 1

    add(f"Smallest achievable largest-group sum: {best}. {counts['guesses']} "
        f"guesses over a range of {b - a + 1} — O(n log sum).",
        _answer(lo, hi, None, best, a, b))
    return {
        "meta": {"algorithm": "min_max_partition", "view": "array",
                 "language": "python", "result": best},
        "array": arr,
        "steps": steps,
    }
