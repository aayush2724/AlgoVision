from collections import deque

from app.tracers.common import Graph, adjacency


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    visited = {start}
    steps = []
    q = deque([start])
    i = 0
    # Cumulative operation counts — snapshotted into every step.
    counts = {"enqueues": 1, "dequeues": 0, "edge_checks": 0}

    steps.append({
        "i": i,
        "line": 1,
        "structures": {"queue": [start], "visited": [start], "counts": dict(counts)},
        "highlight": {"node": start, "edge": None},
        "note": f"Enqueue start node {start}.",
    })

    while q:
        u = q.popleft()
        counts["dequeues"] += 1
        i += 1
        steps.append({
            "i": i,
            "line": 3,
            "structures": {"queue": list(q), "visited": sorted(visited), "counts": dict(counts)},
            "highlight": {"node": u, "edge": None},
            "note": f"Dequeue {u}.",
        })
        for v, _w in sorted(adj.get(u, [])):
            counts["edge_checks"] += 1
            if v not in visited:
                visited.add(v)
                q.append(v)
                counts["enqueues"] += 1
                i += 1
                steps.append({
                    "i": i,
                    "line": 6,
                    "structures": {"queue": list(q), "visited": sorted(visited), "counts": dict(counts)},
                    "highlight": {"node": v, "edge": [u, v]},
                    "note": f"Discover {v} from {u}.",
                })

    # Closing step — captures the final counts (the last node's neighbor
    # checks happen after its dequeue step was recorded).
    steps.append({
        "i": i + 1,
        "line": 7,
        "structures": {"queue": [], "visited": sorted(visited), "counts": dict(counts)},
        "highlight": {"node": None, "edge": None},
        "note": "Queue empty — traversal complete.",
    })

    return {
        "meta": {"algorithm": "bfs", "view": "graph", "language": "python", "start": start},
        "graph": graph.model_dump(),
        "steps": steps,
    }
