"""Power of two — the one-line bit test.

A positive number is a power of two exactly when it has a single set bit. And
n & (n - 1) clears the lowest set bit, so for a power of two that operation wipes
out the only bit and gives 0. Hence: n > 0 and (n & (n - 1)) == 0.

Renders on the array view as a 12-bit row; set bits glow green.
"""

WIDTH = 12
MAX_N = (1 << WIDTH) - 1


def _bits(n):
    return [(n >> (WIDTH - 1 - i)) & 1 for i in range(WIDTH)]


def _set_positions(n):
    return [[i, i] for i in range(WIDTH) if (n >> (WIDTH - 1 - i)) & 1]


def trace(n: int):
    n = int(n)
    steps: list = []
    ones = bin(n if n > 0 else 0).count("1")
    counts = {"set_bits": ones}

    def add(note, value, current=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": _bits(value),
                "sorted_ranges": _set_positions(value),
                "placed": current,
                "counts": dict(counts),
                "found": None,
            },
            "highlight": {"index": current},
            "note": note,
        })

    add(f"n = {n} in binary. A power of two has exactly one set bit — count "
        f"them.", n if n > 0 else 0)

    if n <= 0:
        add(f"{n} is not positive, so it cannot be a power of two.", 0)
        is_pow = False
    else:
        masked = n & (n - 1)
        add(f"Compute n & (n-1) = {masked}. This clears the lowest set bit.",
            masked)
        is_pow = masked == 0
        if is_pow:
            add(f"Result is 0 — the lone set bit was the only one. {n} IS a "
                f"power of two (2^{n.bit_length() - 1}).", n)
        else:
            add(f"Result is {masked} (not 0) — more than one set bit. {n} is NOT "
                f"a power of two.", n)

    return {
        "meta": {"algorithm": "power_of_two", "view": "array",
                 "language": "python", "is_power_of_two": bool(is_pow)},
        "array": _bits(n if n > 0 else 0),
        "steps": steps,
    }
