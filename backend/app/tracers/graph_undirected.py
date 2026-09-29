"""Undirected-graph structure problems (Step 15) on the drawn graph.

* cycle_undirected_bfs / cycle_undirected_dfs — explore every component;
  reaching an already-visited neighbour that is *not* the node we came from
  closes a cycle.
* bridges — Tarjan: each node gets a discovery time and a low-link (the
  earliest time reachable using one back edge). Edge u–v is a bridge when
  low[v] > tin[u]: v's subtree cannot get back above u without it.
* articulation_points — same times; u is a cut vertex when some child v has
  low[v] ≥ tin[u] (the root: when it has two or more DFS children).
* connect_network_ops — each extra (redundant) cable can reconnect one
  component; the answer is components − 1 if there are at least n − 1 cables.
* print_shortest_path — Dijkstra from the start, remembering each node's
  parent; walk the parents back from the LAST node (the sheet's "1 to n") to
  print the path, drawn green.

Reuses the `graph` view: visited nodes, the active node/edge, green edges
(`mst_edges`) for bridges / spare cables, and `dist` labels for low-links.
"""

from collections import deque

from app.tracers.common import Graph, adjacency

TITLES = {
    "cycle_undirected_bfs": "Cycle Detection in an Undirected Graph (BFS)",
    "cycle_undirected_dfs": "Cycle Detection in an Undirected Graph (DFS)",
    "bridges": "Bridges in a Graph (Tarjan)",
    "articulation_points": "Articulation Points",
    "connect_network_ops": "Operations to Make a Network Connected",
    "print_shortest_path": "Print the Shortest Path (Dijkstra + Parents)",
}


class _Steps:
    def __init__(self):
        self.steps: list = []
        self.counts: dict = {}

    def add(self, note, visited=(), node=None, edge=None, green=(), dist=None):
        st = {"visited": sorted(visited), "counts": dict(self.counts),
              "mst_edges": [list(e) for e in green]}
        if dist is not None:
            st["dist"] = dict(dist)
        self.steps.append({"i": len(self.steps), "line": 0, "structures": st,
                           "highlight": {"node": node,
                                         "edge": list(edge) if edge else None},
                           "note": note})


def _neighbours(graph):
    adj = adjacency(graph)
    return {u: sorted({v for v, _ in vs}) for u, vs in adj.items()}


def _order(ids, start):
    order = sorted(ids)
    if start in order:
        order.remove(start)
        order.insert(0, start)
    return order


def _meta(algo, res, **extra):
    return {"algorithm": algo, "view": "graph", "language": "python",
            "result": res, **extra}


def _cycle(graph: Graph, start: str, algo: str):
    nb = _neighbours(graph)
    S = _Steps()
    S.counts = {"visits": 0}
    seen: set = set()
    bfs = algo == "cycle_undirected_bfs"
    S.add(f"Explore every component by {'BFS' if bfs else 'DFS'}, remembering "
          f"which node we arrived from. An already-seen neighbour that isn't our "
          f"parent means a second route exists — a cycle.")
    found = None
    for src in _order(nb, start):
        if src in seen or found:
            continue
        seen.add(src)
        S.add(f"New component — start at {src}.", seen, src)
        if bfs:
            q = deque([(src, None)])
            while q and not found:
                u, parent = q.popleft()
                S.counts["visits"] += 1
                for v in nb[u]:
                    if v == parent:
                        continue
                    if v in seen:
                        found = (u, v)
                        S.add(f"{u} sees {v}, already visited and not its parent "
                              f"— a cycle!", seen, u, (u, v), [(u, v)])
                        break
                    seen.add(v)
                    q.append((v, u))
                    S.add(f"{u} → {v}: new, enqueue it (parent {u}).", seen, v, (u, v))
        else:
            def dfs(u, parent):
                nonlocal found
                S.counts["visits"] += 1
                for v in nb[u]:
                    if found:
                        return
                    if v == parent:
                        continue
                    if v in seen:
                        found = (u, v)
                        S.add(f"{u} sees {v}, already visited and not the parent "
                              f"— a cycle!", seen, u, (u, v), [(u, v)])
                        return
                    seen.add(v)
                    S.add(f"Go deeper: {u} → {v}.", seen, v, (u, v))
                    dfs(v, u)
            dfs(src, None)
    if found:
        S.add(f"Cycle found through the edge {found[0]}–{found[1]}.", seen,
              None, None, [found])
    else:
        S.add("Every component explored without meeting a visited non-parent — "
              "the graph is a forest, no cycle.", seen)
    return {"meta": _meta(algo, bool(found)), "steps": S.steps}


def _tarjan(graph: Graph, start: str, algo: str):
    nb = _neighbours(graph)
    S = _Steps()
    S.counts = {"visits": 0}
    tin, low = {}, {}
    timer = [0]
    bridges, cut = [], set()
    want_bridges = algo == "bridges"
    S.add("DFS stamps each node with a discovery time; its low-link is the "
          "earliest time it can reach using one back edge. The low-links "
          "(shown on nodes) decide " + ("which edges are bridges."
                                        if want_bridges else "which nodes are cut vertices."))

    def dfs(u, parent):
        tin[u] = low[u] = timer[0]
        timer[0] += 1
        S.counts["visits"] += 1
        children = 0
        S.add(f"Discover {u} at time {tin[u]}.", tin, u, green=bridges, dist=low)
        for v in nb[u]:
            if v == parent:
                continue
            if v in tin:
                if tin[v] < low[u]:
                    low[u] = tin[v]
                    S.add(f"Back edge {u}–{v}: {u} can reach time {tin[v]}; "
                          f"low[{u}] = {low[u]}.", tin, u, (u, v), bridges, low)
                continue
            children += 1
            dfs(v, u)
            low[u] = min(low[u], low[v])
            if want_bridges and low[v] > tin[u]:
                bridges.append((u, v))
                S.add(f"Back at {u}: low[{v}] = {low[v]} > tin[{u}] = {tin[u]} — "
                      f"nothing below {v} reaches above {u}. {u}–{v} is a bridge.",
                      tin, u, (u, v), bridges, low)
            elif not want_bridges and parent is not None and low[v] >= tin[u]:
                cut.add(u)
                S.add(f"Back at {u}: low[{v}] = {low[v]} ≥ tin[{u}] = {tin[u]} — "
                      f"removing {u} cuts {v}'s subtree off. {u} is a cut vertex.",
                      tin, u, (u, v), dist=low)
            else:
                S.add(f"Back at {u}: low[{v}] = {low[v]}, so low[{u}] = {low[u]}.",
                      tin, u, (u, v), bridges, low)
        if not want_bridges and parent is None and children > 1:
            cut.add(u)
            S.add(f"{u} is the DFS root with {children} separate children — "
                  f"removing it splits them, so it is a cut vertex.", tin, u, dist=low)

    for src in _order(nb, start):
        if src not in tin:
            dfs(src, None)
    if want_bridges:
        res = sorted(tuple(sorted(e)) for e in bridges)
        S.add(f"Bridges (green): {', '.join(f'{a}–{b}' for a, b in res) or 'none'}.",
              tin, green=bridges, dist=low)
        res = [list(e) for e in res]
    else:
        res = sorted(cut)
        S.add(f"Articulation points (highlighted): {', '.join(res) or 'none'}.",
              res, dist=low)
    return {"meta": _meta(algo, res), "steps": S.steps}


def _network(graph: Graph, start: str, algo: str):
    nodes = sorted(n.id for n in graph.nodes)
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    S = _Steps()
    S.counts = {"cables": len(graph.edges), "spare": 0}
    spare = []
    S.add(f"{len(nodes)} computers, {len(graph.edges)} cables. Union the ends "
          f"of each cable; a cable whose ends are already connected is spare "
          f"and can be moved.")
    for e in graph.edges:
        a, b = str(e[0]), str(e[1])
        ra, rb = find(a), find(b)
        if ra == rb:
            spare.append((a, b))
            S.counts["spare"] += 1
            S.add(f"Cable {a}–{b}: already connected — a spare cable.",
                  node=a, edge=(a, b), green=spare)
        else:
            parent[ra] = rb
            S.add(f"Cable {a}–{b}: joins two groups.", node=a, edge=(a, b),
                  green=spare)
    comps = len({find(n) for n in nodes})
    if len(graph.edges) < len(nodes) - 1:
        res = -1
        msg = (f"Only {len(graph.edges)} cables for {len(nodes)} computers — "
               f"at least {len(nodes) - 1} are needed. Impossible (−1).")
    else:
        res = comps - 1
        msg = (f"{comps} group(s): {comps - 1} move(s) connect them, and there "
               f"are {len(spare)} spare cable(s) to use.")
    S.add(msg, green=spare)
    return {"meta": _meta(algo, res, components=comps), "steps": S.steps}


def _print_path(graph, start, algo):
    import heapq
    adj = adjacency(graph)
    ids = [n.id for n in graph.nodes]
    goal = ids[-1] if ids[-1] != start else ids[0]
    S = _Steps()
    S.counts = {"relaxations": 0, "visits": 0}
    dist = {u: float("inf") for u in ids}
    parent = {u: None for u in ids}
    dist[start] = 0
    fmt = lambda: {u: (None if d == float("inf") else d) for u, d in dist.items()}
    S.add(f"Dijkstra from {start}, but every relaxation also records parent[v] = u. "
          f"Destination: {goal} (the last node).", node=start, dist=fmt())
    pq, done = [(0, start)], set()
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        S.counts["visits"] += 1
        S.add(f"Visit {u} (distance {d:g}).", visited=done, node=u, dist=fmt())
        for v, w in sorted(adj.get(u, [])):
            if v in done:
                continue
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
                S.counts["relaxations"] += 1
                S.add(f"Relax {u}→{v}: dist {d + w:g}, parent[{v}] = {u}.",
                      visited=done, node=v, edge=(u, v), dist=fmt())
    if dist[goal] == float("inf"):
        S.add(f"{goal} was never reached — no path.", visited=done, dist=fmt())
        return {"meta": _meta(algo, []), "steps": S.steps}
    path, u = [], goal
    while u is not None:
        path.append(u)
        u = parent[u]
    path.reverse()
    green = []
    for i in range(len(path) - 1, 0, -1):
        green.append((path[i - 1], path[i]))
        S.add(f"Walk back: parent[{path[i]}] = {path[i - 1]}.", visited=done,
              node=path[i - 1], edge=(path[i - 1], path[i]), green=green, dist=fmt())
    S.add(f"Path {' → '.join(path)}, total {dist[goal]:g}.", visited=done,
          node=goal, green=green, dist=fmt())
    return {"meta": _meta(algo, path), "steps": S.steps}


def trace_for(algo):
    fn = {"cycle_undirected_bfs": _cycle, "cycle_undirected_dfs": _cycle,
          "bridges": _tarjan, "articulation_points": _tarjan,
          "connect_network_ops": _network, "print_shortest_path": _print_path}[algo]
    return lambda graph, start: fn(graph, start, algo)
