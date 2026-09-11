import heapq

from app.tracers.common import Graph, adjacency


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    all_nodes = [n.id for n in graph.nodes]
    in_tree: set = {start}
    mst_edges: list = []
    total = 0.0
    steps = []
    counts = {"edge_checks": 0, "additions": 0, "rejections": 0}

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "visited": sorted(in_tree),
                "mst_edges": [list(e) for e in mst_edges],
                "total_weight": total,
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    add(
        f"Build the cheapest network connecting every node. Start at {start} — "
        f"the tree grows one cheapest reachable edge at a time.",
        node=start,
    )

    # Frontier of candidate edges leaving the tree
    pq = []
    for v, w in sorted(adj.get(start, [])):
        heapq.heappush(pq, (w, start, v))

    while pq and len(in_tree) < len(all_nodes):
        w, u, v = heapq.heappop(pq)
        counts["edge_checks"] += 1
        if v in in_tree:
            counts["rejections"] += 1
            add(
                f"Cheapest frontier edge {u}–{v} ({_fmt(w)}) leads back into the "
                f"tree — taking it would make a cycle. Skip.",
                node=v, edge=[u, v],
            )
            continue
        in_tree.add(v)
        mst_edges.append([u, v])
        total += w
        counts["additions"] += 1
        add(
            f"Add edge {u}–{v} ({_fmt(w)}) — the cheapest way to reach a new "
            f"node. Tree now spans {len(in_tree)} of {len(all_nodes)}.",
            node=v, edge=[u, v],
        )
        for nxt, nw in sorted(adj.get(v, [])):
            if nxt not in in_tree:
                heapq.heappush(pq, (nw, v, nxt))

    unreached = [n for n in all_nodes if n not in in_tree]
    if unreached:
        add(
            f"Frontier exhausted — {len(unreached)} node(s) unreachable from "
            f"{start}: {', '.join(unreached)}. A spanning tree needs a "
            f"connected graph."
        )
    else:
        add(
            f"Every node connected with {len(mst_edges)} edges (always n−1) at "
            f"total cost {_fmt(total)} — the minimum possible."
        )

    return {
        "meta": {
            "algorithm": "prims_mst",
            "view": "graph",
            "language": "python",
            "start": start,
            "total_weight": total,
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
