"""Longest substring without repeating characters — the variable-size window.

Unlike a fixed window, both ends move. Extend the right edge one character at a
time; the moment a character repeats inside the window, slide the left edge just
past its previous occurrence so the window is valid again. Every character enters
and leaves at most once, so it is O(n). The best window seen is the answer.

Renders on the array view: the live window is highlighted, the best window so far
glows green (via the shared window renderer).
"""

MAX_LEN = 20


def trace(text: str):
    s = list(text)
    steps: list = []
    n = len(s)
    counts = {"best": 0, "window": 0}
    last = {}          # char -> last index seen
    left = 0
    best_l, best_r = 0, -1

    def add(note, right):
        win = right - left + 1
        counts["window"] = max(win, 0)
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
                      "highlight": {"index": None}, "note": "Empty string."})
        return _result(s, steps, 0)

    for right in range(n):
        c = s[right]
        if c in last and last[c] >= left:
            new_left = last[c] + 1
            add(f"'{c}' already sits in the window — jump the left edge to "
                f"{new_left}, just past the earlier '{c}'.", right)
            left = new_left
        last[c] = right
        if right - left + 1 > best_r - best_l + 1:
            best_l, best_r = left, right
            add(f"Window [{left}..{right}] is all unique and the longest yet "
                f"({right - left + 1}).", right)
        else:
            add(f"Extend to include '{c}'. Window [{left}..{right}].", right)

    add(f"Longest run of unique characters: {best_r - best_l + 1} "
        f"(\"{''.join(s[best_l:best_r + 1])}\").", best_r)
    return _result(s, steps, best_r - best_l + 1)


def _result(s, steps, best):
    return {
        "meta": {"algorithm": "longest_substring_no_repeat", "view": "array",
                 "language": "python", "length": best},
        "array": list(s),
        "steps": steps,
    }
