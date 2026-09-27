"""Aggressive Cows — maximise the minimum gap by binary-searching the gap.

Place c cows in sorted stalls so the closest pair is as far apart as possible.
Guess a gap d: put the first cow in the first stall, then each next cow in the
first stall at least d beyond the previous one. If all c fit, d is achievable —
and so is every smaller d. Search d over 1..(last − first) for the largest
value that still fits: O(n log range) after sorting.

Reuses the `array` view: stalls are the (sorted) cells, stalls holding a cow
are green, the stall being tested is `placed`, and the optional `answer`
number line shows the gap range shrinking.
"""

MAX_LEN = 10
MAX_POS = 1000


def _answer(lo, hi, mid, best, top):
    return {"min": 1, "max": max(top, 1), "lo": lo, "hi": hi, "mid": mid,
            "best": best, "label": "MIN GAP d"}


def trace(stalls: list, cows: int):
    arr = sorted(int(s) for s in stalls)
    c = int(cows)
    top = arr[-1] - arr[0]
    steps: list = []
    counts = {"guesses": 0, "stall_checks": 0}

    def add(note, answer, placed=None, used=()):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "sorted_ranges": [[j, j] for j in used],
                "answer": answer,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    lo, hi, best = 1, top, None
    add(f"Stalls sorted: {arr}. Place {c} cows so the closest two are as far "
        f"apart as possible. A bigger gap is harder, so fit-or-not flips once — "
        f"binary-search the gap over 1..{top}.", _answer(lo, hi, None, best, top))

    while lo <= hi:
        mid = (lo + hi) // 2
        counts["guesses"] += 1
        used = [0]
        add(f"Guess gap {mid}. First cow goes in the first stall ({arr[0]}).",
            _answer(lo, hi, mid, best, top), placed=0, used=used)
        for i in range(1, len(arr)):
            if len(used) == c:
                break
            counts["stall_checks"] += 1
            gap = arr[i] - arr[used[-1]]
            if gap >= mid:
                used.append(i)
                add(f"Stall {arr[i]} is {gap} ≥ {mid} from the last cow — place "
                    f"cow #{len(used)}.", _answer(lo, hi, mid, best, top),
                    placed=i, used=used)
            else:
                add(f"Stall {arr[i]} is only {gap} from the last cow — too "
                    f"close, skip.", _answer(lo, hi, mid, best, top),
                    placed=i, used=used)
        if len(used) >= c:
            best = mid
            add(f"All {c} cows fit with gap ≥ {mid}. Try wider: "
                f"{mid + 1}..{hi}.", _answer(mid + 1, hi, mid, best, top),
                used=used)
            lo = mid + 1
        else:
            add(f"Only {len(used)} of {c} cows fit — gap {mid} is too wide, and "
                f"so is anything wider. Search {lo}..{mid - 1}.",
                _answer(lo, mid - 1, mid, best, top), used=used)
            hi = mid - 1

    add(f"Largest possible minimum gap: {best}. {counts['guesses']} guesses "
        f"instead of trying every gap up to {top}.",
        _answer(lo, hi, None, best, top))
    return {
        "meta": {"algorithm": "aggressive_cows", "view": "array",
                 "language": "python", "result": best},
        "array": arr,
        "steps": steps,
    }
