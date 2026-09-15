"""Power set via bit masks — every subset is a binary number.

For n elements there are 2^n subsets, and each maps to an n-bit mask: bit i on
means "element i is in". Counting masks from 0 to 2^n - 1 therefore enumerates
every subset exactly once, no recursion required. Column i of the row is
element i; a lit column means it is chosen.

Renders on the array view: the mask's bits (chosen elements glow green).
"""

MAX_ELEMENTS = 5


def trace(elements: list[str]):
    els = list(elements)
    n = len(els)
    steps: list = []
    counts = {"subsets": 0, "elements": n}

    def add(note, mask):
        bits = [(mask >> i) & 1 for i in range(n)]   # column i == element i
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": bits,
                "sorted_ranges": [[i, i] for i in range(n) if bits[i]],
                "placed": None,
                "counts": dict(counts),
            },
            "highlight": {"index": None},
            "note": note,
        })

    if not n:
        add("No elements — the only subset is the empty set.", 0)
        return _result(els, steps, [[]])

    add(f"{n} elements {els} → {2 ** n} subsets. Each subset is an {n}-bit mask; "
        f"count from 0 up and read off the chosen elements.", 0)

    subsets = []
    for mask in range(2 ** n):
        chosen = [els[i] for i in range(n) if (mask >> i) & 1]
        subsets.append(chosen)
        counts["subsets"] += 1
        shown = ("{" + ", ".join(chosen) + "}") if chosen else "{} (empty set)"
        add(f"Mask {mask:0{n}b} → {shown}.", mask)

    add(f"All {2 ** n} subsets enumerated — the complete power set.", 0)
    return _result(els, steps, subsets)


def _result(els, steps, subsets):
    return {
        "meta": {"algorithm": "power_set", "view": "array", "language": "python",
                 "count": len(subsets)},
        "array": [0] * len(els),
        "steps": steps,
    }
