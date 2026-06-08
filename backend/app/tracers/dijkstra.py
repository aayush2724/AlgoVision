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

    steps.append({
        "i": i,
        "line": 1,
        "structures": {"dist": _fmt(dist), "visited": []},
        "highlight": {"node": start, "edge": None},
        "note": f"Start at {start} with distance 0.",
    })

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        i += 1
        steps.append({
            "i": i,
            "line": 4,
            "structures": {"dist": _fmt(dist), "visited": sorted(visited)},
            "highlight": {"node": u, "edge": None},
            "note": f"Visit {u} (distance {d:g}).",
        })
        for v, w in sorted(adj.get(u, [])):
            if v in visited:
                continue
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                i += 1
                steps.append({
                    "i": i,
                    "line": 7,
                    "structures": {"dist": _fmt(dist), "visited": sorted(visited)},
                    "highlight": {"node": v, "edge": [u, v]},
                    "note": f"Relax edge {u} to {v}: distance now {nd:g}.",
                })

    return {
        "meta": {"algorithm": "dijkstra", "view": "graph", "language": "python", "start": start},
        "graph": graph.model_dump(),
        "steps": steps,
    }
