import heapq

from app.tracers.common import Graph, adjacency


def _fmt(dist):
    return {k: (None if v == float("inf") else v) for k, v in dist.items()}


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    dist = {n.id: float("inf") for n in graph.nodes}
    dist[start] = 0.0
    visited: set = set()
    steps = []
    pq = [(0.0, start)]
    i = 0
    # Cumulative operation counts — snapshotted into every step so the
    # frontend can show live cost as the algorithm runs.
    counts = {"visits": 0, "edge_checks": 0, "relaxations": 0, "heap_pushes": 1}

    steps.append({
        "i": i,
        "line": 1,
        "structures": {"dist": _fmt(dist), "visited": [], "counts": dict(counts)},
        "highlight": {"node": start, "edge": None},
        "note": f"Start at {start} with distance 0.",
    })

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        counts["visits"] += 1
        i += 1
        steps.append({
            "i": i,
            "line": 4,
            "structures": {"dist": _fmt(dist), "visited": sorted(visited), "counts": dict(counts)},
            "highlight": {"node": u, "edge": None},
            "note": f"Visit {u} (distance {d:g}).",
        })
        for v, w in sorted(adj.get(u, [])):
            if v in visited:
                continue
            counts["edge_checks"] += 1
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                counts["relaxations"] += 1
                counts["heap_pushes"] += 1
                i += 1
                steps.append({
                    "i": i,
                    "line": 7,
                    "structures": {"dist": _fmt(dist), "visited": sorted(visited), "counts": dict(counts)},
                    "highlight": {"node": v, "edge": [u, v]},
                    "note": f"Relax edge {u} to {v}: distance now {nd:g}.",
                })

    # Closing step — captures the final counts (edge checks after the last
    # visit step would otherwise never be snapshotted).
    steps.append({
        "i": i + 1,
        "line": 9,
        "structures": {"dist": _fmt(dist), "visited": sorted(visited), "counts": dict(counts)},
        "highlight": {"node": None, "edge": None},
        "note": "Priority queue empty — all reachable nodes finalized.",
    })

    return {
        "meta": {"algorithm": "dijkstra", "view": "graph", "language": "python", "start": start},
        "graph": graph.model_dump(),
        "steps": steps,
    }
