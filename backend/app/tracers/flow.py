"""Flows and matching (batch 71) on the `grid` view.

* max_flow — Edmonds–Karp: BFS finds the shortest augmenting path in the
  residual graph; push its bottleneck; repeat until S can't reach T. Cell
  (u, v) of the grid shows flow/capacity for edge u→v.
* min_cut — after max flow, the nodes S can still reach in the residual
  graph form one side; saturated edges leaving that side are the minimum
  cut, and their capacities add up to the max flow.
* bipartite_matching — Kuhn's algorithm: for each left vertex, try each
  neighbour; take it if free, or if its current partner can be re-matched
  elsewhere (an augmenting path).
"""

from collections import deque

from app.tracers.grid_common import Grid

TITLES = {
    "max_flow": "Maximum Flow (Edmonds–Karp)",
    "min_cut": "Minimum s-t Cut",
    "bipartite_matching": "Maximum Bipartite Matching (Kuhn)",
}


def _edges(text):
    edges, order = [], []
    for part in [p.strip() for p in (text or "").split(",") if p.strip()]:
        try:
            uv, cap = part.replace(" ", "").split(":")
            u, v = uv.split(">")
            cap = int(cap)
        except ValueError:
            raise ValueError("Edges look like S>A:10, A>T:5 (from>to:capacity).") from None
        u, v = u.upper(), v.upper()
        if not (u.isalnum() and v.isalnum()) or u == v or not (1 <= cap <= 99):
            raise ValueError("Names are letters/digits, no self-loops, capacity 1–99.")
        for x in (u, v):
            if x not in order:
                order.append(x)
        edges.append((u, v, cap))
    if not edges or len(edges) > 14 or len(order) > 7:
        raise ValueError("Give 1–14 edges over at most 7 nodes.")
    if "S" not in order or "T" not in order:
        raise ValueError("Name the source S and the sink T.")
    order = ["S"] + [x for x in order if x not in ("S", "T")] + ["T"]
    return edges, order


def run(algo, text, target=None):
    if algo == "bipartite_matching":
        return _kuhn(*_bipartite(text))
    edges, order = _edges(text)
    return _edmonds_karp(edges, order, algo)


def _edmonds_karp(edges, order, algo):
    n = len(order)
    idx = {x: i for i, x in enumerate(order)}
    cap = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        cap[idx[u]][idx[v]] += c
    flow = [[0] * n for _ in range(n)]
    G = Grid(n, n)
    G.counts = {"augmenting_paths": 0, "flow": 0}

    def draw():
        G.grid = [[f"{flow[i][j]}/{cap[i][j]}" if cap[i][j] else None
                   for j in range(n)] for i in range(n)]

    draw()
    G.add("Cell (u, v) = flow/capacity on edge u→v. Residual room on u→v is "
          "cap − flow, plus flow on v→u that could be pushed back. Repeatedly "
          "BFS from S to T through edges with room, and push the bottleneck.")
    s, t = 0, n - 1
    while True:
        par = [-1] * n
        par[s] = s
        q = deque([s])
        while q and par[t] == -1:
            u = q.popleft()
            for v in range(n):
                room = cap[u][v] - flow[u][v] + flow[v][u]
                if par[v] == -1 and room > 0:
                    par[v] = u
                    q.append(v)
        if par[t] == -1:
            reach = [order[i] for i in range(n) if par[i] != -1]
            G.add(f"BFS can't reach T any more — the flow is maximum: "
                  f"{G.counts['flow']}. (S still reaches {reach}.)", match=False)
            break
        path, v = [], t
        while v != s:
            path.append((par[v], v))
            v = par[v]
        path.reverse()
        push = min(cap[u][v] - flow[u][v] + flow[v][u] for u, v in path)
        for u, v in path:
            back = min(push, flow[v][u])           # cancel reverse flow first
            flow[v][u] -= back
            flow[u][v] += push - back
        G.counts["augmenting_paths"] += 1
        G.counts["flow"] += push
        draw()
        names = " → ".join([order[path[0][0]]] + [order[v] for _, v in path])
        G.add(f"Augmenting path {names}: bottleneck {push}. Total flow "
              f"{G.counts['flow']}.", None, None, [], path)
    if algo == "max_flow":
        return G.result("max_flow", G.counts["flow"], order, order)
    side = {i for i in range(n) if par[i] != -1}
    cut = [(u, v) for u in sorted(side) for v in range(n) if v not in side and cap[u][v]]
    G.add(f"S-side = {[order[i] for i in sorted(side)]}. Every edge from the S-side "
          f"to the T-side is saturated; together they form the minimum cut, "
          f"capacity {sum(cap[u][v] for u, v in cut)} = the max flow.",
          None, None, [], cut)
    res = sorted(f"{order[u]}>{order[v]}" for u, v in cut)
    return G.result("min_cut", res, order, order, max_flow=G.counts["flow"])


def _bipartite(text):
    left, rights, adj = [], [], {}
    for part in [p.strip() for p in (text or "").split(";") if p.strip()]:
        if ":" not in part:
            raise ValueError("Give 'a: x y; b: x' — each left vertex and the right "
                             "vertices it may pair with.")
        u, vs = part.split(":", 1)
        u = u.strip()
        nb = vs.replace(",", " ").split()
        if not u.isalnum() or not all(v.isalnum() for v in nb) or u in adj:
            raise ValueError("Names are letters/digits; list each left vertex once.")
        left.append(u)
        adj[u] = list(dict.fromkeys(nb))
        rights += [v for v in adj[u] if v not in rights]
    if not (1 <= len(left) <= 6) or not (1 <= len(rights) <= 6):
        raise ValueError("1–6 vertices on each side.")
    return left, sorted(rights), adj


def _kuhn(left, rights, adj):
    G = Grid(len(left), len(rights))
    ri = {v: j for j, v in enumerate(rights)}
    match = {}                                       # right → left
    G.counts = {"tries": 0, "matched": 0}

    def draw():
        G.grid = [["M" if match.get(v) == u else ("·" if v in adj[u] else None)
                   for v in rights] for u in left]

    draw()
    G.add("Rows are left vertices, columns right ones; · = allowed pair, M = "
          "matched. For each left vertex, try its neighbours: a free one is "
          "taken; a taken one is freed if its partner can move elsewhere.")

    def try_(u, seen):
        r = left.index(u)
        for v in adj[u]:
            if v in seen:
                continue
            seen.add(v)
            G.counts["tries"] += 1
            if v not in match:
                match[v] = u
                draw()
                G.add(f"{u} → {v}: {v} is free — match.", r, ri[v])
                return True
            owner = match[v]
            G.add(f"{u} → {v}: {v} is taken by {owner} — can {owner} move?",
                  r, ri[v], [(left.index(owner), ri[v])], match=False)
            if try_(owner, seen):
                match[v] = u
                draw()
                G.add(f"{owner} moved, so {u} takes {v}.", r, ri[v])
                return True
        return False

    for u in left:
        if try_(u, set()):
            G.counts["matched"] += 1
        else:
            G.add(f"{u} can't be matched without breaking the rest.",
                  left.index(u), None, match=False)
    pairs = sorted((u, v) for v, u in match.items())
    G.add(f"Maximum matching: {len(pairs)} pair(s) — {pairs}.",
          path=[(left.index(u), ri[v]) for u, v in pairs])
    return G.result("bipartite_matching", len(pairs), left, rights,
                    pairs=[list(p) for p in pairs])
