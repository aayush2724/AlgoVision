"""Largest Rectangle in a Histogram — the monotonic stack's hardest classic.

Every bar could be the *height* of the best rectangle; the question is how
far it can stretch. It stretches left until the first shorter bar and right
until the next shorter bar. An increasing stack of indices answers both at
once: a bar is popped exactly when a shorter bar arrives (its right limit),
and the bar beneath it on the stack is its left limit. A sentinel height 0 at
the end flushes whatever is left. Each bar is pushed and popped once: O(n).

Reuses the `array` view: the arriving bar is `placed`, the rectangle being
measured is the orange `merging` span, and the best one so far is green via
`sorted_ranges`. No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(heights: list):
    arr = list(heights)
    n = len(arr)
    steps: list = []
    counts = {"pushes": 0, "pops": 0, "areas": 0}
    stack: list[int] = []
    best = {"area": 0, "range": None}

    def add(note, placed=None, merging=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "merging": list(merging) if merging else None,
                "sorted_ranges": [list(best["range"])] if best["range"] else [],
                "stack": stack[:],
                "stack_values": [arr[s] for s in stack],
                "best": best["area"],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("No bars — the largest rectangle has area 0.")
        return _result(arr, steps, 0, None)

    add("Each bar can be the height of a rectangle that stretches left and "
        "right until a shorter bar. Keep a stack of bars in increasing height; "
        "a shorter arrival tells a waiting bar exactly where it must stop.")

    for i in range(n + 1):
        cur = arr[i] if i < n else 0
        who = f"Bar {i} ({_fmt(cur)})" if i < n else "The end (a height-0 sentinel)"
        while stack and arr[stack[-1]] >= cur:
            top = stack.pop()
            counts["pops"] += 1
            counts["areas"] += 1
            h = arr[top]
            left = stack[-1] + 1 if stack else 0
            width = i - left
            area = h * width
            limit = (f"bar {stack[-1]} is shorter on the left" if stack
                     else "nothing shorter on the left, so it reaches the start")
            improved = area > best["area"]
            if improved:
                best["area"] = area
                best["range"] = (left, i - 1)
            add(f"{who} is not taller than bar {top} ({_fmt(h)}) — pop it. It "
                f"spans indices {left}..{i - 1} ({limit}): {_fmt(h)} × {width} "
                f"= {_fmt(area)}."
                + (" New best!" if improved
                   else f" Best stays {_fmt(best['area'])}."),
                placed=i if i < n else None, merging=(left, i - 1))
        if i < n:
            stack.append(i)
            counts["pushes"] += 1
            add(f"Push bar {i} ({_fmt(cur)}). Stack heights, increasing: "
                f"{[_fmt(arr[s]) for s in stack]}.", placed=i)

    if best["range"] is None:
        add("Every bar has height 0 — the largest rectangle has area 0.")
        return _result(arr, steps, 0, None)
    lo, hi = best["range"]
    add(f"Largest rectangle: area {_fmt(best['area'])}, over indices {lo}..{hi}. "
        f"Every bar was pushed once and popped once — O(n), versus O(n²) for "
        f"expanding around each bar.")
    return _result(arr, steps, best["area"], best["range"])


def _result(arr, steps, area, rng):
    return {
        "meta": {
            "algorithm": "largest_rectangle",
            "view": "array",
            "language": "python",
            "result": area,
            "range": list(rng) if rng else None,
        },
        "array": arr,
        "steps": steps,
    }
