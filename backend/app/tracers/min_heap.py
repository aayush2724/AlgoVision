"""Min-heap — build one by inserting values and bubbling each up.

The mirror of the max-heap: every parent must be <= its children, so the
smallest value ends up at the root. Each new value is dropped in the next free
slot (keeping the tree complete) and swapped upward until its parent is no
larger. That is a min-heap / min-priority-queue, the workhorse behind Dijkstra
and k-smallest problems.

Renders on the shared tree view via heap_insert.serialize (a heap array is a
complete binary tree by index).
"""

from app.tracers.heap_insert import serialize

MAX_TREE_LEN = 12


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    values = list(array)
    heap: list = []
    steps = []
    counts = {"insertions": 0, "comparisons": 0, "swaps": 0}

    def add(note, current=None, inserting=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "tree": serialize(heap),
                "current": current,
                "inserting": inserting,
                "found": None,
                "counts": dict(counts),
            },
            "highlight": {"node": current},
            "note": note,
        })

    if not values:
        add("No values — an empty heap.")
        return _result(values, steps)

    add(f"Build a min-heap from {len(values)} values: every parent must be "
        f"<= its children, so new values bubble up until that holds.")

    for v in values:
        heap.append(v)
        counts["insertions"] += 1
        i = len(heap) - 1
        add(f"Insert {_fmt(v)} at the next free slot (index {i}) — the tree "
            f"stays complete.", current=i)
        while i > 0:
            p = (i - 1) // 2
            counts["comparisons"] += 1
            if heap[i] < heap[p]:
                heap[i], heap[p] = heap[p], heap[i]
                counts["swaps"] += 1
                add(f"{_fmt(heap[p])} is smaller than its parent {_fmt(heap[i])} "
                    f"— swap up.", current=p)
                i = p
            else:
                add(f"{_fmt(heap[i])} >= parent {_fmt(heap[p])} — the heap "
                    f"property holds. Stop bubbling.", current=i)
                break

    add(f"Min-heap complete — the smallest value ({_fmt(heap[0])}) sits at the "
        f"root, ready to be served first.")
    return _result(values, steps)


def _result(values, steps):
    return {
        "meta": {"algorithm": "min_heap", "view": "tree", "language": "python"},
        "array": values,
        "steps": steps,
    }
