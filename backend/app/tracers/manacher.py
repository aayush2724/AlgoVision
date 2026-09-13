"""Manacher's algorithm — the longest palindromic substring in O(n).

The trick that makes brute force (O(n²) centres × O(n) expansion) collapse to
linear is a mirror: we keep the rightmost palindrome found so far, and any
centre inside it can copy its mirror centre's radius instead of expanding from
zero. To treat odd- and even-length palindromes uniformly the string is
interleaved with separators ('#a#b#a#') so every palindrome has a single
centre — but we report spans back on the *original* string.

Reuses the `array` view: cells are the original characters, `merging` is the
palindrome currently growing around a centre, and `sorted_ranges` keeps the
best palindrome lit green. The radius rides in the note. No new renderer.
"""

MAX_LEN = 18


def trace(text: str):
    s = text
    n = len(s)
    steps: list = []
    counts = {"centres": 0, "expansions": 0, "mirror_reuses": 0}
    best_len = 0
    best_start = 0

    # Interleave with '#': T has a single centre for every palindrome, odd or
    # even. A radius p in T equals the palindrome's length in s.
    t = "#" + "#".join(s) + "#"
    m = len(t)
    p = [0] * m

    def raw_span(i):
        """Map transformed centre i with radius p[i] back to s-coordinates."""
        length = p[i]
        if length == 0:
            return None
        start = (i - length) // 2
        return [start, start + length - 1]

    def add(note, window=None, best=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(s),
                "placed": None,
                "merging": list(window) if window else None,
                "sorted_ranges": [list(best)] if best else [],
                "counts": dict(counts),
            },
            "highlight": {"index": None},
            "note": note,
        })

    add(f"Find the longest palindrome inside '{s}'. Interleaving with '#' gives "
        f"every palindrome one centre; the rightmost one found so far lets "
        f"inner centres copy a radius instead of expanding from scratch.")

    if n == 0:
        add("Empty string — the longest palindrome has length 0.")
        return _result(s, "", 0, steps)

    c = r = 0
    for i in range(1, m - 1):
        counts["centres"] += 1
        reused = ""
        if i < r:
            mirror = 2 * c - i
            p[i] = min(r - i, p[mirror])
            counts["mirror_reuses"] += 1
            reused = (f" Inside the current palindrome, so copy the mirror's "
                      f"radius to start at {p[i]}.")
        grew = 0
        while (i - p[i] - 1 >= 0 and i + p[i] + 1 < m
               and t[i - p[i] - 1] == t[i + p[i] + 1]):
            p[i] += 1
            grew += 1
            counts["expansions"] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
        span = raw_span(i)
        if p[i] > best_len:
            best_len = p[i]
            best_start = (i - p[i]) // 2
        best_span = [best_start, best_start + best_len - 1] if best_len else None
        centre_desc = (f"character '{s[(i - 1) // 2]}'" if i % 2
                       else "the gap between two characters")
        if span:
            add(f"Centre at {centre_desc}: radius {p[i]} → palindrome "
                f"'{s[span[0]:span[1] + 1]}'.{reused} "
                f"{'Expanded ' + str(grew) + ' step(s).' if grew else ''}".strip(),
                window=span, best=best_span)
        else:
            add(f"Centre at {centre_desc}: no palindrome longer than a single "
                f"point here.{reused}", best=best_span)

    longest = s[best_start:best_start + best_len]
    add(f"The longest palindrome is '{longest}' (length {best_len}). The mirror "
        f"rule kept every character inside a constant amount of work, so the "
        f"whole scan is O(n) — not the O(n²) of expanding around every centre.",
        window=[best_start, best_start + best_len - 1] if best_len else None,
        best=[best_start, best_start + best_len - 1] if best_len else None)
    return _result(s, longest, best_len, steps)


def _result(s, longest, length, steps):
    return {
        "meta": {
            "algorithm": "manacher",
            "view": "array",
            "language": "python",
            "text": s,
            "longest": longest,
            "result": length,
        },
        "array": list(s),
        "steps": steps,
    }
