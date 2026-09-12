"""Segment tree — build it, then answer a range-sum query in O(log n).

The build is the easy part; the query is the lesson. Instead of walking the
range element by element, the query lands on a handful of nodes that already
summarise whole blocks, and stops there.
"""

MAX_ARRAY_LEN = 8


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], lo: int, hi: int):
    values = list(array)
    n = len(values)
    steps: list = []
    counts = {"nodes_built": 0, "nodes_visited": 0, "full_covers": 0,
              "elements_scanned_naively": max(hi - lo + 1, 0)}

    # Each node covers [start, end]; children are 2i+1 / 2i+2 in a flat list.
    nodes: dict[int, dict] = {}

    def snapshot():
        """Lay the tree out for the tree renderer."""
        if not nodes:
            return []
        by_depth: dict[int, list[int]] = {}
        for idx in sorted(nodes):
            by_depth.setdefault(nodes[idx]["depth"], []).append(idx)
        out = []
        for idx in sorted(nodes):
            nd = nodes[idx]
            row = by_depth[nd["depth"]]
            pos = row.index(idx)
            out.append({
                "id": idx,
                "value": _fmt(nd["sum"]),
                "depth": nd["depth"],
                "x": (pos + 0.5) / len(row),
                "left": 2 * idx + 1 if (2 * idx + 1) in nodes else None,
                "right": 2 * idx + 2 if (2 * idx + 2) in nodes else None,
                "range": [nd["start"], nd["end"]],
            })
        return out

    def add(note, current=None, found=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": snapshot(),
                "current": current,
                "found": found,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    def build(idx, start, end, depth):
        counts["nodes_built"] += 1
        if start == end:
            nodes[idx] = {"start": start, "end": end, "sum": values[start],
                          "depth": depth}
            add(f"Leaf for index {start} holds {_fmt(values[start])}.",
                current=idx)
            return values[start]
        mid = (start + end) // 2
        left = build(2 * idx + 1, start, mid, depth + 1)
        right = build(2 * idx + 2, mid + 1, end, depth + 1)
        nodes[idx] = {"start": start, "end": end, "sum": left + right,
                      "depth": depth}
        add(f"Node covering [{start}..{end}] stores {_fmt(left)} + "
            f"{_fmt(right)} = {_fmt(left + right)} — one number summarising "
            f"{end - start + 1} elements.", current=idx)
        return left + right

    if n == 0:
        add("An empty array has no segment tree.")
        return _result(values, steps, lo, hi, 0)

    add(f"Build a segment tree over {', '.join(_fmt(v) for v in values)}. "
        f"Every node stores the sum of a block, so a query can reuse whole "
        f"blocks instead of adding elements one at a time.")
    build(0, 0, n - 1, 0)
    add(f"Tree built with {counts['nodes_built']} nodes. The root covers "
        f"everything: {_fmt(nodes[0]['sum'])}.", current=0)

    add(f"Now query the sum of [{lo}..{hi}]. Walk down from the root and stop "
        f"as soon as a node lies entirely inside the range.", current=0)

    def query(idx, start, end):
        counts["nodes_visited"] += 1
        if hi < start or end < lo:
            add(f"[{start}..{end}] is completely outside [{lo}..{hi}] — "
                f"contribute 0 and stop descending.", current=idx)
            return 0
        if lo <= start and end <= hi:
            counts["full_covers"] += 1
            add(f"[{start}..{end}] sits entirely inside the query — take its "
                f"stored sum {_fmt(nodes[idx]['sum'])} and stop. This is the "
                f"whole point: {end - start + 1} elements in one read.",
                current=idx, found=True)
            return nodes[idx]["sum"]
        mid = (start + end) // 2
        add(f"[{start}..{end}] only partly overlaps — split and ask both "
            f"children.", current=idx)
        return query(2 * idx + 1, start, mid) + query(2 * idx + 2, mid + 1, end)

    total = query(0, 0, n - 1)
    add(f"Sum of [{lo}..{hi}] = {_fmt(total)}, found by visiting "
        f"{counts['nodes_visited']} nodes ({counts['full_covers']} of them "
        f"reused whole blocks). Adding the elements directly would have "
        f"touched {counts['elements_scanned_naively']} — and the gap grows "
        f"as the array does.", found=True)
    return _result(values, steps, lo, hi, total)


def _result(values, steps, lo, hi, total):
    return {
        "meta": {
            "algorithm": "segment_tree",
            "view": "tree",
            "language": "python",
            "range": [lo, hi],
            "result": total,
        },
        "array": values,
        "steps": steps,
    }
