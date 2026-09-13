"""The Z-function — for every position, how much of the string's own prefix
starts again right here?

Z[i] is the length of the longest substring starting at i that matches a
prefix of the whole string. The trick is the [l, r] "Z-box": the widest match
found so far. When i falls inside it, the already-known value at the mirror
position i-l gives Z[i] for free, so we rarely re-compare from scratch — that
is what makes the whole pass linear.

Reuses the `array` view: cells are the characters, `placed` marks i, `merging`
draws the current Z-box, and `sorted_ranges` lights the matched run green. The
Z value itself rides in the note. No new renderer.
"""

MAX_LEN = 22


def trace(text: str):
    s = text
    n = len(s)
    z = [0] * n
    steps: list = []
    counts = {"comparisons": 0, "box_reuses": 0, "matches": 0}

    def add(note, placed=None, box=None, matched=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(s),
                "placed": placed,
                "merging": list(box) if box else None,
                "sorted_ranges": [list(matched)] if matched else [],
                "z": list(z),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    add(f"For each position i, Z[i] is how long a run starting at i also starts "
        f"the whole string '{s}'. The [l, r] Z-box remembers the widest match "
        f"so far and lets mirror positions copy their answer.", placed=0)

    if n:
        z[0] = n  # by convention the whole string matches its own prefix
        add(f"Z[0] is the whole string by convention ({n}).", placed=0)

    l = r = 0
    for i in range(1, n):
        if i < r:
            mirror = i - l
            z[i] = min(r - i, z[mirror])
            counts["box_reuses"] += 1
            add(f"i={i} sits inside the Z-box [{l}, {r - 1}]. Its mirror "
                f"(position {mirror}) scored {z[mirror]}, so start from "
                f"{z[i]} instead of 0.", placed=i, box=[l, r - 1])
        # Try to extend the match past what we already know.
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            counts["comparisons"] += 1
            z[i] += 1
        if z[i]:
            counts["matches"] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
            add(f"Extended: Z[{i}] = {z[i]} ('{s[i:i + z[i]]}' restarts the "
                f"prefix). The Z-box grows to [{l}, {r - 1}].",
                placed=i, box=[l, r - 1] if r > l else None,
                matched=[i, i + z[i] - 1] if z[i] else None)
        else:
            add(f"Z[{i}] = {z[i]} — position {i} shares "
                f"{'nothing' if not z[i] else str(z[i]) + ' char(s)'} with the "
                f"prefix.", placed=i,
                matched=[i, i + z[i] - 1] if z[i] else None)

    best = max(range(n), key=lambda k: z[k]) if n else 0
    add(f"Done. The longest internal prefix-match is Z[{best}] = "
        f"{z[best] if n else 0}. Every character was compared at most a "
        f"constant number of times — the Z-box is why this is O(n).",
        placed=best)

    return {
        "meta": {
            "algorithm": "z_function",
            "view": "array",
            "language": "python",
            "text": s,
            "z": z,
            "result": max(z[1:], default=0),
        },
        "array": list(s),
        "steps": steps,
    }
