"""Fenwick tree (Binary Indexed Tree) — prefix sums that survive updates.

A plain prefix-sum array answers queries in O(1) but costs O(n) to update.
A Fenwick tree gives up a little query speed for O(log n) updates, and the
mechanism is pure bit tricks: index & -index isolates the lowest set bit,
which is exactly how many elements that slot is responsible for.
"""

MAX_ARRAY_LEN = 8


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], query_upto: int):
    values = list(array)
    n = len(values)
    # tree is 1-indexed internally; tree[0] is unused padding.
    tree = [0.0] * (n + 1)
    steps: list = []
    counts = {"updates": 0, "slots_touched": 0, "query_reads": 0}

    def add(note, placed=None, marked=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                # Show the internal tree slots 1..n over the original indices
                "array": [tree[i] for i in range(1, n + 1)],
                "placed": placed,
                "sorted_ranges": [[m, m] for m in (marked or [])],
                "values": list(values),
                "tree": list(tree),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("An empty array needs no Fenwick tree.")
        return _result(values, steps, query_upto, 0)

    add(f"Build a Fenwick tree over {', '.join(_fmt(v) for v in values)}. "
        f"Slot i is responsible for the last (i & -i) elements ending at i — "
        f"that bit trick is the entire data structure.")

    for i, v in enumerate(values):
        pos = i + 1
        counts["updates"] += 1
        touched = []
        add(f"Add {_fmt(v)} from index {i} into the tree, starting at slot "
            f"{pos}.", placed=i)
        while pos <= n:
            tree[pos] += v
            counts["slots_touched"] += 1
            touched.append(pos - 1)
            step = pos & -pos
            add(f"Slot {pos} covers the last {step} element(s), so it must "
                f"include this value — it becomes {_fmt(tree[pos])}. Next "
                f"responsible slot: {pos} + {step} = {pos + step}.",
                placed=i, marked=touched)
            pos += step

    add(f"Tree built: every value folded into {counts['slots_touched']} slots "
        f"instead of rewriting a whole prefix array each time.")

    add(f"Now query the prefix sum up to index {query_upto}. Walk downward by "
        f"stripping the lowest set bit each time.", placed=query_upto)
    total = 0.0
    pos = query_upto + 1
    read = []
    while pos > 0:
        total += tree[pos]
        counts["query_reads"] += 1
        read.append(pos - 1)
        step = pos & -pos
        add(f"Add slot {pos} ({_fmt(tree[pos])}) — it covers {step} "
            f"element(s). Strip the low bit: {pos} − {step} = {pos - step}. "
            f"Running total {_fmt(total)}.", placed=query_upto, marked=read)
        pos -= step

    direct = sum(values[:query_upto + 1])
    add(f"Prefix sum up to index {query_upto} = {_fmt(total)} (direct addition "
        f"agrees: {_fmt(direct)}), read from just {counts['query_reads']} "
        f"slots. Both the query and an update are O(log n) — that balance is "
        f"why a Fenwick tree beats a plain prefix array when values change.",
        placed=query_upto, marked=read)
    return _result(values, steps, query_upto, total)


def _result(values, steps, query_upto, total):
    return {
        "meta": {
            "algorithm": "fenwick_tree",
            "view": "array",
            "language": "python",
            "query_upto": query_upto,
            "result": total,
        },
        "array": values,
        "steps": steps,
    }
