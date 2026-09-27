"""Rotate a Linked List right by k — close it into a ring, then cut.

Rotating by k moves the last k nodes to the front. Walk once to find the length
and the tail; k larger than the length wraps, so use k mod length. Link the
tail back to the head (a ring), walk to the node length − k − 1 from the head —
the new tail — and cut the ring after it. O(n), no node moves, two arrows
change.

Reuses the `list` view: the tail→head arrow closes the ring visibly, then the
cut removes one arrow. No new renderer.
"""

MAX_LIST_LEN = 10
MAX_K = 100


def _fmt(v):
    return f"{v:g}"


def trace(array: list, k: int):
    values = list(array)
    n = len(values)
    k = int(k)
    nxt = [i + 1 if i < n - 1 else None for i in range(n)]
    steps: list = []
    counts = {"walk_steps": 0}
    ptr = {"head": 0 if n else None, "tail": None, "newTail": None}

    def add(note, curr=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "curr": curr,
                "pointers": [[p, v] for p, v in ptr.items() if v is not None],
                "counts": dict(counts),
            },
            "highlight": {"index": curr},
            "note": note,
        })

    def order():
        out, j, seen = [], ptr["head"], 0
        while j is not None and seen < n:
            out.append(values[j])
            j = nxt[j]
            seen += 1
        return out

    if n == 0:
        add("An empty list — nothing to rotate.")
        return _result(values, steps, [])

    add(f"Rotate right by {k}: the last {k} node(s) move to the front. First "
        f"walk to the tail to learn the length.", curr=0)
    tail = 0
    while nxt[tail] is not None:
        tail = nxt[tail]
        counts["walk_steps"] += 1
    ptr["tail"] = tail
    eff = k % n
    add(f"Length {n}, tail is node {tail}. Rotating by {k} is the same as by "
        f"{k} mod {n} = {eff}.", curr=tail)

    if eff == 0:
        add(f"A rotation by a multiple of {n} changes nothing — the list stays "
            f"{' → '.join(_fmt(v) for v in order())}.")
        return _result(values, steps, order())

    nxt[tail] = 0
    add(f"Close the ring: link the tail (node {tail}) back to the head.",
        curr=tail)
    new_tail = 0
    ptr["newTail"] = 0
    for _ in range(n - eff - 1):
        new_tail = nxt[new_tail]
        ptr["newTail"] = new_tail
        counts["walk_steps"] += 1
        add(f"Walk to the new tail: node {new_tail} (it must end up {n - eff} "
            f"nodes from the front).", curr=new_tail)

    new_head = nxt[new_tail]
    nxt[new_tail] = None
    ptr.update(head=new_head, tail=None)
    add(f"Cut the ring after node {new_tail}: node {new_head} is the new head.",
        curr=new_head)
    ptr["newTail"] = None
    result = order()
    add(f"Rotated: {' → '.join(_fmt(v) for v in result)}. Two arrows changed; "
        f"{counts['walk_steps']} steps walked in total.")
    return _result(values, steps, result)


def _result(values, steps, result):
    return {
        "meta": {
            "algorithm": "rotate_list",
            "view": "list",
            "language": "python",
            "result": result,
        },
        "array": values,
        "steps": steps,
    }
