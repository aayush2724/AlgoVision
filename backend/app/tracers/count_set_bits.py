"""Count set bits — Brian Kernighan's trick.

The naive way checks all bits; Kernighan's runs once per *set* bit. The key
identity: n & (n - 1) clears the lowest set bit. So repeatedly do n = n & (n-1)
and count the iterations — you touch only the ones, never the zeros.

Renders on the array view as a 12-bit row (MSB→LSB); set bits glow green, the
lowest set bit about to be cleared is highlighted.
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
    counts = {"set_bits": 0, "iterations": 0}

    def add(note, value, current=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": _bits(value),
                "sorted_ranges": _set_positions(value),
                "placed": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    add(f"n = {n} in binary. Kernighan's trick: n & (n-1) erases the lowest set "
        f"bit, so we loop once per 1-bit.", n)

    cur = n
    while cur:
        low = cur & -cur                      # isolate lowest set bit
        pos = WIDTH - low.bit_length()        # its column (MSB = 0)
        cur = cur & (cur - 1)
        counts["set_bits"] += 1
        counts["iterations"] += 1
        add(f"Clear the lowest set bit (value {low}) — count is now "
            f"{counts['set_bits']}. n becomes {cur}.", cur, current=pos)

    add(f"n hit 0 after {counts['iterations']} steps — {n} has "
        f"{counts['set_bits']} set bit(s).", 0)
    return {
        "meta": {"algorithm": "count_set_bits", "view": "array",
                 "language": "python", "set_bits": counts["set_bits"]},
        "array": _bits(n),
        "steps": steps,
    }
