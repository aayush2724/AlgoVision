from collections import deque

from app.tracers.common import Graph, adjacency


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    visited = {start}
    steps = []
    q = deque([start])
    i = 0

    steps.append({
        "i": i,
        "line": 1,
        "structures": {"queue": [start], "visited": [start]},
        "highlight": {"node": start, "edge": None},
        "note": f"Enqueue start node {start}.",
    })

    while q:
        u = q.popleft()
        i += 1
        steps.append({
            "i": i,
            "line": 3,
            "structures": {"queue": list(q), "visited": sorted(visited)},
            "highlight": {"node": u, "edge": None},
            "note": f"Dequeue {u}.",
        })
        for v, _w in sorted(adj.get(u, [])):
            if v not in visited:
                visited.add(v)
                q.append(v)
                i += 1
                steps.append({
                    "i": i,
                    "line": 6,
                    "structures": {"queue": list(q), "visited": sorted(visited)},
                    "highlight": {"node": v, "edge": [u, v]},
                    "note": f"Discover {v} from {u}.",
                })

    return {
        "meta": {"algorithm": "bfs", "view": "graph", "language": "python", "start": start},
        "graph": graph.model_dump(),
        "steps": steps,
    }
