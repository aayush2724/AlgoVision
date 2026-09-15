"""Single Number — find the one unpaired value with XOR.

Every number that appears twice cancels itself, because x ^ x = 0, and XOR is
commutative, so order doesn't matter. Fold the whole array with XOR and whatever
survives is the lone number. O(n) time, O(1) space — no hash set needed.

Renders on the array view as the running XOR's 12-bit row; set bits glow green.
"""

WIDTH = 12
MAX_N = (1 << WIDTH) - 1


def _bits(n):
    return [(n >> (WIDTH - 1 - i)) & 1 for i in range(WIDTH)]


def _set_positions(n):
    return [[i, i] for i in range(WIDTH) if (n >> (WIDTH - 1 - i)) & 1]


def trace(nums: list[int]):
    values = [int(v) for v in nums]
    steps: list = []
    counts = {"xored": 0, "acc": 0}

    def add(note, value):
        counts["acc"] = value
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": _bits(value),
                "sorted_ranges": _set_positions(value),
                "placed": None,
                "counts": dict(counts),
            },
            "highlight": {"index": None},
            "note": note,
        })

    add(f"Fold {values} with XOR. Pairs cancel (x ^ x = 0); the accumulator "
        f"starts at 0.", 0)

    acc = 0
    for v in values:
        acc ^= v
        counts["xored"] += 1
        add(f"XOR in {v} → accumulator is now {acc}. Its bits are the running "
            f"parity of every value seen.", acc)

    add(f"Everything paired has cancelled — the survivor is {acc}, the single "
        f"number.", acc)
    return {
        "meta": {"algorithm": "single_number", "view": "array",
                 "language": "python", "single": acc},
        "array": _bits(acc),
        "steps": steps,
    }
