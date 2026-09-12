"""Max-heap extract — sift-down, and why heap sort falls out of it for free.

`heap_insert` shows values bubbling *up*. Extract is the mirror image and the
half that does the real work: the max is always at the root, but removing it
leaves a hole, so the last leaf moves into the root and sinks back down until
the heap property holds again.

Extract repeatedly and the values come out in descending order — that is heap
sort. Running it to completion here makes that obvious rather than asserted.
"""

from app.tracers.heap_insert import MAX_TREE_LEN, serialize  # noqa: F401


def _fmt(v: float) -> str:
    return f"{v:g}"


def _heapify(values):
    """Floyd's build-heap: sift down from the last parent backwards."""
    heap = list(values)
    n = len(heap)
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and heap[left] > heap[largest]:
                largest = left
            if right < n and heap[right] > heap[largest]:
                largest = right
            if largest == i:
                break
            heap[i], heap[largest] = heap[largest], heap[i]
            i = largest
    return heap


def trace(array: list[float]):
    values = list(array)
    steps: list = []
    counts = {"extractions": 0, "comparisons": 0, "swaps": 0}
    heap = _heapify(values)
    removed: list = []

    def add(note, current=None, comparing=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": serialize(heap),
                "current": current,
                "comparing": list(comparing) if comparing else None,
                "removed": list(removed),
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    if not values:
        add("No values — an empty heap, nothing to extract.")
        return _result(removed, steps)

    add(f"Start from a max-heap of {len(heap)} values: every parent is >= both "
        f"its children, so the largest value has nowhere to hide — it must be "
        f"at the root. Reading the max is O(1). Removing it is the interesting "
        f"part.", current=0)

    while heap:
        top = heap[0]
        counts["extractions"] += 1

        if len(heap) == 1:
            removed.append(top)
            heap.pop()
            add(f"{_fmt(top)} is the last value left — take it and the heap is "
                f"empty.")
            break

        last = heap[-1]
        add(f"Take {_fmt(top)} from the root — that is the maximum. But now the "
            f"root is a hole, and a heap has to stay a complete tree, so the "
            f"last leaf ({_fmt(last)}) moves up into it.", current=0)

        removed.append(top)
        heap[0] = heap.pop()
        counts["swaps"] += 1
        add(f"{_fmt(heap[0])} sits at the root now, almost certainly too small "
            f"to belong there. Sift it down: compare with its children and swap "
            f"with the larger one until both children are smaller.",
            current=0)

        i = 0
        n = len(heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            kids = []
            if left < n:
                kids.append(left)
                counts["comparisons"] += 1
                if heap[left] > heap[largest]:
                    largest = left
            if right < n:
                kids.append(right)
                counts["comparisons"] += 1
                if heap[right] > heap[largest]:
                    largest = right

            if not kids:
                add(f"{_fmt(heap[i])} has no children — it has reached the "
                    f"bottom and the heap property holds again.", current=i)
                break

            kid_text = " and ".join(_fmt(heap[k]) for k in kids)
            if largest == i:
                add(f"{_fmt(heap[i])} is already >= {kid_text} — it is in the "
                    f"right place, so the sift stops here.",
                    current=i, comparing=kids)
                break

            add(f"{_fmt(heap[i])} is smaller than {_fmt(heap[largest])} — swap "
                f"them so the bigger child takes the parent slot.",
                current=i, comparing=kids)
            heap[i], heap[largest] = heap[largest], heap[i]
            counts["swaps"] += 1
            i = largest

    add(f"Extracted in order: {', '.join(_fmt(v) for v in removed)}. "
        f"Each extract cost one sift-down — at most the height of the tree, so "
        f"O(log n) — and doing it {counts['extractions']} times sorted the "
        f"whole array in O(n log n). That is heap sort; it came for free.")

    return _result(removed, steps)


def _result(removed, steps):
    return {
        "meta": {
            "algorithm": "heap_extract",
            "view": "tree",
            "language": "python",
            "order": list(removed),
        },
        "steps": steps,
    }
