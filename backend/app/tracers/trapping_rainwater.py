"""Trapping Rainwater — two pointers that each trust the *shorter* wall.

Water above a bar is min(tallest wall to its left, tallest to its right) minus
the bar. The naive way scans both sides for every bar (O(n²)); prefix-max
arrays make it O(n) time but O(n) space. The two-pointer version keeps just
left_max and right_max: whichever side has the lower max is the bottleneck, so
that side's bar can be settled right now — the far wall is at least as tall.
O(n) time, O(1) space.

Reuses the `array` view: the bar being settled is `placed`, and bars already
settled from either end are green via `sorted_ranges`. No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(heights: list):
    arr = list(heights)
    n = len(arr)
    steps: list = []
    counts = {"bars_settled": 0}
    water: list = [0] * n
    state = {"left": 0, "right": n - 1, "total": 0}

    def add(note, placed=None):
        ranges = []
        if state["left"] > 0:
            ranges.append([0, state["left"] - 1])
        if state["right"] < n - 1:
            ranges.append([state["right"] + 1, n - 1])
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "sorted_ranges": ranges,
                "water": water[:],
                "total": state["total"],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("No bars, no water.")
        return _result(arr, steps, 0, water)

    add("Water over a bar = min(tallest wall on its left, tallest on its "
        "right) − its height. Two pointers start at the ends; each remembers "
        "the tallest wall it has passed.")

    left_max = right_max = 0
    while state["left"] <= state["right"]:
        l, r = state["left"], state["right"]
        if left_max <= right_max:
            i, h = l, arr[l]
            if h >= left_max:
                left_max = h
                note = (f"Left side is the bottleneck (max {_fmt(left_max)} ≤ "
                        f"{_fmt(right_max)}). Bar {i} ({_fmt(h)}) is a new "
                        f"tallest left wall — it holds no water.")
            else:
                water[i] = left_max - h
                state["total"] += water[i]
                note = (f"Left side is the bottleneck (max {_fmt(left_max)} ≤ "
                        f"{_fmt(right_max)}), so the right wall is tall enough. "
                        f"Bar {i} holds {_fmt(left_max)} − {_fmt(h)} = "
                        f"{_fmt(water[i])}. Total {_fmt(state['total'])}.")
            state["left"] += 1
        else:
            i, h = r, arr[r]
            if h >= right_max:
                right_max = h
                note = (f"Right side is the bottleneck (max {_fmt(right_max)} < "
                        f"{_fmt(left_max)}). Bar {i} ({_fmt(h)}) is a new "
                        f"tallest right wall — it holds no water.")
            else:
                water[i] = right_max - h
                state["total"] += water[i]
                note = (f"Right side is the bottleneck (max {_fmt(right_max)} < "
                        f"{_fmt(left_max)}), so the left wall is tall enough. "
                        f"Bar {i} holds {_fmt(right_max)} − {_fmt(h)} = "
                        f"{_fmt(water[i])}. Total {_fmt(state['total'])}.")
            state["right"] -= 1
        counts["bars_settled"] += 1
        add(note, placed=i)

    add(f"Trapped water: {_fmt(state['total'])} units "
        f"(per bar: {[_fmt(w) for w in water]}). One pass, two pointers, two "
        f"running maxima — O(n) time and O(1) extra space.")
    return _result(arr, steps, state["total"], water)


def _result(arr, steps, total, water):
    return {
        "meta": {
            "algorithm": "trapping_rainwater",
            "view": "array",
            "language": "python",
            "result": total,
            "water": water,
        },
        "array": arr,
        "steps": steps,
    }
