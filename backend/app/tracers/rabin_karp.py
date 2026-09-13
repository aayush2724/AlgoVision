"""Rabin–Karp substring search — compare a cheap fingerprint first, the
characters only when the fingerprints agree.

Every window of the text is hashed. A rolling hash updates that fingerprint in
O(1) as the window slides: subtract the leaving character, shift, add the
entering one. A window whose hash differs from the pattern's cannot match, so
it is skipped without touching a single character. Equal hashes are only a
*hint* — they still need one character check to rule out a collision.

Reuses the `array` view: cells are the text, `merging` is the current window,
`placed` marks its start, and `sorted_ranges` lights confirmed matches green.
The rolling hash rides in the note. No new renderer.
"""

MAX_TEXT = 24
MAX_PATTERN = 12

BASE = 256
MOD = 1_000_000_007


def trace(text: str, pattern: str):
    n, m = len(text), len(pattern)
    steps: list = []
    counts = {"hashes": 0, "hash_hits": 0, "char_checks": 0,
              "collisions": 0, "matches": 0}
    matches: list[int] = []

    def add(note, placed=None, window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(text),
                "placed": placed,
                "merging": list(window) if window else None,
                "sorted_ranges": [[k, k + m - 1] for k in matches],
                "pattern": list(pattern),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if m == 0 or m > n:
        add(f"Pattern '{pattern}' cannot fit in '{text}' — nothing to search.")
        return _result(text, pattern, matches, steps)

    # Pattern hash and the first window hash, plus BASE^(m-1) for the roll.
    patt_hash = 0
    win_hash = 0
    high = pow(BASE, m - 1, MOD)
    for k in range(m):
        patt_hash = (patt_hash * BASE + ord(pattern[k])) % MOD
        win_hash = (win_hash * BASE + ord(text[k])) % MOD
    counts["hashes"] += 2
    add(f"Fingerprint the pattern '{pattern}' (hash {patt_hash % 1000:03d}…) "
        f"and the first window '{text[:m]}' (hash {win_hash % 1000:03d}…). "
        f"Only windows whose fingerprint matches are worth a closer look.",
        placed=0, window=[0, m - 1])

    for i in range(n - m + 1):
        if i > 0:
            # Roll: drop text[i-1], shift, add text[i+m-1] — O(1), not O(m).
            win_hash = ((win_hash - ord(text[i - 1]) * high) * BASE
                        + ord(text[i + m - 1])) % MOD
            counts["hashes"] += 1
            add(f"Slide to index {i}: roll the hash — drop '{text[i - 1]}', "
                f"add '{text[i + m - 1]}' → {win_hash % 1000:03d}…. One "
                f"operation, not a full rehash.", placed=i, window=[i, i + m - 1])
        if win_hash == patt_hash:
            counts["hash_hits"] += 1
            if text[i:i + m] == pattern:
                counts["char_checks"] += 1
                counts["matches"] += 1
                matches.append(i)
                add(f"Fingerprints agree at index {i} and the characters "
                    f"confirm it — '{pattern}' found here.",
                    placed=i, window=[i, i + m - 1])
            else:
                counts["char_checks"] += 1
                counts["collisions"] += 1
                add(f"Fingerprints agree at index {i} but the characters differ "
                    f"— a hash collision, not a match. This is why the check is "
                    f"never skipped.", placed=i, window=[i, i + m - 1])

    if matches:
        where = ", ".join(str(x) for x in matches)
        add(f"Found '{pattern}' at index {where}. Most windows were dismissed "
            f"on their fingerprint alone — characters were compared only "
            f"{counts['char_checks']} time(s).")
    else:
        add(f"'{pattern}' never appears. The rolling hash screened every "
            f"window in O(1); characters were touched only "
            f"{counts['char_checks']} time(s).")
    return _result(text, pattern, matches, steps)


def _result(text, pattern, matches, steps):
    return {
        "meta": {
            "algorithm": "rabin_karp",
            "view": "array",
            "language": "python",
            "text": text,
            "pattern": pattern,
            "matches": matches,
        },
        "array": list(text),
        "steps": steps,
    }
