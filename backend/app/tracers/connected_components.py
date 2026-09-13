"""Connected components of an undirected graph.

The graph is read undirected (the shared `adjacency` helper symmetrises every
edge), which is exactly right here: two nodes belong to the same component
when *some* path joins them, regardless of direction. We flood each
unvisited node with BFS, stamping it with a component number, then move to
the next untouched node and start a new component.

Reuses the `graph` view: `structures.visited` lights up every node reached so
far, and the note carries which component we are building. No new renderer.
"""

from collections import deque

from app.tracers.common import Graph, adjacency


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    # Deterministic sweep order, but honour the user's chosen start node by
    # flooding its component first — the trace then follows their intent.
    order = sorted(n.id for n in graph.nodes)
    if start in order:
        order.remove(start)
        order.insert(0, start)

    visited: set = set()
    component: dict[str, int] = {}
    components: list[list[str]] = []
    steps: list = []
    counts = {"components": 0, "nodes_seen": 0, "edge_checks": 0}

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "visited": sorted(visited),
                "component": dict(component),
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    add("Two nodes share a component when any path connects them. We sweep "
        "the nodes; each time we hit one we have not seen, it opens a brand "
        "new component that we flood outward from.")

    for src in order:
        if src in visited:
            continue
        cid = len(components)
        components.append([])
        counts["components"] += 1
        q = deque([src])
        visited.add(src)
        component[src] = cid
        components[cid].append(src)
        counts["nodes_seen"] += 1
        add(f"'{src}' was not in any component yet — start component "
            f"#{cid + 1} and flood from here.", node=src)

        while q:
            u = q.popleft()
            for v, _w in sorted(adj.get(u, [])):
                counts["edge_checks"] += 1
                if v in visited:
                    continue
                visited.add(v)
                component[v] = cid
                components[cid].append(v)
                counts["nodes_seen"] += 1
                q.append(v)
                add(f"Reach '{v}' from '{u}' — it joins component "
                    f"#{cid + 1}.", node=v, edge=[u, v])

    n = len(components)
    sizes = ", ".join(str(len(c)) for c in components) if components else "—"
    add(f"The sweep is done: {n} component(s) (sizes {sizes}). A single "
        f"component means the whole graph is connected; more than one means "
        f"there are islands no edge bridges.")

    return {
        "meta": {
            "algorithm": "connected_components",
            "view": "graph",
            "language": "python",
            "component_count": n,
            "components": [sorted(c) for c in components],
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
