from app.tracers.common import Graph


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(graph: Graph, start: str = None):
    """Kruskal's MST. `start` is accepted for a uniform graph-tracer signature
    but unused — Kruskal's is edge-driven, not vertex-driven."""
    node_ids = [n.id for n in graph.nodes]
    parent = {nid: nid for nid in node_ids}

    def find(x):
        # Path compression, iterative so deep chains cannot blow the stack
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    def components():
        groups: dict = {}
        for nid in node_ids:
            groups.setdefault(find(nid), []).append(nid)
        return sorted((sorted(v) for v in groups.values()), key=lambda g: g[0])

    edges = []
    for e in graph.edges:
        a, b = str(e[0]), str(e[1])
        w = float(e[2]) if len(e) > 2 else 1.0
        edges.append((w, a, b))
    edges.sort()

    mst_edges: list = []
    total = 0.0
    steps = []
    counts = {"edge_checks": 0, "unions": 0, "cycles_skipped": 0}

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "visited": sorted({n for e in mst_edges for n in e}),
                "mst_edges": [list(e) for e in mst_edges],
                "components": components(),
                "total_weight": total,
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    if not edges:
        add(f"No edges — {len(node_ids)} isolated node(s), nothing to connect.")
        return _result(graph, total, steps)

    order = ", ".join(f"{a}–{b}({_fmt(w)})" for w, a, b in edges)
    add(
        f"Kruskal's works on edges, not nodes: sort every edge cheapest-first, "
        f"then take each one unless it closes a cycle. Order: {order}."
    )
    add(
        f"Every node starts in its own group — {len(node_ids)} separate "
        f"components. An edge is safe only if it joins two different groups."
    )

    for w, a, b in edges:
        counts["edge_checks"] += 1
        ra, rb = find(a), find(b)
        if ra == rb:
            counts["cycles_skipped"] += 1
            add(
                f"Edge {a}–{b} ({_fmt(w)}): {a} and {b} are already in the same "
                f"group — this edge would close a cycle. Reject it.",
                node=b, edge=[a, b],
            )
            continue
        parent[rb] = ra
        mst_edges.append([a, b])
        total += w
        counts["unions"] += 1
        add(
            f"Edge {a}–{b} ({_fmt(w)}): different groups, so it is safe — "
            f"union them. {len(mst_edges)} edge(s) in the tree, cost {_fmt(total)}.",
            node=b, edge=[a, b],
        )
        if len(mst_edges) == len(node_ids) - 1:
            break

    groups = components()
    if len(groups) > 1:
        add(
            f"Edges exhausted with {len(groups)} components left — the graph is "
            f"disconnected, so this is a spanning *forest*, not a tree. "
            f"Total cost {_fmt(total)}."
        )
    else:
        add(
            f"One group remains — every node connected with {len(mst_edges)} "
            f"edges at total cost {_fmt(total)}, the same minimum Prim's finds."
        )

    return _result(graph, total, steps)


def _result(graph, total, steps):
    return {
        "meta": {
            "algorithm": "kruskals_mst",
            "view": "graph",
            "language": "python",
            "total_weight": total,
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
