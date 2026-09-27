"""More graph algorithms with text input (batch 77) on the `grid` view.

* euler_path — Hierholzer: an undirected graph has an Euler path iff it is
  connected (ignoring isolated vertices) and 0 or 2 vertices have odd
  degree; start at an odd one. Walk unused edges greedily, pushing
  vertices on a stack; when stuck, pop onto the answer. Detours get spliced
  in automatically.
* longest_path_dag — longest paths are NP-hard in general, but in a DAG
  process vertices in topological order and relax with max instead of min.
* count_paths_dag — ways[v] = Σ ways[u] over edges u→v, in topological
  order.
"""

from collections import deque

from app.tracers.grid_common import Grid

TITLES = {
    "euler_path": "Euler Path / Circuit (Hierholzer)",
    "longest_path_dag": "Longest Path in a DAG",
    "count_paths_dag": "Count Paths in a DAG",
}


def _name(x):
    x = x.strip().upper()
    if not (1 <= len(x) <= 3) or not x.isalnum():
        raise ValueError("Vertex names are 1–3 letters/digits.")
    return x


def _undirected(text):
    edges = []
    for part in [p for p in (text or "").replace(" ", "").split(",") if p]:
        if part.count("-") != 1:
            raise ValueError("Edges look like A-B, B-C (undirected).")
        edges.append(tuple(_name(x) for x in part.split("-")))
    if not (1 <= len(edges) <= 12):
        raise ValueError("Give 1–12 edges.")
    return edges


def _directed(text):
    edges, order = [], []
    for part in [p for p in (text or "").replace(" ", "").split(",") if p]:
        w = 1
        if ":" in part:
            part, wt = part.split(":", 1)
            try:
                w = int(wt)
            except ValueError:
                raise ValueError("Weights are whole numbers.") from None
            if abs(w) > 99:
                raise ValueError("Weights within ±99.")
        if part.count(">") != 1:
            raise ValueError("Edges look like S>A:3, A>T:2 (directed, weight optional).")
        u, v = (_name(x) for x in part.split(">"))
        if u == v:
            raise ValueError("No self-loops in a DAG.")
        edges.append((u, v, w))
        order += [x for x in (u, v) if x not in order]
    if not (1 <= len(edges) <= 14) or len(order) > 8:
        raise ValueError("Give 1–14 edges over at most 8 vertices.")
    return edges, order


def run(algo, text, target=None):
    if algo == "euler_path":
        return _euler(_undirected(text))
    edges, order = _directed(text)
    if "S" not in order or (algo == "count_paths_dag" and "T" not in order):
        raise ValueError("Name the start vertex S" +
                         (" and the end vertex T." if algo == "count_paths_dag" else "."))
    topo = _topo(edges, order)
    if topo is None:
        raise ValueError("That graph has a cycle — it isn't a DAG.")
    return _dag(edges, topo, algo)


def _euler(edges):
    verts = sorted({x for e in edges for x in e})
    deg = {v: 0 for v in verts}
    adj = {v: [] for v in verts}
    for i, (u, v) in enumerate(edges):
        deg[u] += 1
        deg[v] += 1
        adj[u].append((v, i))
        adj[v].append((u, i))
    G = Grid(len(edges), 3)
    G.grid = [[u, v, None] for u, v in edges]
    G.counts = {"edges_used": 0}
    cols = ["from", "to", "used #"]
    odd = [v for v in verts if deg[v] % 2]
    G.add(f"Degrees: {deg}. Odd-degree vertices: {odd or 'none'}. An Euler path "
          f"needs 0 odd vertices (a circuit) or exactly 2 (start at one of them).")
    seen, st = {verts[0]}, [verts[0]]
    while st:
        x = st.pop()
        for y, _ in adj[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    if len(seen) != len(verts) or len(odd) not in (0, 2):
        why = ("the graph is disconnected" if len(seen) != len(verts)
               else f"{len(odd)} vertices have odd degree")
        G.add(f"No Euler path: {why}.", match=False)
        return G.result("euler_path", None, None, cols)
    start = odd[0] if odd else verts[0]
    used = [False] * len(edges)
    ptr = {v: 0 for v in verts}
    stack, path = [start], []
    G.add(f"Start at {start}. Keep walking along unused edges, pushing each "
          f"vertex; when a vertex has no unused edge left, pop it onto the answer.")
    while stack:
        v = stack[-1]
        while ptr[v] < len(adj[v]) and used[adj[v][ptr[v]][1]]:
            ptr[v] += 1
        if ptr[v] == len(adj[v]):
            path.append(stack.pop())
            G.add(f"{v} has no unused edges — pop it onto the path "
                  f"(built backwards): {path[::-1]}.", match=False)
            continue
        w, i = adj[v][ptr[v]]
        used[i] = True
        G.counts["edges_used"] += 1
        G.grid[i][2] = G.counts["edges_used"]
        stack.append(w)
        G.add(f"Walk {v} → {w} (edge {i}). Stack: {stack}.", i, 2,
              path=[(k, 2) for k in range(len(edges)) if used[k]])
    path.reverse()
    kind = "circuit" if not odd else "path"
    G.add(f"Euler {kind}: {' → '.join(path)} — every edge exactly once.",
          path=[(k, 2) for k in range(len(edges))])
    return G.result("euler_path", path, None, cols)


def _topo(edges, order):
    indeg = {v: 0 for v in order}
    for _, v, _ in edges:
        indeg[v] += 1
    q = deque(v for v in order if indeg[v] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for a, b, _ in edges:
            if a == u:
                indeg[b] -= 1
                if indeg[b] == 0:
                    q.append(b)
    return out if len(out) == len(order) else None


def _dag(edges, topo, algo):
    longest = algo == "longest_path_dag"
    row = {v: i for i, v in enumerate(topo)}
    val = {v: None for v in topo}
    val["S"] = 0 if longest else 1
    frm = {v: None for v in topo}
    G = Grid(len(topo), 3)
    G.counts = {"relaxations": 0}

    def draw():
        G.grid = [[v, val[v], frm[v]] for v in topo]

    draw()
    G.add(f"Topological order (Kahn): {topo}. Every edge points down the table, "
          + ("so when we reach a vertex its best distance is final. Start: "
             "dist[S] = 0; relax with MAX." if longest else
             "so when we reach a vertex all ways into it are counted. Start: "
             "ways[S] = 1."), row["S"], 1)
    for u in topo:
        if val[u] is None:
            G.add(f"{u} is not reachable from S — skip it.", row[u], 0, match=False)
            continue
        outs = [(b, w) for a, b, w in edges if a == u]
        changed = []
        for b, w in outs:
            G.counts["relaxations"] += 1
            if longest:
                if val[b] is None or val[u] + w > val[b]:
                    val[b], frm[b] = val[u] + w, u
                    changed.append(b)
            else:
                val[b] = (val[b] or 0) + val[u]
                frm[b] = ",".join(sorted(set((frm[b] or "").split(",") + [u]) - {""}))
                changed.append(b)
        draw()
        G.add(f"Process {u} ({'dist' if longest else 'ways'} {val[u]}): "
              + (", ".join(f"{b} ← {val[b]}" for b in changed) if changed
                 else "no improvements") + ".", row[u], 1,
              [(row[b], 1) for b, _ in outs])
    cols = ["vertex", "dist" if longest else "ways", "from"]
    if not longest:
        res = val["T"] or 0
        G.add(f"{res} path(s) from S to T.", row["T"], 1, path=[(row["T"], 1)])
        return G.result("count_paths_dag", res, None, cols)
    reach = {v: d for v, d in val.items() if d is not None}
    end = max(reach, key=lambda v: (reach[v], -row[v]))
    path, v = [], end
    while v is not None:
        path.append(v)
        v = frm[v]
    path.reverse()
    G.add(f"The farthest vertex from S is {end} at distance {reach[end]}: "
          f"{' → '.join(path)}.", row[end], 1, path=[(row[x], 1) for x in path])
    return G.result("longest_path_dag", [reach[end], path], None, cols)
