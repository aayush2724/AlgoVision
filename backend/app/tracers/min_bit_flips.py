"""Minimum bit flips to convert A to B.

A "flip" changes one bit. The bits you must flip are exactly the positions where
A and B differ — and A ^ B has a 1 in precisely those positions. So the answer is
the number of set bits in A ^ B. XOR finds the differences; popcount counts them.

Renders on the array view as a 12-bit row: first A, then B, then A ^ B whose set
bits (the required flips) glow green.
"""

WIDTH = 12
MAX_N = (1 << WIDTH) - 1


def _bits(n):
    return [(n >> (WIDTH - 1 - i)) & 1 for i in range(WIDTH)]


def _set_positions(n):
    return [[i, i] for i in range(WIDTH) if (n >> (WIDTH - 1 - i)) & 1]


def trace(a: int, b: int):
    a, b = int(a), int(b)
    steps: list = []
    x = a ^ b
    flips = bin(x).count("1")
    counts = {"flips": flips}

    def add(note, value, positions=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": _bits(value),
                "sorted_ranges": positions if positions is not None else [],
                "placed": None,
                "counts": dict(counts),
            },
            "highlight": {"index": None},
            "note": note,
        })

    add(f"A = {a}. Its bits are the starting point.", a, _set_positions(a))
    add(f"B = {b}. The target bit pattern.", b, _set_positions(b))
    add(f"A ^ B = {x}. A 1 marks every position where A and B disagree — each is "
        f"one flip. That is {flips} flip(s).", x, _set_positions(x))
    return {
        "meta": {"algorithm": "min_bit_flips", "view": "array",
                 "language": "python", "flips": flips},
        "array": _bits(x),
        "steps": steps,
    }
