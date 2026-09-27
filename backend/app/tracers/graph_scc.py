"""Strongly connected components and friends (batch 81) on the `grid` view.

* tarjan_scc — one DFS. disc[v] = visit time, low[v] = the earliest visit
  time reachable from v's subtree using at most one back edge to a vertex
  still on the stack. When low[v] = disc[v], v is the root of an SCC: pop
  the stack down to v.
* two_sat — each clause (a ∨ b) becomes two implications ¬a → b and ¬b → a.
  The formula is satisfiable iff no variable shares an SCC with its
  negation; Tarjan finds SCCs in reverse topological order, so set x true
  when x's SCC was found before ¬x's.
* lexicographic_topo — Kahn's algorithm with a min-heap instead of a queue:
  always output the smallest vertex whose in-degree is 0.
"""

import heapq

from app.tracers.grid_common import Grid

TITLES = {
    "tarjan_scc": "Strongly Connected Components (Tarjan)",
    "two_sat": "2-SAT (Implication Graph + SCC)",
    "lexicographic_topo": "Lexicographically Smallest Topological Order",
}
SCC_COLS = ["vertex", "disc", "low", "on stack", "scc #"]


def _edges(text):
    edges, order = [], []
    for part in [p for p in (text or "").replace(" ", "").split(",") if p]:
        if part.count(">") != 1:
            raise ValueError("Directed edges look like A>B, B>C.")
        u, v = (x.upper() for x in part.split(">"))
        if not (u.isalnum() and v.isalnum()) or len(u) > 3 or len(v) > 3:
            raise ValueError("Vertex names are 1–3 letters/digits.")
        edges.append((u, v))
        order += [x for x in (u, v) if x not in order]
    if not (1 <= len(edges) <= 14) or len(order) > 8:
        raise ValueError("Give 1–14 edges over at most 8 vertices.")
    return edges, order


def run(algo, text, target=None):
    if algo == "two_sat":
        return _two_sat(text)
    edges, order = _edges(text)
    if algo == "tarjan_scc":
        return _tarjan_trace(edges, sorted(order))
    return _lex_topo(edges, sorted(order))


def _tarjan(verts, adj, G, label=str):
    disc, low, on, st, comps = {}, {}, set(), [], []
    time = [0]
    row = {v: i for i, v in enumerate(verts)}

    def draw():
        for v in verts:
            c = next((k for k, cc in enumerate(comps) if v in cc), None)
            G.grid[row[v]] = [label(v), disc.get(v), low.get(v),
                              "yes" if v in on else None, c]

    def dfs(v):
        disc[v] = low[v] = time[0]
        time[0] += 1
        st.append(v)
        on.add(v)
        G.counts["visits"] += 1
        draw()
        G.add(f"Visit {label(v)}: disc = low = {disc[v]}; push it.", row[v], 1)
        for w in adj[v]:
            if w not in disc:
                dfs(w)
                low[v] = min(low[v], low[w])
                draw()
                G.add(f"Back from {label(w)}: low[{label(v)}] = min(…, low[{label(w)}]) "
                      f"= {low[v]}.", row[v], 2, [(row[w], 2)])
            elif w in on:
                low[v] = min(low[v], disc[w])
                draw()
                G.add(f"{label(v)} → {label(w)} reaches a vertex still on the stack: "
                      f"low[{label(v)}] = min(…, disc[{label(w)}]) = {low[v]}.",
                      row[v], 2, [(row[w], 1)])
        if low[v] == disc[v]:
            comp = []
            while True:
                w = st.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)
            draw()
            G.add(f"low[{label(v)}] = disc[{label(v)}]: {label(v)} roots an SCC — pop "
                  f"{[label(x) for x in comp]}.", row[v], 4,
                  path=[(row[x], 4) for x in comp])

    for v in verts:
        if v not in disc:
            dfs(v)
    return comps


def _tarjan_trace(edges, verts):
    adj = {v: sorted({b for a, b in edges if a == v}) for v in verts}
    G = Grid(len(verts), 5)
    G.grid = [[v, None, None, None, None] for v in verts]
    G.counts = {"visits": 0}
    G.add("One DFS. disc = discovery time; low = the earliest discovery time "
          "reachable from here through the DFS subtree plus one edge back to a "
          "vertex still on the stack.")
    comps = _tarjan(verts, adj, G)
    res = sorted(sorted(c) for c in comps)
    G.add(f"{len(comps)} strongly connected component(s): {res}.",
          path=[(r, 4) for r in range(len(verts))])
    return G.result("tarjan_scc", res, None, SCC_COLS)


def _two_sat(text):
    clauses, names = [], []
    for part in [p for p in (text or "").replace(" ", "").split(",") if p]:
        lits = part.split("|")
        if len(lits) != 2:
            raise ValueError("Clauses look like a|b, !a|c (two literals each, ! = not).")
        cl = []
        for lit in lits:
            neg = lit.startswith("!")
            name = lit[1:] if neg else lit
            if not (len(name) == 1 and name.isalpha() and name.islower()):
                raise ValueError("Variables are single lowercase letters.")
            if name not in names:
                names.append(name)
            cl.append((name, neg))
        clauses.append(cl)
    if not (1 <= len(clauses) <= 8) or len(names) > 4:
        raise ValueError("Give 1–8 clauses over at most 4 variables.")
    names.sort()
    lits = [(x, False) for x in names] + [(x, True) for x in names]
    label = lambda l: ("¬" if l[1] else "") + l[0]
    adj = {l: [] for l in lits}
    for (a, na), (b, nb) in clauses:
        adj[(a, not na)].append((b, nb))            # ¬a → b
        adj[(b, not nb)].append((a, na))            # ¬b → a
    G = Grid(len(lits), 5)
    G.grid = [[label(l), None, None, None, None] for l in lits]
    G.counts = {"visits": 0}
    G.add("Every clause (a ∨ b) means: if a is false then b must be true, and "
          "if b is false then a must be true — two implication edges. Find the "
          "SCCs of this implication graph with Tarjan.")
    comps = _tarjan(lits, adj, G, label)
    idx = {l: k for k, c in enumerate(comps) for l in c}
    cols = ["literal"] + SCC_COLS[1:]
    bad = [x for x in names if idx[(x, False)] == idx[(x, True)]]
    if bad:
        G.add(f"{bad[0]} and ¬{bad[0]} are in the same SCC — each implies the other, "
              f"a contradiction. Unsatisfiable.", match=False)
        return G.result("two_sat", None, None, cols)
    value = {x: idx[(x, False)] < idx[(x, True)] for x in names}
    G.add("No variable shares an SCC with its negation — satisfiable. Tarjan "
          "finishes SCCs in reverse topological order, so pick each variable's "
          f"literal whose SCC finished FIRST: {value}.",
          path=[(lits.index((x, not value[x])), 4) for x in names])
    return G.result("two_sat", value, None, cols)


def _lex_topo(edges, verts):
    indeg = {v: 0 for v in verts}
    for _, b in edges:
        indeg[b] += 1
    row = {v: i for i, v in enumerate(verts)}
    cols = ["vertex", "in-degree", "order"]
    G = Grid(len(verts), 3)
    G.grid = [[v, indeg[v], None] for v in verts]
    G.counts = {"heap_pops": 0}
    heap = [v for v in verts if indeg[v] == 0]
    heapq.heapify(heap)
    out = []
    G.add(f"Kahn's algorithm, but the ready set is a MIN-heap, so among all "
          f"vertices with in-degree 0 we always output the smallest. Ready now: "
          f"{sorted(heap)}.", None, None, [(row[v], 1) for v in heap])
    while heap:
        u = heapq.heappop(heap)
        out.append(u)
        G.counts["heap_pops"] += 1
        G.grid[row[u]][2] = len(out)
        freed = []
        for a, b in edges:
            if a == u:
                indeg[b] -= 1
                G.grid[row[b]][1] = indeg[b]
                if indeg[b] == 0:
                    heapq.heappush(heap, b)
                    freed.append(b)
        G.add(f"Output {u} (#{len(out)}); drop its out-edges"
              + (f" — {freed} become ready." if freed else ".")
              + f" Ready: {sorted(heap) or 'none'}.", row[u], 2,
              [(row[v], 1) for v in heap], [(row[v], 2) for v in out])
    if len(out) < len(verts):
        G.add("Some vertices never reached in-degree 0 — the graph has a cycle, "
              "so no topological order exists.", match=False)
        return G.result("lexicographic_topo", None, None, cols)
    G.add(f"Smallest topological order: {out}.")
    return G.result("lexicographic_topo", out, None, cols)
