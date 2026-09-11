from app.tracers.common import Graph, adjacency


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    visited: set = set()
    path: list = []  # current DFS path — the recursion stack
    steps = []
    counts = {"visits": 0, "edge_checks": 0, "backtracks": 0}

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "stack": list(path),
                "visited": sorted(visited),
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    def dfs(u, parent):
        visited.add(u)
        path.append(u)
        counts["visits"] += 1
        if parent is None:
            add(f"Start at {u} — dive into the first corridor.", node=u)
        else:
            add(f"Go deeper: {parent} to {u}.", node=u, edge=[parent, u])
        for v, _w in sorted(adj.get(u, [])):
            counts["edge_checks"] += 1
            if v not in visited:
                dfs(v, u)
        path.pop()
        counts["backtracks"] += 1
        if path:
            add(f"All routes from {u} explored — backtrack to {path[-1]}.", node=path[-1])

    dfs(start, None)
    add("Stack empty — every reachable room mapped.")

    return {
        "meta": {"algorithm": "dfs", "view": "graph", "language": "python", "start": start},
        "graph": graph.model_dump(),
        "steps": steps,
    }
