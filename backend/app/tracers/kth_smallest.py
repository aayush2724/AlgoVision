"""Kth smallest element — a size-k max-heap that keeps only the smallest k seen.

Mirror of kth-largest: hold a max-heap capped at k. The largest of your k
smallest sits at the root, so a new value only matters if it is smaller than that
root — then evict the root. After the stream, the root is the kth smallest.
O(n log k). (Python's heapq is a min-heap, so we store negatives and flip them
back for display, which renders as a valid max-heap.)

Renders on the tree view (heap_insert.serialize).
"""

import heapq

from app.tracers.heap_insert import serialize

MAX_LEN = 14


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], k: int):
    values = list(array)
    steps = []
    counts = {"k": k, "heap_size": 0, "evictions": 0}
    heap: list = []  # min-heap of negated values == max-heap of actual values

    def display():
        return [-x for x in heap]

    def add(note, current=None):
        counts["heap_size"] = len(heap)
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "tree": serialize(display()),
                "current": current,
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    add(f"Keep a max-heap of at most k={k} values — the largest of the smallest "
        f"k seen so far always sits at the root.")

    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, -v)
            add(f"Heap not yet full — add {_fmt(v)}. Root (largest of these) is "
                f"{_fmt(-heap[0])}.", current=0)
        elif v < -heap[0]:
            evicted = -heapq.heapreplace(heap, -v)
            counts["evictions"] += 1
            add(f"{_fmt(v)} is smaller than the root {_fmt(evicted)} — evict the "
                f"root and push {_fmt(v)}. New root {_fmt(-heap[0])}.", current=0)
        else:
            add(f"{_fmt(v)} >= root {_fmt(-heap[0])} — it can't be in the "
                f"smallest k. Skip it.", current=0)

    ans = -heap[0] if heap else None
    add((f"After the whole input the root is {_fmt(ans)} — the {k}-th smallest "
         f"element.") if ans is not None else "No elements.", current=0)
    return {
        "meta": {"algorithm": "kth_smallest", "view": "tree", "language": "python",
                 "kth": ans},
        "array": values,
        "steps": steps,
    }
