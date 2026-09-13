"""Radix sort (LSD) — sort whole numbers without ever comparing two of them.

One pass per digit, least-significant first. Each pass is a *stable* bucket
sort on a single digit: numbers drop into ten bins 0–9 in order, then the bins
are read back left to right. Because each pass preserves the order the earlier
passes established, after the last digit the whole array is sorted.

Reuses the `array` view: cells are the current order (they physically reorder
each pass), `placed` marks the number being bucketed, and the digit under
examination rides in the note. No new renderer.
"""

MAX_ARRAY_LEN = 12
MAX_VALUE = 9999


def trace(nums: list):
    arr = [int(x) for x in nums]
    n = len(arr)
    steps: list = []
    counts = {"passes": 0, "placements": 0, "collects": 0}

    def add(note, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "placed": placed,
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    add("Radix sort never compares two numbers. It sorts by one digit at a "
        "time, least-significant first, and each pass is a stable bucket sort "
        "that keeps the order the earlier passes already fixed.")

    if n <= 1:
        add("Nothing to sort — an array of 0 or 1 element is already ordered.")
        return _result(arr, steps)

    max_val = max(arr)
    digit = 1
    place_name = ["ones", "tens", "hundreds", "thousands"]
    pos = 0
    while max_val // digit > 0:
        counts["passes"] += 1
        buckets: list[list[int]] = [[] for _ in range(10)]
        name = place_name[pos] if pos < len(place_name) else f"10^{pos}"
        add(f"Pass {counts['passes']}: sort on the {name} digit. Drop each "
            f"number into the bin for that digit, keeping their current order.")
        for idx, v in enumerate(arr):
            d = (v // digit) % 10
            buckets[d].append(v)
            counts["placements"] += 1
            add(f"{v} has {name} digit {d} → bin {d}.", placed=idx)
        arr = [v for b in buckets for v in b]
        counts["collects"] += 1
        add(f"Read the bins 0→9 back into the array: {arr}. The {name} digit is "
            f"now ordered, and every earlier digit's order survived.")
        digit *= 10
        pos += 1

    add(f"After {counts['passes']} pass(es) — one per digit — the array is "
        f"sorted: {arr}. No two numbers were ever compared; the cost is "
        f"O(passes × n), linear in the count for a fixed number of digits.")
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {
            "algorithm": "radix_sort",
            "view": "array",
            "language": "python",
            "result": arr,
        },
        "array": list(arr),
        "steps": steps,
    }
