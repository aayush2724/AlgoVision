"""Bellman-Ford — single-source shortest paths that survive negative edges,
and can prove when no shortest path exists at all.

Unlike Dijkstra, this reads edges as *directed* (a -> b) and tolerates negative
weights. The idea is brute but bulletproof: relax every edge, V-1 times over.
After k rounds every shortest path using at most k edges is correct, and a
shortest path visits at most V-1 edges — so V-1 rounds settle everything. One
extra round that still finds an improvement is a certificate of a negative
cycle: a loop you could ride forever to get "shorter", so no shortest path
exists.

Reuses the `graph` view and Dijkstra's per-node distance display: `structures.
dist` drives the labels, `highlight.edge` lights the edge being relaxed. Edges
are directed here, like topological sort. No new renderer.
"""

from app.tracers.common import Graph, edge_list


def _fmt(dist):
    return {k: (None if v == float("inf") else v) for k, v in dist.items()}


def trace(graph: Graph, start: str):
    edges = edge_list(graph)
    nodes = [n.id for n in graph.nodes]
    v = len(nodes)
    dist = {n: float("inf") for n in nodes}
    dist[start] = 0.0
    steps: list = []
    counts = {"rounds": 0, "relaxations": 0, "edge_checks": 0}

    def add(note, node=None, edge=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "dist": _fmt(dist),
                "visited": sorted(n for n in nodes if dist[n] != float("inf")),
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    add(f"Bellman-Ford from {start}. Edges are directed (a → b) and may be "
        f"negative. Relax every edge, {max(v - 1, 0)} times over — after k "
        f"rounds every shortest path of at most k edges is correct.",
        node=start)

    # V-1 rounds of relaxing every edge. Stop early if a round changes nothing.
    for r in range(1, v):
        counts["rounds"] += 1
        changed = False
        add(f"Round {r}: sweep all {len(edges)} edge(s) and relax any that "
            f"offer a shorter path.")
        for a, b, w in sorted(edges):
            counts["edge_checks"] += 1
            if dist[a] != float("inf") and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                counts["relaxations"] += 1
                changed = True
                add(f"Edge {a} → {b} (weight {w:g}): {b} is now reachable in "
                    f"{dist[b]:g} via {a}.", node=b, edge=[a, b])
        if not changed:
            add(f"Round {r} changed nothing — every shortest path is already "
                f"settled, so we can stop {v - 1 - r} round(s) early.")
            break

    # One more full sweep: any relaxation now means a negative cycle exists.
    negative_cycle = False
    for a, b, w in sorted(edges):
        counts["edge_checks"] += 1
        if dist[a] != float("inf") and dist[a] + w < dist[b]:
            negative_cycle = True
            add(f"Edge {a} → {b} can STILL be relaxed after {v - 1} rounds. "
                f"That means a negative cycle is reachable — you could loop it "
                f"forever to get 'shorter', so no shortest path exists.",
                node=b, edge=[a, b])
            break

    if negative_cycle:
        add("A negative cycle makes shortest paths undefined for the nodes it "
            "can reach. Bellman-Ford is the algorithm that can say so.")
    else:
        reached = sorted(n for n in nodes if dist[n] != float("inf"))
        add(f"No negative cycle. Shortest distances from {start} are final for "
            f"{len(reached)} reachable node(s), after {counts['relaxations']} "
            f"relaxation(s). Dijkstra would have been faster but could not have "
            f"handled the negative edges.")

    return {
        "meta": {
            "algorithm": "bellman_ford",
            "view": "graph",
            "language": "python",
            "directed": True,
            "start": start,
            "dist": _fmt(dist),
            "negative_cycle": negative_cycle,
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
