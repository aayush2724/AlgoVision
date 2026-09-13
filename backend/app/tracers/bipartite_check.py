"""Bipartite check by 2-colouring (BFS).

A graph is bipartite when its nodes split into two groups with every edge
crossing between the groups — never inside one. We BFS from each unvisited
node, painting the start colour 0 and every neighbour the opposite colour.
The moment an edge joins two nodes that already share a colour, the two-group
split is impossible and we stop: that edge sits inside an odd-length cycle.

Undirected is correct here, and reuses the `graph` view. `structures.color`
carries each node's side (0/1) for the narration; `visited` drives the
node highlighting the renderer already understands.
"""

from collections import deque

from app.tracers.common import Graph, adjacency

SIDE = {0: "A", 1: "B"}


def trace(graph: Graph, start: str):
    adj = adjacency(graph)
    order = sorted(n.id for n in graph.nodes)
    if start in order:
        order.remove(start)
        order.insert(0, start)

    color: dict[str, int] = {}
    visited: set = set()
    steps: list = []
    counts = {"colored": 0, "edge_checks": 0, "conflicts": 0}
    conflict_edge = None

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "visited": sorted(visited),
                "color": dict(color),
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    add("Can we split every node into two groups, A and B, so that every edge "
        "runs between the groups and never inside one? Paint a start node A, "
        "its neighbours B, theirs A — a clash means no.")

    for src in order:
        if src in color:
            continue
        color[src] = 0
        visited.add(src)
        counts["colored"] += 1
        q = deque([src])
        add(f"'{src}' is unpainted — drop it in group {SIDE[0]} and spread "
            f"the colouring from here.", node=src)

        while q:
            u = q.popleft()
            for v, _w in sorted(adj.get(u, [])):
                counts["edge_checks"] += 1
                if v not in color:
                    color[v] = 1 - color[u]
                    visited.add(v)
                    counts["colored"] += 1
                    q.append(v)
                    add(f"'{v}' is next to '{u}' (group {SIDE[color[u]]}), so "
                        f"it must go in group {SIDE[color[v]]}.",
                        node=v, edge=[u, v])
                elif color[v] == color[u]:
                    counts["conflicts"] += 1
                    conflict_edge = [u, v]
                    add(f"Edge '{u}'–'{v}' joins two nodes already in group "
                        f"{SIDE[color[u]]}. That edge lives inside a group, so "
                        f"no two-group split works — the graph is NOT "
                        f"bipartite.", node=v, edge=[u, v])
                    return _result(graph, steps, color, False, conflict_edge)

    groups = {"A": sorted(k for k, c in color.items() if c == 0),
              "B": sorted(k for k, c in color.items() if c == 1)}
    add(f"Every node is painted with no clash: group A = "
        f"{', '.join(groups['A']) or '—'}, group B = "
        f"{', '.join(groups['B']) or '—'}. The graph IS bipartite.")
    return _result(graph, steps, color, True, None)


def _result(graph, steps, color, bipartite, conflict_edge):
    return {
        "meta": {
            "algorithm": "bipartite_check",
            "view": "graph",
            "language": "python",
            "bipartite": bipartite,
            "coloring": {k: SIDE[c] for k, c in color.items()},
            "conflict_edge": conflict_edge,
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
