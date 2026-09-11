MAX_TREE_LEN = 12


def _fmt(v: float) -> str:
    return f"{v:g}"


def serialize(heap: list):
    """A heap is a complete binary tree by index: children of i are 2i+1, 2i+2.
    x comes from the slot position within the level."""
    out = []
    n = len(heap)
    for i, v in enumerate(heap):
        depth = (i + 1).bit_length() - 1
        pos = i - (2 ** depth - 1)
        width = 2 ** depth
        out.append({
            "id": i,
            "value": v,
            "left": 2 * i + 1 if 2 * i + 1 < n else None,
            "right": 2 * i + 2 if 2 * i + 2 < n else None,
            "x": (pos + 0.5) / width,
            "depth": depth,
        })
    return out


def trace(array: list[float]):
    values = list(array)
    heap: list = []
    steps = []
    counts = {"insertions": 0, "comparisons": 0, "swaps": 0}

    def add(note, current=None, inserting=None):
        steps.append({
            "i": len(steps),
            "line": 0,
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

    add(f"Build a max-heap from {len(values)} values: every parent must be "
        f">= its children. New values bubble up until that holds.")

    for v in values:
        heap.append(v)
        counts["insertions"] += 1
        i = len(heap) - 1
        add(f"Insert {_fmt(v)} at the next free slot (index {i}) — "
            f"the tree stays complete.", current=i)
        while i > 0:
            p = (i - 1) // 2
            counts["comparisons"] += 1
            if heap[i] > heap[p]:
                heap[i], heap[p] = heap[p], heap[i]
                counts["swaps"] += 1
                add(f"{_fmt(heap[p])} is bigger than its parent {_fmt(heap[i])} "
                    f"— swap up.", current=p)
                i = p
            else:
                add(f"{_fmt(heap[i])} <= parent {_fmt(heap[p])} — the heap "
                    f"property holds. Stop bubbling.", current=i)
                break

    add(f"Max-heap complete — the largest value ({_fmt(heap[0])}) sits at the "
        f"root, ready to be served first.")
    return _result(values, steps)


def _result(values, steps):
    return {
        "meta": {"algorithm": "heap_insert", "view": "tree", "language": "python"},
        "array": values,
        "steps": steps,
    }
