"""Fast (binary) exponentiation — base^exp in O(log exp) multiplications.

Read the exponent in binary, most-significant bit first. Start the result at 1
and, for each bit, square the running result; when the bit is 1, also multiply
by the base once. Squaring doubles the exponent you've built so far, and the
set bits add the rest — so log(exp) steps reach the full power instead of exp
of them.

Reuses the `grid` view as a table that grows one row per bit: the bit, the
operation, and the running result. No new renderer.
"""

MAX_BASE = 12
MAX_EXP = 20


def trace(base: int, exp: int):
    base, exp = int(base), int(exp)
    bits = bin(exp)[2:] if exp > 0 else "0"
    rows: list = []
    steps: list = []
    counts = {"squarings": 0, "multiplies": 0}
    result = 1

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

    add(f"Compute {base}^{exp}. Write {exp} in binary as {bits}, then read it "
        f"left to right: start at 1, square the result for every bit, and "
        f"multiply in an extra {base} whenever the bit is 1. Only "
        f"{len(bits)} step(s) — that is the log.")

    if exp == 0:
        rows.append(["—", "start", 1])
        add(f"Anything to the power 0 is 1, so {base}^0 = 1.", match=True)
        return _result(base, exp, 1, rows, steps)

    for bit in bits:
        result = result * result
        counts["squarings"] += 1
        op = "square"
        if bit == "1":
            result = result * base
            counts["multiplies"] += 1
            op = f"square, ×{base}"
        rows.append([int(bit), op, result])
        add(f"Bit {bit}: square the result"
            + (f", then multiply by {base}" if bit == "1" else "")
            + f" → {result}.")

    add(f"All {len(bits)} bit(s) consumed: {base}^{exp} = {result}. "
        f"{counts['squarings']} squaring(s) and {counts['multiplies']} "
        f"multiply(ies) — versus {exp} multiplications the naive way.",
        match=True)
    return _result(base, exp, result, rows, steps)


def _result(base, exp, result, rows, steps):
    return {
        "meta": {
            "algorithm": "fast_exponentiation",
            "view": "grid",
            "language": "python",
            "rows": len(rows),
            "cols": 3,
            "row_labels": [str(i) for i in range(len(rows))],
            "col_labels": ["bit", "op", "result"],
            "result": result,
        },
        "steps": steps,
    }
