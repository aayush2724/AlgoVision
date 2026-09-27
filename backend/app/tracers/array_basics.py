"""Array fundamentals (Step 3) — small in-place tricks worth watching.

* remove_duplicates_sorted — two pointers: `i` ends the unique prefix, `j`
  scans; a new value is copied to i+1. The first k cells end up unique.
* rotate_array_k — left-rotate by k with three reversals: reverse the first
  k, reverse the rest, reverse the whole array. O(n) time, O(1) space.
* move_zeros — `j` marks the first zero; every non-zero found after it is
  swapped down to j, so non-zeros keep their order and zeros sink to the end.
* leaders — a value is a leader if nothing to its right is bigger. Scan from
  the right, keeping the running maximum.
* longest_subarray_sum_k — non-negative values only: grow a window on the
  right, shrink it from the left while its sum is too big; record the
  longest window whose sum is exactly k.
* second_largest — one pass with two trackers, no sorting.

Reuses the `array` view: cell values change in place, `placed` is the cell
being handled, green `sorted_ranges` mark what is settled, orange `merging`
marks a segment being reversed; the sum-k window uses the existing
`window`/`best_window` sliding-window highlight.
"""

TITLES = {
    "remove_duplicates_sorted": "Remove Duplicates From Sorted Array",
    "rotate_array_k": "Left Rotate Array by K (Reversal)",
    "move_zeros": "Move Zeros to the End",
    "leaders": "Leaders in an Array",
    "longest_subarray_sum_k": "Longest Subarray With Sum K",
    "second_largest": "Second Largest Element",
}
NEEDS_TARGET = {"rotate_array_k", "longest_subarray_sum_k"}
MAX_LEN = 12


def _f(v):
    return f"{v:g}"


def validate(algo, arr, target):
    if not arr or len(arr) > MAX_LEN:
        return f"Give 1–{MAX_LEN} numbers."
    if algo in NEEDS_TARGET and (target is None or target != int(target)):
        return "This needs a whole-number K."
    if algo == "rotate_array_k" and not (0 <= target <= 100):
        return "K must be 0–100."
    if algo == "longest_subarray_sum_k":
        if any(v < 0 for v in arr):
            return "The sliding window needs non-negative values."
        if not (0 <= target <= 10_000):
            return "K must be 0–10000."
    if algo == "second_largest" and len(arr) < 2:
        return "Give at least two numbers."
    return None


def trace(algo, array, target=None):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"steps": 0}

    def add(note, placed=None, green=(), span=None, extra=None):
        st = {"array": arr[:], "placed": placed,
              "sorted_ranges": [list(r) for r in green],
              "merging": list(span) if span else None, "counts": dict(counts)}
        if extra:
            st.update(extra)
        steps.append({"i": len(steps), "line": 0, "structures": st,
                      "highlight": {"index": placed}, "note": note})

    if algo == "remove_duplicates_sorted":
        arr.sort()
        i = 0
        add("Sorted, so duplicates sit together. `i` ends the unique prefix, "
            "`j` scans ahead.", 0, [(0, 0)])
        for j in range(1, n):
            counts["steps"] += 1
            if arr[j] != arr[i]:
                i += 1
                arr[i] = arr[j]
                add(f"{_f(arr[j])} at j={j} is new — copy it to position {i}.",
                    j, [(0, i)])
            else:
                add(f"{_f(arr[j])} at j={j} repeats {_f(arr[i])} — skip it.",
                    j, [(0, i)])
        result = i + 1
        add(f"The first {result} cells are the unique values: "
            f"{[_f(v) for v in arr[:result]]}. O(n), no extra array.",
            None, [(0, i)])
    elif algo == "rotate_array_k":
        k = int(target) % n
        orig = arr[:]

        def rev(a, b, label):
            add(f"{label}: reverse positions {a}..{b}.", None, (), (a, b))
            while a < b:
                arr[a], arr[b] = arr[b], arr[a]
                counts["steps"] += 1
                add(f"Swap positions {a} and {b}.", a, (), (a, b))
                a, b = a + 1, b - 1

        add(f"Left-rotate by {int(target)} (= {k} after mod {n}). Three "
            f"reversals do it in place.")
        if k:
            rev(0, k - 1, "Step 1")
            rev(k, n - 1, "Step 2")
            rev(0, n - 1, "Step 3")
        result = arr[:]
        add(f"Rotated: {[_f(v) for v in orig]} → {[_f(v) for v in arr]}. "
            f"{counts['steps']} swaps, O(1) extra space.", None, [(0, n - 1)])
    elif algo == "move_zeros":
        j = next((i for i, v in enumerate(arr) if v == 0), None)
        if j is None:
            add("No zeros — nothing to move.", None, [(0, n - 1)])
        else:
            add(f"The first zero is at {j}. Every non-zero after it swaps down "
                f"to j, and j advances.", j, [(0, j - 1)] if j else ())
            for i in range(j + 1, n):
                counts["steps"] += 1
                if arr[i] != 0:
                    arr[i], arr[j] = arr[j], arr[i]
                    add(f"{_f(arr[j])} at {i} is non-zero — swap it down to {j}.",
                        i, [(0, j)])
                    j += 1
                else:
                    add(f"Position {i} is zero — leave it.", i,
                        [(0, j - 1)] if j else ())
            add(f"Non-zeros kept their order; the zeros sank to the end: "
                f"{[_f(v) for v in arr]}.", None, [(0, j - 1)] if j else ())
        result = arr[:]
    elif algo == "leaders":
        best = None
        found: list = []
        add("A leader has nothing bigger to its right. Scan from the right, "
            "tracking the biggest value seen.")
        for i in range(n - 1, -1, -1):
            counts["steps"] += 1
            v = arr[i]
            if best is None or v > best:
                best = v
                found.append(i)
                add(f"{_f(v)} beats everything to its right — a leader.", i,
                    [(j, j) for j in found])
            else:
                add(f"{_f(v)} is not above the running max {_f(best)} — not a "
                    f"leader.", i, [(j, j) for j in found])
        result = [arr[i] for i in sorted(found)]
        add(f"Leaders (left to right): {[_f(v) for v in result]}. One pass.",
            None, [(j, j) for j in found])
    elif algo == "longest_subarray_sum_k":
        k = target
        lo, s, best = 0, 0, None
        add(f"Find the longest run summing to exactly {_f(k)}. Values are "
            f"non-negative, so growing the window only raises the sum.",
            extra={"window": None, "best_window": None})
        for hi in range(n):
            s += arr[hi]
            counts["steps"] += 1
            while s > k and lo <= hi:
                s -= arr[lo]
                lo += 1
            if s == k and lo <= hi and (best is None or hi - lo > best[1] - best[0]):
                best = (lo, hi)
                note = (f"Window {lo}..{hi} sums to {_f(k)} — longest so far "
                        f"({hi - lo + 1}).")
            else:
                note = (f"Window {lo}..{hi} sums to {_f(s)}." if lo <= hi
                        else f"The window emptied — {_f(arr[hi])} alone is too big.")
            add(note, hi, extra={"window": [lo, hi] if lo <= hi else None,
                                 "best_window": list(best) if best else None})
        result = 0 if best is None else best[1] - best[0] + 1
        add(f"Longest subarray with sum {_f(k)}: length {result}"
            + (f" (indices {best[0]}..{best[1]})." if best else " — none exists."),
            extra={"window": None, "best_window": list(best) if best else None})
    else:
        first = second = None
        add("Track the largest and second largest in one pass — no sorting.")
        for i, v in enumerate(arr):
            counts["steps"] += 1
            if first is None or v > first:
                second, first = first, v
                note = f"{_f(v)} is a new largest; the old largest becomes second."
            elif v != first and (second is None or v > second):
                second = v
                note = f"{_f(v)} is below the largest but beats second — new second."
            else:
                note = f"{_f(v)} changes nothing."
            add(note + f" (largest {_f(first)}, second "
                f"{'—' if second is None else _f(second)})", i)
        result = second
        add(f"Second largest: "
            f"{'none (all values equal)' if second is None else _f(second)}.")
    return {"meta": {"algorithm": algo, "view": "array", "language": "python",
                     "result": result},
            "array": list(array) if algo != "remove_duplicates_sorted" else sorted(array),
            "steps": steps}
