"""Heap sort — build a max-heap in place, then swap the max to the end and
shrink, over and over, so the array sorts itself with no extra memory.

`heap_extract` shows the same mechanic on a tree while collecting the output in
a separate list. Heap sort is the *in-place* cousin: the front of the array is
the heap, the back is the finished, sorted suffix, and the boundary marches
left one value per round. That sorted suffix growing is the whole story, so
this runs on the array view, not the tree.

Reuses the `array` view: cells are the live array (they physically move),
`placed` marks the node being sifted, and `sorted_ranges` lights the locked-in
sorted suffix green. No new renderer.
"""

MAX_ARRAY_LEN = 12


def _fmt(v):
    return f"{v:g}"


def trace(array: list):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"comparisons": 0, "swaps": 0}
    sorted_from = n  # everything at index >= sorted_from is locked in

    def add(note, placed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "placed": placed,
                "sorted_ranges": [[sorted_from, n - 1]] if sorted_from < n else [],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    def sift_down(lo, hi, phase):
        """Restore the heap rooted at lo, treating hi as the (exclusive) end."""
        i = lo
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < hi:
                counts["comparisons"] += 1
                if arr[left] > arr[largest]:
                    largest = left
            if right < hi:
                counts["comparisons"] += 1
                if arr[right] > arr[largest]:
                    largest = right
            if largest == i:
                return
            arr[i], arr[largest] = arr[largest], arr[i]
            counts["swaps"] += 1
            add(f"{phase}: {_fmt(arr[largest])} was smaller than its child "
                f"{_fmt(arr[i])} — swap so the larger value rises.", placed=largest)
            i = largest

    add(f"Heap sort has two phases. First turn the array into a max-heap (every "
        f"parent ≥ its children); then repeatedly swap the root — the maximum — "
        f"to the end and sink the new root back down.")

    if n <= 1:
        add("An array of 0 or 1 element is already sorted.")
        return _result(arr, steps)

    # Phase 1 — build the heap from the last parent backwards.
    add("Phase 1: build the max-heap, sifting down from the last parent up to "
        "the root.")
    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n, "Build")

    add(f"The array is now a max-heap — the largest value, {_fmt(arr[0])}, sits "
        f"at the front. Phase 2: extract it to the back, shrink, repeat.",
        placed=0)

    # Phase 2 — swap root to the end, shrink the heap, sift the new root.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        counts["swaps"] += 1
        sorted_from = end
        add(f"Swap the max {_fmt(arr[end])} into its final place at index "
            f"{end}. The sorted suffix now holds {n - end} value(s).",
            placed=end)
        sift_down(0, end, "Re-heap")
    sorted_from = 0
    add(f"Every value has marched into the sorted suffix: {arr}. Build is O(n), "
        f"each of the {n - 1} sift-downs is O(log n) — O(n log n) total, and "
        f"not one byte of extra memory.")
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {
            "algorithm": "heap_sort",
            "view": "array",
            "language": "python",
            "result": arr,
        },
        "array": list(arr),
        "steps": steps,
    }
