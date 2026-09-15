"""Kth largest element — a size-k min-heap that keeps only the biggest k seen.

The trick: hold a min-heap capped at k elements. The smallest of your k biggest
sits at the root, so once the heap is full any new value only matters if it beats
that root — push it and evict the root. After the whole stream, the root *is* the
kth largest. This is O(n log k), and it works on a running stream, not just a
fixed array.

Renders on the tree view (heap_insert.serialize) — the little size-k heap.
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
    heap: list = []

    def add(note, current=None):
        counts["heap_size"] = len(heap)
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "tree": serialize(heap),
                "current": current,
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    add(f"Keep a min-heap of at most k={k} values — the smallest of the biggest "
        f"k seen so far always sits at the root.")

    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, v)
            add(f"Heap not yet full — add {_fmt(v)}. Root (smallest of these) "
                f"is {_fmt(heap[0])}.", current=0)
        elif v > heap[0]:
            evicted = heapq.heapreplace(heap, v)
            counts["evictions"] += 1
            add(f"{_fmt(v)} beats the root {_fmt(evicted)} — evict the root and "
                f"push {_fmt(v)}. New root {_fmt(heap[0])}.", current=0)
        else:
            add(f"{_fmt(v)} <= root {_fmt(heap[0])} — it can't be in the top k. "
                f"Skip it.", current=0)

    ans = heap[0] if heap else None
    add((f"After the whole input the root is {_fmt(ans)} — the {k}-th largest "
         f"element.") if ans is not None else "No elements.", current=0)
    return {
        "meta": {"algorithm": "kth_largest", "view": "tree", "language": "python",
                 "kth": ans},
        "array": values,
        "steps": steps,
    }
