"""Koko Eating Bananas — binary search on the *answer*, not on the array.

Koko eats at k bananas/hour; a pile of p takes ceil(p / k) hours. Faster is
always at least as good, so "can she finish in h hours at speed k?" flips from
no to yes exactly once as k grows. That monotonic yes/no is what makes binary
search work — over the range of speeds 1..max(pile), not over the piles.
Each guess costs one O(n) pass: O(n log max).

Reuses the `array` view: the piles are the cells (the pile being eaten is
`placed`), and the optional `answer` number line above them shows the speed
range shrinking — lo..hi, the guess `mid`, and the best speed found so far.
"""

MAX_LEN = 8
MAX_PILE = 1000


def _answer(lo, hi, mid, best, top):
    return {"min": 1, "max": top, "lo": lo, "hi": hi, "mid": mid,
            "best": best, "label": "SPEED k"}


def trace(piles: list, h: int):
    arr = [int(p) for p in piles]
    h = int(h)
    top = max(arr)
    steps: list = []
    counts = {"guesses": 0, "pile_checks": 0}

    def add(note, answer, placed=None, done=()):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "sorted_ranges": [[j, j] for j in done],
                "answer": answer,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    lo, hi, best = 1, top, None
    add(f"Find the slowest speed that finishes all piles within {h} hours. "
        f"Too slow fails, fast enough succeeds — and that only flips once, so "
        f"binary-search the speeds 1..{top} (the biggest pile).",
        _answer(lo, hi, None, best, top))

    while lo <= hi:
        mid = (lo + hi) // 2
        counts["guesses"] += 1
        hours = 0
        add(f"Guess k = {mid} (middle of {lo}..{hi}). Time each pile.",
            _answer(lo, hi, mid, best, top))
        for i, p in enumerate(arr):
            counts["pile_checks"] += 1
            t = -(-p // mid)
            hours += t
            add(f"Pile {p} at {mid}/hour takes ⌈{p}/{mid}⌉ = {t} h — running "
                f"total {hours} h.", _answer(lo, hi, mid, best, top),
                placed=i, done=range(i))
            if hours > h:
                break
        if hours <= h:
            best = mid
            add(f"{hours} h ≤ {h} — speed {mid} works. Record it and try "
                f"slower: search {lo}..{mid - 1}.",
                _answer(lo, mid - 1, mid, best, top), done=range(len(arr)))
            hi = mid - 1
        else:
            add(f"Already {hours} h > {h} — speed {mid} is too slow. Every "
                f"slower speed fails too, so search {mid + 1}..{hi}.",
                _answer(mid + 1, hi, mid, best, top))
            lo = mid + 1

    add(f"The range is empty: the minimum speed is {best} bananas/hour. "
        f"{counts['guesses']} guesses instead of trying all {top} speeds — "
        f"O(n log max).", _answer(lo, hi, None, best, top))
    return {
        "meta": {"algorithm": "koko_bananas", "view": "array",
                 "language": "python", "result": best},
        "array": arr,
        "steps": steps,
    }
