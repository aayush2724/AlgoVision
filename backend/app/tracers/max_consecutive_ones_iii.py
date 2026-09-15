"""Max consecutive ones III — the "at most k zeros" variable window.

Reframe the problem: the longest run of 1s you can get by flipping up to k zeros
is just the longest window containing at most k zeros. Extend the right edge; if
the window ever holds more than k zeros, shrink from the left until it holds k
again. The widest valid window is the answer.

Renders on the array view: the live window is highlighted, the best window so far
glows green (shared window renderer).
"""

MAX_LEN = 20


def trace(bits: list[float], k: int):
    a = [int(v) for v in bits]
    steps: list = []
    n = len(a)
    counts = {"best": 0, "zeros": 0, "k": k}
    left = 0
    zeros = 0
    best_l, best_r = 0, -1

    def add(note, right):
        counts["zeros"] = zeros
        counts["best"] = (best_r - best_l + 1) if best_r >= best_l else 0
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "array": list(a),
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
        return _result(a, steps, 0)

    for right in range(n):
        if a[right] == 0:
            zeros += 1
        add(f"Extend to index {right} (value {a[right]}). Zeros in window: "
            f"{zeros}.", right)
        while zeros > k:
            if a[left] == 0:
                zeros -= 1
            left += 1
            add(f"Too many zeros (> {k}) — shrink from the left to {left}.", right)
        if right - left + 1 > best_r - best_l + 1:
            best_l, best_r = left, right
            add(f"Window [{left}..{right}] has ≤{k} zeros and is the longest yet "
                f"({right - left + 1}).", right)

    add(f"Longest run after flipping ≤{k} zeros: {best_r - best_l + 1}.", best_r)
    return _result(a, steps, best_r - best_l + 1)


def _result(a, steps, best):
    return {
        "meta": {"algorithm": "max_consecutive_ones_iii", "view": "array",
                 "language": "python", "length": best},
        "array": list(a),
        "steps": steps,
    }
