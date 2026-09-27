"""More binary search on the answer — square root, nth root, bouquets.

Same idea as Koko: the thing being searched is a range of candidate answers,
and a yes/no check flips exactly once across it.

* sqrt_search — floor(√n): the largest x with x·x ≤ n, over 1..n.
* nth_root — the x with xⁿ = m exactly (or none), over 1..m.
* min_bouquets — the earliest day on which m bouquets of k *adjacent* bloomed
  flowers can be made, over min(bloom)..max(bloom). If m·k exceeds the number
  of flowers, no day works.

Reuses the `array` view plus the optional `answer` number line (range,
guess, best). For the roots the cells just hold the inputs; for bouquets the
cells are the flowers — bloomed ones green, the run being counted orange.
"""

TITLES = {
    "sqrt_search": "Square Root (Binary Search)",
    "nth_root": "Nth Root of a Number",
    "min_bouquets": "Minimum Days to Make M Bouquets",
}
MAX_N = 1_000_000
MAX_FLOWERS = 12


def validate(algo, arr, target_text):
    if algo == "sqrt_search":
        if len(arr) != 1 or arr[0] != int(arr[0]) or not (1 <= arr[0] <= MAX_N):
            return f"Give one whole number n, 1–{MAX_N}."
    elif algo == "nth_root":
        if len(arr) != 2 or any(v != int(v) for v in arr):
            return "Give two whole numbers: n, m (find the nth root of m)."
        if not (1 <= arr[0] <= 10) or not (1 <= arr[1] <= MAX_N):
            return f"n must be 1–10 and m 1–{MAX_N}."
    else:
        if not arr or len(arr) > MAX_FLOWERS:
            return f"Give 1–{MAX_FLOWERS} bloom days."
        if any(v != int(v) or not (1 <= v <= 1000) for v in arr):
            return "Bloom days must be whole numbers 1–1000."
        if _parse_mk(target_text) is None:
            return "Give M and K as 'M, K' (each 1–12) — e.g. 3, 1."
    return None


def _parse_mk(text):
    parts = [p for p in (text or "").replace(" ", "").split(",") if p]
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        return None
    m, k = int(parts[0]), int(parts[1])
    return (m, k) if 1 <= m <= 12 and 1 <= k <= 12 else None


def trace(algo, array, target_text=None):
    arr = [int(v) for v in array]
    if algo == "min_bouquets":
        return _bouquets(arr, *_parse_mk(target_text))
    steps: list = []
    counts = {"guesses": 0}

    def line(lo, hi, mid, best, top):
        return {"min": 1, "max": top, "lo": lo, "hi": hi, "mid": mid,
                "best": best, "label": "CANDIDATE x"}

    def add(note, answer, found=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"array": arr[:],
                                     "placed": 0 if found is None else None,
                                     "sorted_ranges": [[0, len(arr) - 1]] if found else [],
                                     "answer": answer, "counts": dict(counts)},
                      "highlight": {"index": 0}, "note": note})

    if algo == "sqrt_search":
        n = arr[0]
        lo, hi, best = 1, n, None
        add(f"floor(√{n}) is the largest x with x·x ≤ {n}. Small x pass, big x "
            f"fail — binary-search x over 1..{n}.", line(lo, hi, None, best, n))
        while lo <= hi:
            mid = (lo + hi) // 2
            counts["guesses"] += 1
            sq = mid * mid
            if sq <= n:
                best = mid
                add(f"{mid}² = {sq} ≤ {n} — {mid} works. Try bigger: "
                    f"{mid + 1}..{hi}.", line(mid + 1, hi, mid, best, n))
                lo = mid + 1
            else:
                add(f"{mid}² = {sq} > {n} — too big. Try smaller: "
                    f"{lo}..{mid - 1}.", line(lo, mid - 1, mid, best, n))
                hi = mid - 1
        add(f"floor(√{n}) = {best}, found in {counts['guesses']} guesses.",
            line(lo, hi, None, best, n), found=True)
        result = best
    else:
        p, m = arr
        lo, hi, best = 1, m, None
        add(f"Find x with x^{p} = {m} exactly. x^{p} only grows with x, so "
            f"binary-search x over 1..{m}.", line(lo, hi, None, best, m))
        result = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            counts["guesses"] += 1
            val = mid ** p
            if val == m:
                best = result = mid
                add(f"{mid}^{p} = {m} exactly — found it.",
                    line(lo, hi, mid, best, m), found=True)
                break
            if val < m:
                add(f"{mid}^{p} = {val} < {m} — go bigger: {mid + 1}..{hi}.",
                    line(mid + 1, hi, mid, best, m))
                lo = mid + 1
            else:
                add(f"{mid}^{p} = {val} > {m} — go smaller: {lo}..{mid - 1}.",
                    line(lo, mid - 1, mid, best, m))
                hi = mid - 1
        if result == -1:
            add(f"The range is empty: no whole number x has x^{p} = {m}, so the "
                f"answer is -1.", line(lo, hi, None, None, m), found=False)
    return {"meta": {"algorithm": algo, "view": "array", "language": "python",
                     "result": result},
            "array": arr, "steps": steps}


def _bouquets(arr, m, k):
    steps: list = []
    counts = {"guesses": 0, "flower_checks": 0}
    a, b = min(arr), max(arr)

    def line(lo, hi, mid, best):
        return {"min": a, "max": b, "lo": lo, "hi": hi, "mid": mid,
                "best": best, "label": "DAY"}

    def add(note, answer, placed=None, bloomed=(), run=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"array": arr[:], "placed": placed,
                                     "sorted_ranges": [[j, j] for j in bloomed],
                                     "merging": list(run) if run else None,
                                     "answer": answer, "counts": dict(counts)},
                      "highlight": {"index": placed}, "note": note})

    if m * k > len(arr):
        add(f"{m} bouquets × {k} flowers = {m * k} flowers, but only "
            f"{len(arr)} exist — impossible on any day. Answer: -1.",
            line(a, b, None, None))
        return {"meta": {"algorithm": "min_bouquets", "view": "array",
                         "language": "python", "result": -1},
                "array": arr, "steps": steps}

    lo, hi, best = a, b, None
    add(f"Make {m} bouquets, each of {k} adjacent bloomed flowers. Waiting "
        f"longer only helps, so binary-search the day over {a}..{b}.",
        line(lo, hi, None, best))
    while lo <= hi:
        day = (lo + hi) // 2
        counts["guesses"] += 1
        made, run, start = 0, 0, 0
        bloomed = []
        add(f"Guess day {day}. Walk the flowers, counting adjacent runs.",
            line(lo, hi, day, best))
        for i, d in enumerate(arr):
            counts["flower_checks"] += 1
            if d <= day:
                bloomed.append(i)
                if run == 0:
                    start = i
                run += 1
                if run == k:
                    made += 1
                    add(f"Flower {i} has bloomed (day {d}) — a run of {k}: "
                        f"bouquet #{made}.", line(lo, hi, day, best), i,
                        bloomed, (start, i))
                    run = 0
                else:
                    add(f"Flower {i} has bloomed (day {d}) — run is now {run}.",
                        line(lo, hi, day, best), i, bloomed, (start, i))
            else:
                run = 0
                add(f"Flower {i} blooms on day {d}, after {day} — the run "
                    f"breaks.", line(lo, hi, day, best), i, bloomed)
        if made >= m:
            best = day
            add(f"{made} bouquet(s) ≥ {m} on day {day} — works. Try earlier: "
                f"{lo}..{day - 1}.", line(lo, day - 1, day, best), bloomed=bloomed)
            hi = day - 1
        else:
            add(f"Only {made} bouquet(s) on day {day} — too early. Try later: "
                f"{day + 1}..{hi}.", line(day + 1, hi, day, best), bloomed=bloomed)
            lo = day + 1
    add(f"Earliest day: {best}. {counts['guesses']} guesses instead of "
        f"checking every day from {a} to {b}.", line(lo, hi, None, best))
    return {"meta": {"algorithm": "min_bouquets", "view": "array",
                     "language": "python", "result": best},
            "array": arr, "steps": steps}
