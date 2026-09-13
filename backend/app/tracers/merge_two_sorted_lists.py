"""Merge two sorted linked lists into one — by re-pointing, not by copying.

Both inputs are already sorted, so the merged head is always whichever current
node is smaller. Splice it onto the tail of the result, advance that list, and
repeat; when one list runs dry, the other's remaining tail is already sorted,
so attach it whole. It is the merge step of merge sort, but on pointers, in
O(1) extra space.

Reuses the `list` view: the two input lists sit side by side as nodes, and the
`next` arrows physically rewire into one chain as the merge proceeds. Three
named `pointers` (a, b, tail) track the two inputs and the growing result.
No new renderer.
"""

MAX_EACH = 6


def _fmt(v):
    return f"{v:g}"


def trace(list_a: list, list_b: list):
    a_vals = list(list_a)
    b_vals = list(list_b)
    la, lb = len(a_vals), len(b_vals)
    values = a_vals + b_vals          # nodes 0..la-1 are A, la.. are B
    nxt: list = [None] * (la + lb)
    for i in range(la - 1):
        nxt[i] = i + 1                # A's own chain
    for i in range(la, la + lb - 1):
        nxt[i] = i + 1                # B's own chain

    steps: list = []
    counts = {"comparisons": 0, "splices": 0}
    order: list[int] = []
    head = None
    tail = None

    a = 0 if la else None
    b = la if lb else None

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "values": list(values),
                "next": list(nxt),
                "pointers": [["a", a], ["b", b], ["tail", tail]],
                "head": head,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    def adv_a():
        return a + 1 if a is not None and a < la - 1 else None

    def adv_b():
        return b + 1 if b is not None and b < la + lb - 1 else None

    def splice(node):
        nonlocal head, tail
        if tail is None:
            head = node
        else:
            nxt[tail] = node
        tail = node
        nxt[tail] = None
        order.append(node)
        counts["splices"] += 1

    add(f"Two sorted lists: [{', '.join(_fmt(v) for v in a_vals) or '∅'}] and "
        f"[{', '.join(_fmt(v) for v in b_vals) or '∅'}]. The merged head is "
        f"always the smaller of the two current nodes — splice it on and "
        f"advance that list. No values are copied; only pointers move.")

    while a is not None and b is not None:
        counts["comparisons"] += 1
        if values[a] <= values[b]:
            chosen = a
            add(f"{_fmt(values[a])} (list A) ≤ {_fmt(values[b])} (list B) — "
                f"splice A's node onto the result.", current=chosen)
            splice(chosen)
            a = adv_a()
        else:
            chosen = b
            add(f"{_fmt(values[b])} (list B) < {_fmt(values[a])} (list A) — "
                f"splice B's node onto the result.", current=chosen)
            splice(chosen)
            b = adv_b()

    # One list is exhausted; the other's remaining tail is already sorted.
    while a is not None:
        add(f"List B is done — attach A's remaining node {_fmt(values[a])}.",
            current=a)
        splice(a)
        a = adv_a()
    while b is not None:
        add(f"List A is done — attach B's remaining node {_fmt(values[b])}.",
            current=b)
        splice(b)
        b = adv_b()

    merged = [values[i] for i in order]
    add(f"Merged into one sorted chain: [{', '.join(_fmt(v) for v in merged) or '∅'}]. "
        f"{counts['comparisons']} comparison(s), every node spliced once, and "
        f"no second array allocated — O(la + lb) time, O(1) extra space.")

    return {
        "meta": {
            "algorithm": "merge_two_sorted_lists",
            "view": "list",
            "language": "python",
            "merged": merged,
            "order": order,
        },
        "array": values,
        "steps": steps,
    }
