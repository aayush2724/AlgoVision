"""Prime factorisation by trial division — break a number into its prime
building blocks.

Try the smallest divisor, 2, and keep dividing it out while it goes evenly;
move to 3, then 5, 7, … Once the trial divisor exceeds the square root of
what's left, whatever remains above 1 must itself be prime. Dividing the
number down as you go is what keeps this fast: the candidates shrink with it.

Reuses the `grid` view as a table that grows one row per factor pulled out:
the prime found and what remains to factor. No new renderer.
"""

MAX_VALUE = 100000


def trace(n: int):
    n = int(n)
    rows: list = []
    factors: list[int] = []
    steps: list = []
    counts = {"trials": 0, "factors": 0}

    def add(note, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [r[:] for r in rows],
                "row": len(rows) - 1 if rows else None,
                "col": None,
                "deps": [],
                "match": match,
                "path": [],
                "counts": dict(counts),
            },
            "highlight": {"index": None},
            "note": note,
        })

    add(f"Break {n} into primes by trial division: divide out 2 as often as it "
        f"goes, then 3, 5, 7, … Once a trial divisor passes √{n}, whatever is "
        f"left above 1 is prime.")

    if n < 2:
        add(f"{n} has no prime factorisation — factoring starts at 2.",
            match=True)
        return _result(n, factors, rows, steps)

    remaining = n
    d = 2
    while d * d <= remaining:
        counts["trials"] += 1
        if remaining % d == 0:
            while remaining % d == 0:
                factors.append(d)
                remaining //= d
                counts["factors"] += 1
                rows.append([d, remaining])
                add(f"{d} divides evenly — pull it out. {remaining} left to "
                    f"factor.")
        d += 1 if d == 2 else 2   # after 2, only odd candidates can be prime

    if remaining > 1:
        factors.append(remaining)
        counts["factors"] += 1
        rows.append([remaining, 1])
        add(f"{remaining} is bigger than √(original) and above 1 — it must be "
            f"prime. Pull it out; nothing remains.")

    pretty = " × ".join(str(f) for f in factors)
    add(f"{n} = {pretty}. Trial division only tested up to √{n}, which is why "
        f"it stays fast even though the number is large.", match=True)
    return _result(n, factors, rows, steps)


def _result(n, factors, rows, steps):
    return {
        "meta": {
            "algorithm": "prime_factorisation",
            "view": "grid",
            "language": "python",
            "rows": len(rows),
            "cols": 2,
            "row_labels": [str(i) for i in range(len(rows))],
            "col_labels": ["prime", "remaining"],
            "n": n,
            "factors": factors,
            "result": factors,
        },
        "steps": steps,
    }
