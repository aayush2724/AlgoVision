"""KMP substring search — never re-read a character you already matched.

Two phases, and the first is the one that matters: the failure table records,
for each prefix of the pattern, the longest proper prefix that is also a
suffix. That table is what lets the search slide the pattern forward without
ever moving the text pointer backwards.
"""

MAX_TEXT = 24
# 12, not 8: the canonical teaching example (ABABDABACDABABCABAB / ABABCABAB)
# has a 9-character pattern and must fit.
MAX_PATTERN = 12


def trace(text: str, pattern: str):
    n, m = len(text), len(pattern)
    steps: list = []
    counts = {"comparisons": 0, "shifts": 0, "matches": 0, "naive_would_cost": n * m}
    lps = [0] * m
    matches: list[int] = []

    def add(note, placed=None, window=None, marked=None, phase="search"):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(text),
                "placed": placed,
                "merging": list(window) if window else None,
                "sorted_ranges": [[mk, mk + m - 1] for mk in (marked or [])],
                "pattern": list(pattern),
                "lps": list(lps),
                "phase": phase,
                "matches": list(matches),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    add(f"Find '{pattern}' inside '{text}'. First build the failure table — "
        f"for each prefix of the pattern, how much of it is both a prefix and "
        f"a suffix. That is what lets us skip ahead safely.", phase="table")

    # ── Phase 1: the failure (LPS) table ──
    length = 0
    i = 1
    while i < m:
        counts["comparisons"] += 1
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            add(f"'{pattern[i]}' extends the border to length {length} — "
                f"'{pattern[:length]}' is both a prefix and a suffix of "
                f"'{pattern[:i + 1]}'.", phase="table")
            i += 1
        elif length:
            add(f"'{pattern[i]}' breaks the border — fall back to the shorter "
                f"border of length {lps[length - 1]} instead of starting over.",
                phase="table")
            length = lps[length - 1]
        else:
            lps[i] = 0
            add(f"'{pattern[i]}' shares nothing with the start — border 0.",
                phase="table")
            i += 1

    add(f"Failure table: {lps}. Now scan the text; the text pointer only ever "
        f"moves forward.", phase="table")

    # ── Phase 2: the scan ──
    i = j = 0
    while i < n:
        counts["comparisons"] += 1
        if text[i] == pattern[j]:
            add(f"'{text[i]}' matches pattern position {j} — advance both.",
                placed=i, window=[i - j, i], marked=list(matches))
            i += 1
            j += 1
            if j == m:
                start = i - m
                matches.append(start)
                counts["matches"] += 1
                add(f"Whole pattern matched at index {start}. Slide by the "
                    f"border ({lps[j - 1]}) and keep going — no need to "
                    f"restart at {start + 1}.",
                    placed=start, window=[start, i - 1], marked=list(matches))
                j = lps[j - 1]
                counts["shifts"] += 1
        else:
            if j:
                counts["shifts"] += 1
                add(f"'{text[i]}' breaks the match at pattern position {j}. "
                    f"The failure table says {lps[j - 1]} characters still "
                    f"line up, so jump the pattern there — the text pointer "
                    f"stays at {i}.",
                    placed=i, window=[i - j, i], marked=list(matches))
                j = lps[j - 1]
            else:
                add(f"'{text[i]}' does not start a match — step forward.",
                    placed=i, marked=list(matches))
                i += 1

    if matches:
        where = ", ".join(str(x) for x in matches)
        add(f"Found '{pattern}' at index {where}. {counts['comparisons']} "
            f"comparisons — the naive nested loop could have needed up to "
            f"{counts['naive_would_cost']}.", marked=list(matches))
    else:
        add(f"'{pattern}' never appears. Still only {counts['comparisons']} "
            f"comparisons, because the text pointer never backed up.")

    return {
        "meta": {
            "algorithm": "kmp_search",
            "view": "array",
            "language": "python",
            "text": text,
            "pattern": pattern,
            "lps": lps,
            "matches": matches,
        },
        "array": list(text),
        "steps": steps,
    }
