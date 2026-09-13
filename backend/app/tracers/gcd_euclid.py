"""Euclid's algorithm — the greatest common divisor, by repeated remainder.

gcd(a, b) = gcd(b, a mod b): whatever divides both a and b also divides their
remainder, so replacing the pair with (b, a mod b) never loses the answer but
always shrinks the numbers. When the remainder hits 0 the other number is the
gcd. It is one of the oldest algorithms there is, and it is breathtakingly
fast.

Reuses the `grid` view as a computation table that grows one row per step:
columns a, b, and a mod b. The final row, where the remainder is 0, names the
gcd. No new renderer.
"""

MAX_VALUE = 100000


def trace(a: int, b: int):
    a, b = int(a), int(b)
    rows: list = []
    steps: list = []
    counts = {"divisions": 0}

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

    add(f"gcd({a}, {b}) by Euclid's rule: gcd(a, b) = gcd(b, a mod b). Each step "
        f"replaces the pair with (b, remainder) — always smaller, never losing "
        f"the answer. When the remainder is 0, the other number is the gcd.")

    x, y = a, b
    while y != 0:
        r = x % y
        rows.append([x, y, r])
        counts["divisions"] += 1
        add(f"{x} mod {y} = {r}. Drop {x}; carry ({y}, {r}) to the next row.")
        x, y = y, r

    # y is 0 now; x holds the gcd (and gcd(0, 0) is defined here as 0).
    rows.append([x, 0, "—"])
    add(f"The remainder is 0, so the algorithm stops: gcd({a}, {b}) = {x}. It "
        f"took {counts['divisions']} division(s) — Euclid's method is "
        f"logarithmic in the smaller number, not linear.", match=True)

    return {
        "meta": {
            "algorithm": "gcd_euclid",
            "view": "grid",
            "language": "python",
            "rows": len(rows),
            "cols": 3,
            "row_labels": [str(i) for i in range(len(rows))],
            "col_labels": ["a", "b", "a mod b"],
            "result": x,
        },
        "steps": steps,
    }
