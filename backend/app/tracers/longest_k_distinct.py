"""Longest substring with at most K distinct characters — the counted window.

Keep a count of how many of each character sit inside the window. Extend the
right edge; whenever the window holds more than K distinct characters, shrink
from the left, dropping counts to zero as characters leave, until only K distinct
remain. "Fruit into baskets" is exactly this with K = 2 (two basket types).

Renders on the array view: the live window is highlighted, the best window so far
glows green (shared window renderer).
"""

MAX_LEN = 20


def trace(text: str, k: int):
    s = list(text)
    steps: list = []
    n = len(s)
    counts = {"best": 0, "distinct": 0, "k": k}
    freq: dict = {}
    left = 0
    best_l, best_r = 0, -1

    def add(note, right):
        counts["distinct"] = len(freq)
        counts["best"] = (best_r - best_l + 1) if best_r >= best_l else 0
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(s),
                "window": [left, right] if right >= left else None,
                "best_window": [best_l, best_r] if best_r >= best_l else None,
                "placed": right,
                "counts": dict(counts),
            },
            "highlight": {"index": right},
            "note": note,
        })

    if not n:
        steps.append({"i": 0, "line": 0,
                      "structures": {"array": [], "counts": dict(counts)},
                      "highlight": {"index": None}, "note": "Empty input."})
        return _result(s, steps, 0)

    for right in range(n):
        c = s[right]
        freq[c] = freq.get(c, 0) + 1
        add(f"Extend to include '{c}'. Distinct in window: {len(freq)}.", right)
        while len(freq) > k:
            lc = s[left]
            freq[lc] -= 1
            if freq[lc] == 0:
                del freq[lc]
            left += 1
            add(f"More than {k} distinct — drop '{lc}' from the left (now at "
                f"{left}).", right)
        if right - left + 1 > best_r - best_l + 1:
            best_l, best_r = left, right
            add(f"Window [{left}..{right}] has ≤{k} distinct and is the longest "
                f"yet ({right - left + 1}).", right)

    add(f"Longest window with ≤{k} distinct characters: {best_r - best_l + 1} "
        f"(\"{''.join(s[best_l:best_r + 1])}\").", best_r)
    return _result(s, steps, best_r - best_l + 1)


def _result(s, steps, best):
    return {
        "meta": {"algorithm": "longest_k_distinct", "view": "array",
                 "language": "python", "length": best},
        "array": list(s),
        "steps": steps,
    }
