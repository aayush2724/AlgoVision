"""Kahn's algorithm — topological ordering of a directed acyclic graph.

Unlike the other graph tracers, edges here are read as *directed*: [a, b]
means a must come before b. That is the whole point of the algorithm, so the
UI labels the input as a dependency list rather than a plain graph.
"""

from collections import deque

from app.tracers.common import Graph


def _directed(graph: Graph):
    adj: dict[str, list[str]] = {n.id: [] for n in graph.nodes}
    indeg: dict[str, int] = {n.id: 0 for n in graph.nodes}
    for e in graph.edges:
        a, b = str(e[0]), str(e[1])
        adj[a].append(b)
        indeg[b] += 1
    for a in adj:
        adj[a].sort()
    return adj, indeg


def trace(graph: Graph, start: str):
    adj, indeg = _directed(graph)
    steps: list = []
    order: list[str] = []
    counts = {"emitted": 0, "edge_relaxations": 0}

    def add(note, node=None, edge=None, queue=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "queue": list(queue if queue is not None else []),
                "visited": list(order),
                "order": list(order),
                "indegree": dict(indeg),
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": edge},
            "note": note,
        })

    add("Every edge is a dependency: A → B means A must be finished before B. "
        "Kahn's rule: repeatedly take a task nobody is waiting on.")

    # Seed with every task that has no prerequisites. The chosen start node
    # goes first when it qualifies, so the trace follows the user's intent.
    ready = sorted([n for n, d in indeg.items() if d == 0])
    if start in ready:
        ready.remove(start)
        ready.insert(0, start)
    q = deque(ready)

    if not q:
        add("No task has an in-degree of 0 — every task waits on another. "
            "This graph is one big cycle, so no valid order exists.")
        return _result(graph, steps, order, cyclic=True)

    add(f"Tasks with no prerequisites: {', '.join(q)}. They can start immediately.",
        queue=q)

    while q:
        u = q.popleft()
        order.append(u)
        counts["emitted"] += 1
        add(f"'{u}' has nothing left blocking it — emit it as position "
            f"{len(order)} in the order.", node=u, queue=q)

        for v in adj[u]:
            indeg[v] -= 1
            counts["edge_relaxations"] += 1
            if indeg[v] == 0:
                q.append(v)
                add(f"'{u}' was the last thing '{v}' waited on — '{v}' is now "
                    f"ready.", node=v, edge=[u, v], queue=q)
            else:
                add(f"'{v}' still waits on {indeg[v]} more task(s).",
                    node=v, edge=[u, v], queue=q)

    if len(order) < len(indeg):
        stuck = sorted([n for n, d in indeg.items() if d > 0])
        add(f"The queue drained but {', '.join(stuck)} never reached in-degree 0 "
            f"— they depend on each other in a cycle, so no topological order "
            f"exists.")
        return _result(graph, steps, order, cyclic=True)

    add(f"All {len(order)} tasks emitted with no cycle: {' → '.join(order)}.")
    return _result(graph, steps, order, cyclic=False)


def _result(graph: Graph, steps, order, cyclic):
    return {
        "meta": {
            "algorithm": "topological_sort",
            "view": "graph",
            "language": "python",
            "directed": True,
            "order": order,
            "cyclic": cyclic,
        },
        "graph": graph.model_dump(),
        "steps": steps,
    }
