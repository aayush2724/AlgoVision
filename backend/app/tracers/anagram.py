"""Anagram check — are two words rearrangements of the same letters?

Sort both words and they become identical exactly when they are anagrams:
same letters, same counts, only the order differed. Different lengths can be
rejected on sight. It is the cleanest proof that "same multiset of characters"
is all an anagram really means.

Reuses the `grid` view as two rows — the sorted letters of each word — compared
column by column. A column where the letters differ (or a length mismatch)
settles it. No new renderer.
"""

MAX_LEN = 12


def trace(a: str, b: str):
    sa, sb = sorted(a), sorted(b)
    width = max(len(sa), len(sb), 1)
    # Two rows, padded so the grid stays rectangular for the renderer.
    row_a = [sa[i] if i < len(sa) else "·" for i in range(width)]
    row_b = [sb[i] if i < len(sb) else "·" for i in range(width)]
    steps: list = []
    counts = {"comparisons": 0, "mismatches": 0}

    def add(note, col=None, match=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "grid": [row_a[:], row_b[:]],
                "row": None,
                "col": col,
                "deps": [[0, col], [1, col]] if col is not None else [],
                "match": match,
                "path": [],
                "counts": dict(counts),
            },
            "highlight": {"index": col},
            "note": note,
        })

    add(f"Are '{a}' and '{b}' anagrams? Sort each word: if the sorted letters "
        f"line up position for position, they use exactly the same letters the "
        f"same number of times. The rows below are '{a}' and '{b}', sorted.")

    if len(a) != len(b):
        counts["mismatches"] += 1
        add(f"'{a}' has {len(a)} letters and '{b}' has {len(b)} — different "
            f"lengths can't be anagrams. Done.", match=False)
        return _result(a, b, False, steps)

    is_anagram = True
    for c in range(width):
        counts["comparisons"] += 1
        if row_a[c] == row_b[c]:
            add(f"Column {c}: '{row_a[c]}' = '{row_b[c]}' — still matching.",
                col=c, match=True)
        else:
            counts["mismatches"] += 1
            is_anagram = False
            add(f"Column {c}: '{row_a[c]}' ≠ '{row_b[c]}'. The sorted letters "
                f"diverge here, so these are NOT anagrams.", col=c, match=False)
            break

    if is_anagram:
        add(f"Every column matched — '{a}' and '{b}' are anagrams. Sorting both "
            f"is O(n log n); a letter-count map would make it O(n).")
    return _result(a, b, is_anagram, steps)


def _result(a, b, is_anagram, steps):
    return {
        "meta": {
            "algorithm": "anagram",
            "view": "grid",
            "language": "python",
            "rows": 2,
            "cols": max(len(a), len(b), 1),
            "row_labels": ["A", "B"],
            "col_labels": [str(i) for i in range(max(len(a), len(b), 1))],
            "result": is_anagram,
        },
        "steps": steps,
    }
