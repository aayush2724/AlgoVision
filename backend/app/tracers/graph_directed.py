"""Directed-graph problems (Step 15) on the drawn graph — edges read a → b.

* cycle_directed — DFS keeping the current path; an edge back into the path
  (not just to any visited node) is a directed cycle.
* safe_states — a node is safe if every path from it ends at a terminal
  node. DFS with three states: on-path, safe, unsafe; any node that can
  reach a cycle is unsafe.
* kosaraju — strongly connected components: DFS to record finish order, then
  DFS on the reversed graph in decreasing finish order; each second-pass tree
  is one SCC (its number shown on the nodes).
* shortest_path_dag — topological order first (Kahn), then relax every edge
  out of each node in that order; one pass settles every distance, even with
  negative weights.

Reuses the `graph` view with `meta.directed` (arrows): visited nodes, the
active node/edge, green edges, and `dist` labels on the nodes.
"""

from collections import deque

from app.tracers.common import Graph, directed_adjacency

TITLES = {
    "cycle_directed": "Cycle Detection in a Directed Graph (DFS)",
    "safe_states": "Find Eventual Safe States",
    "kosaraju": "Strongly Connected Components (Kosaraju)",
    "shortest_path_dag": "Shortest Path in a DAG",
    "network_delay": "Network Delay Time",
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


def _meta(algo, res, **extra):
    return {"algorithm": algo, "view": "graph", "language": "python",
            "directed": True, "result": res, **extra}


def _out(graph):
    adj = directed_adjacency(graph)
    return {u: sorted({v for v, _ in vs}) for u, vs in adj.items()}


def _order(ids, start):
    order = sorted(ids)
    if start in order:
        order.remove(start)
        order.insert(0, start)
    return order


def _cycle(graph: Graph, start: str):
    out = _out(graph)
    S = _Steps()
    S.counts = {"visits": 0}
    seen, on_path = set(), []
    found = None
    S.add("Edges point one way. DFS keeps the current path; an edge back into "
          "that path is a directed cycle. (A visited node off the path is fine "
          "— that is just two routes, not a loop.)")

    def dfs(u):
        nonlocal found
        seen.add(u)
        on_path.append(u)
        S.counts["visits"] += 1
        S.add(f"Enter {u}. Path: {' → '.join(on_path)}.", seen, u)
        for v in out[u]:
            if found:
                return
            if v in on_path:
                found = (u, v)
                loop = on_path[on_path.index(v):] + [v]
                S.add(f"{u} → {v} points back into the current path — a directed "
                      f"cycle: {' → '.join(loop)}.", seen, u, (u, v), [(u, v)])
                return
            if v not in seen:
                S.add(f"Follow {u} → {v}.", seen, v, (u, v))
                dfs(v)
            else:
                S.add(f"{u} → {v}: {v} is finished and off the path — no cycle "
                      f"through it.", seen, u, (u, v))
        if not found:
            on_path.pop()

    for s in _order(out, start):
        if s not in seen and not found:
            dfs(s)
    S.add("Cycle found." if found else "Every node finished with no back edge — "
          "the graph is acyclic.", seen, green=[found] if found else [])
    return {"meta": _meta("cycle_directed", bool(found)), "steps": S.steps}


def _safe(graph: Graph, start: str):
    out = _out(graph)
    S = _Steps()
    S.counts = {"visits": 0}
    state: dict = {}          # 1 = on path, 2 = safe, 3 = unsafe
    safe_now = lambda: [k for k, s in state.items() if s == 2]
    S.add("A node is safe if every path from it ends somewhere with no way "
          "out. DFS: a node that can reach a cycle (or an unsafe node) is "
          "unsafe; one whose every edge leads to safe nodes is safe.")

    def dfs(u):
        state[u] = 1
        S.counts["visits"] += 1
        for v in out[u]:
            if state.get(v) in (1, 3):
                state[u] = 3
                S.add(f"{u} → {v} leads into a cycle or an unsafe node — {u} is "
                      f"unsafe.", safe_now(), u, (u, v))
                return False
            if v not in state and not dfs(v):
                state[u] = 3
                S.add(f"{u} → {v}, and {v} is unsafe — so {u} is unsafe too.",
                      safe_now(), u, (u, v))
                return False
        state[u] = 2
        S.add(f"Every edge out of {u} ends safely — {u} is safe.", safe_now(), u)
        return True

    for s in _order(out, start):
        if s not in state:
            dfs(s)
    res = sorted(safe_now())
    S.add(f"Safe nodes (highlighted): {', '.join(res) or 'none'}.", res)
    return {"meta": _meta("safe_states", res), "steps": S.steps}


def _kosaraju(graph: Graph, start: str):
    out = _out(graph)
    rev = {u: [] for u in out}
    for u, vs in out.items():
        for v in vs:
            rev[v].append(u)
    S = _Steps()
    S.counts = {"visits": 0, "components": 0}
    seen, finish = set(), []
    S.add("Pass 1: DFS the graph and list nodes by finish time. The node that "
          "finishes last lies in a 'source' component.")

    def dfs1(u):
        seen.add(u)
        S.counts["visits"] += 1
        for v in out[u]:
            if v not in seen:
                S.add(f"Pass 1: {u} → {v}.", seen, v, (u, v))
                dfs1(v)
        finish.append(u)
        S.add(f"Pass 1: {u} finishes (#{len(finish)}).", seen, u)

    for s in _order(out, start):
        if s not in seen:
            dfs1(s)
    comp: dict = {}
    S.add(f"Pass 2: reverse every edge, then DFS in reverse finish order "
          f"({', '.join(reversed(finish))}). Each tree found is one strongly "
          f"connected component.", [], dist={})

    def dfs2(u, cid):
        comp[u] = cid
        S.counts["visits"] += 1
        S.add(f"Pass 2: {u} joins component {cid}.", list(comp), u, dist=comp)
        for v in sorted(rev[u]):
            if v not in comp:
                dfs2(v, cid)

    for u in reversed(finish):
        if u not in comp:
            S.counts["components"] += 1
            dfs2(u, S.counts["components"])
    groups: dict = {}
    for u, c in comp.items():
        groups.setdefault(c, []).append(u)
    res = sorted(sorted(g) for g in groups.values())
    S.add(f"{len(res)} strongly connected component(s): "
          + "; ".join("{" + ", ".join(g) + "}" for g in res) + ". The numbers on "
          "the nodes are their component.", list(comp), dist=comp)
    return {"meta": _meta("kosaraju", res), "steps": S.steps}


def _dag_shortest(graph: Graph, start: str):
    adj = directed_adjacency(graph)
    indeg = {u: 0 for u in adj}
    for u, vs in adj.items():
        for v, _ in vs:
            indeg[v] += 1
    S = _Steps()
    S.counts = {"relaxations": 0}
    q = deque(sorted(u for u, d in indeg.items() if d == 0))
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in sorted(adj[u]):
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(topo) != len(adj):
        S.add("This graph has a directed cycle, so it is not a DAG — there is "
              "no topological order to relax along.")
        return {"meta": _meta("shortest_path_dag", None), "steps": S.steps}
    dist = {u: None for u in adj}
    dist[start] = 0
    prev: dict = {}
    reached = lambda: [x for x, d in dist.items() if d is not None]
    tree = lambda: [(prev[x], x) for x in prev]
    S.add(f"It is a DAG: topological order {' → '.join(topo)}. Relax edges in "
          f"that order — when a node is reached, every edge into it has already "
          f"been tried. Start {start} at 0.", [start], start, dist=dist)
    for u in topo:
        if dist[u] is None:
            continue
        for v, w in sorted(adj[u]):
            S.counts["relaxations"] += 1
            cand = dist[u] + w
            if dist[v] is None or cand < dist[v]:
                dist[v] = cand
                prev[v] = u
                S.add(f"{u} → {v} (weight {w:g}): {dist[u]:g} + {w:g} = {cand:g} "
                      f"improves {v}.", reached(), v, (u, v), tree(), dist)
            else:
                S.add(f"{u} → {v}: {cand:g} is not better than {dist[v]:g}.",
                      reached(), u, (u, v), tree(), dist)
    S.add("Every edge relaxed exactly once, in topological order — O(V + E). "
          "Green: the shortest-path tree.", reached(), green=tree(), dist=dist)
    return {"meta": _meta("shortest_path_dag", dict(dist)), "steps": S.steps}


def _network_delay(graph: Graph, start: str):
    """Dijkstra from the source; the signal reaches everyone when the
    farthest node hears it, so the answer is the largest distance."""
    import heapq
    adj = directed_adjacency(graph)
    S = _Steps()
    S.counts = {"settled": 0}
    dist = {u: None for u in adj}
    dist[start] = 0
    prev: dict = {}
    pq = [(0, start)]
    done: set = set()
    S.add(f"A signal leaves {start}. It reaches each node along the fastest "
          f"route (Dijkstra, edges one-way); the delay is when the LAST node "
          f"hears it.", [start], start, dist=dist)
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        S.counts["settled"] += 1
        S.add(f"Settle {u}: the signal arrives at time {d:g}.", sorted(done), u,
              green=[(prev[x], x) for x in prev], dist=dist)
        for v, w in sorted(adj[u]):
            if w < 0:
                continue
            if dist[v] is None or d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                S.add(f"{u} → {v}: arrives at {d:g} + {w:g} = {dist[v]:g}.",
                      sorted(done), v, (u, v), [(prev[x], x) for x in prev], dist)
    if any(d is None for d in dist.values()):
        res = -1
        S.add("Some node is never reached — the answer is −1.", sorted(done),
              green=[(prev[x], x) for x in prev], dist=dist)
    else:
        res = max(dist.values())
        S.add(f"Everyone has the signal by time {res:g} — the largest distance.",
              sorted(done), green=[(prev[x], x) for x in prev], dist=dist)
    return {"meta": _meta("network_delay", res), "steps": S.steps}


def trace_for(algo):
    return {"cycle_directed": _cycle, "safe_states": _safe,
            "kosaraju": _kosaraju, "shortest_path_dag": _dag_shortest,
            "network_delay": _network_delay}[algo]
