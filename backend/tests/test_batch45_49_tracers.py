"""Batches 45–49 — grid graphs, grid shortest paths / union-find, undirected
and directed graph structure, Floyd–Warshall, stock state machines and the
LIS family. Each tracer is checked against a *different* method than the one
it uses (brute force, reachability, edge/vertex deletion, Bellman-Ford …).
"""

import itertools
import random
from collections import deque

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    grid_graphs as GG, grid_paths as GP, graph_undirected as GU,
    graph_directed as GD, floyd as FW, dp_stocks_lis as SL,
)
from app.tracers.common import Graph

client = TestClient(app)
R = random.Random(45)


def txt(g):
    return "/".join(",".join(str(v) for v in row) for row in g)


def rand_grid(vals, rmax=5, cmax=5):
    r, c = R.randint(1, rmax), R.randint(1, cmax)
    return [[R.choice(vals) for _ in range(c)] for _ in range(r)]


def reach_set(cells, s):
    seen, stack = {s}, [s]
    while stack:
        r, c = stack.pop()
        for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if nb in cells and nb not in seen:
                seen.add(nb)
                stack.append(nb)
    return seen


def comps(cells):
    cells, seen, n = set(cells), set(), 0
    for s in cells:
        if s not in seen:
            n += 1
            seen |= reach_set(cells, s)
    return n


def reach(g, start, ok):
    R_, C_ = len(g), len(g[0])
    seen, q = {start}, deque([start])
    while q:
        r, c = q.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R_ and 0 <= nc < C_ and (nr, nc) not in seen and ok(r, c, nr, nc):
                seen.add((nr, nc))
                q.append((nr, nc))
    return seen


class TestGridGraphs:
    def test_islands_enclaves_surrounded(self):
        for _ in range(60):
            g = rand_grid([0, 1])
            R_, C_ = len(g), len(g[0])
            land = {(r, c) for r in range(R_) for c in range(C_) if g[r][c]}
            assert GG.run("number_of_islands", txt(g))["meta"]["result"] == comps(land)
            safe = set()
            for r, c in land:
                if r in (0, R_ - 1) or c in (0, C_ - 1):
                    safe |= reach_set(land, (r, c))
            assert GG.run("number_of_enclaves", txt(g))["meta"]["result"] == len(land - safe)
            xo = [["O" if v else "X" for v in row] for row in g]
            out = GG.run("surrounded_regions", txt(xo))["meta"]["result"]
            assert out == [["O" if (r, c) in safe else "X" for c in range(C_)]
                           for r in range(R_)]

    def test_rotten_and_nearest(self):
        for _ in range(60):
            g = rand_grid([0, 1, 1, 2])
            grid, minute = [row[:] for row in g], 0
            while True:
                new = {(nr, nc) for r, row in enumerate(grid) for c, v in enumerate(row)
                       if v == 2
                       for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                       if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 1}
                if not new:
                    break
                for r, c in new:
                    grid[r][c] = 2
                minute += 1
            want = -1 if any(v == 1 for row in grid for v in row) else minute
            assert GG.run("rotten_oranges", txt(g))["meta"]["result"] == want
            g2 = rand_grid([0, 1])
            ones = [(r, c) for r, row in enumerate(g2) for c, v in enumerate(row) if v]
            if ones:
                want = [[min(abs(r - a) + abs(c - b) for a, b in ones)
                         for c in range(len(g2[0]))] for r in range(len(g2))]
                assert GG.run("nearest_one_distance", txt(g2))["meta"]["result"] == want


class TestGridPaths:
    def test_maze(self):
        for _ in range(60):
            g = rand_grid([1, 1, 0], 6, 6)
            g[0][0] = g[-1][-1] = 1
            dist, q = {(0, 0): 0}, deque([(0, 0)])
            while q:
                r, c = q.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < len(g) and 0 <= nc < len(g[0]) and g[nr][nc] \
                            and (nr, nc) not in dist:
                        dist[(nr, nc)] = dist[(r, c)] + 1
                        q.append((nr, nc))
            want = dist.get((len(g) - 1, len(g[0]) - 1), -1)
            assert GP.run("binary_maze_path", txt(g))["meta"]["result"] == want

    def test_minimax_paths_by_threshold(self):
        for _ in range(50):
            g = rand_grid(list(range(10)), 4, 4)
            end = (len(g) - 1, len(g[0]) - 1)
            eff = next(t for t in range(100) if end in reach(
                g, (0, 0), lambda r, c, nr, nc: abs(g[nr][nc] - g[r][c]) <= t))
            assert GP.run("min_effort_path", txt(g))["meta"]["result"] == eff
            swim = next(t for t in range(100) if g[0][0] <= t and end in reach(
                g, (0, 0), lambda r, c, nr, nc: g[nr][nc] <= t))
            assert GP.run("swim_rising_water", txt(g))["meta"]["result"] == swim

    def test_largest_island_and_islands_ii(self):
        def biggest(cells):
            return max((len(reach_set(cells, s)) for s in cells), default=0)
        for _ in range(60):
            g = rand_grid([0, 1], 5, 5)
            land = {(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v}
            zeros = [(r, c) for r in range(len(g)) for c in range(len(g[0])) if not g[r][c]]
            want = max([biggest(land)] + [biggest(land | {z}) for z in zeros])
            assert GP.run("largest_island", txt(g))["meta"]["result"] == want
        for _ in range(40):
            r, c = R.randint(1, 5), R.randint(1, 5)
            ops = [(R.randrange(r), R.randrange(c)) for _ in range(R.randint(1, 12))]
            text = f"{r}x{c} | " + " ".join(f"{a}:{b}" for a, b in ops)
            want, cells = [], set()
            for op in ops:
                cells.add(op)
                want.append(comps(cells))
            assert GP.run("islands_ii", text)["meta"]["result"] == want


def rand_graph(n=6, p=0.35, directed=False):
    ids = [chr(65 + i) for i in range(R.randint(2, n))]
    pairs = itertools.permutations(ids, 2) if directed else itertools.combinations(ids, 2)
    edges = [[a, b] for a, b in pairs if R.random() < p]
    return ids, edges, Graph(nodes=[{"id": x} for x in ids], edges=edges)


def ncomp(ids, edges, skip_node=None, skip_edge=None):
    adj = {x: set() for x in ids if x != skip_node}
    for a, b in edges:
        if skip_node in (a, b) or (skip_edge and {a, b} == set(skip_edge)):
            continue
        adj[a].add(b)
        adj[b].add(a)
    seen, n = set(), 0
    for s in adj:
        if s in seen:
            continue
        n += 1
        stack = [s]
        seen.add(s)
        while stack:
            u = stack.pop()
            for v in adj[u] - seen:
                seen.add(v)
                stack.append(v)
    return n


class TestUndirected:
    def test_all(self):
        for _ in range(80):
            ids, edges, g = rand_graph()
            base = ncomp(ids, edges)
            has_cycle = len(edges) > len(ids) - base
            for algo in ("cycle_undirected_bfs", "cycle_undirected_dfs"):
                assert GU.trace_for(algo)(g, ids[0])["meta"]["result"] is has_cycle
            want_b = sorted(sorted(e) for e in edges if ncomp(ids, edges, skip_edge=e) > base)
            assert GU.trace_for("bridges")(g, ids[0])["meta"]["result"] == want_b
            want_a = sorted(x for x in ids if ncomp(ids, edges, skip_node=x) > base)
            assert GU.trace_for("articulation_points")(g, ids[0])["meta"]["result"] == want_a
            want_n = -1 if len(edges) < len(ids) - 1 else base - 1
            assert GU.trace_for("connect_network_ops")(g, ids[0])["meta"]["result"] == want_n


def reachable(ids, edges):
    """reach[x] = nodes reachable from x by one or more edges."""
    r = {x: set() for x in ids}
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            new = {b} | r[b]
            if not new <= r[a]:
                r[a] |= new
                changed = True
    return r


class TestDirected:
    def test_cycle_safe_scc(self):
        for _ in range(80):
            ids, edges, g = rand_graph(directed=True, p=0.25)
            r = reachable(ids, edges)
            on_cycle = {x for x in ids if x in r[x]}
            assert GD.trace_for("cycle_directed")(g, ids[0])["meta"]["result"] is bool(on_cycle)
            safe = sorted(x for x in ids if x not in on_cycle and not (r[x] & on_cycle))
            assert GD.trace_for("safe_states")(g, ids[0])["meta"]["result"] == safe
            sccs = sorted({tuple(sorted({x} | {y for y in ids if y in r[x] and x in r[y]}))
                           for x in ids})
            assert GD.trace_for("kosaraju")(g, ids[0])["meta"]["result"] == \
                [list(c) for c in sccs]

    def test_dag_shortest(self):
        for _ in range(60):
            ids = [chr(65 + i) for i in range(R.randint(2, 6))]
            edges = [[a, b, R.randint(-4, 9)] for a, b in itertools.combinations(ids, 2)
                     if R.random() < 0.4]
            g = Graph(nodes=[{"id": x} for x in ids], edges=edges)
            dist = {x: None for x in ids}
            dist[ids[0]] = 0
            for _ in ids:
                for a, b, w in edges:
                    if dist[a] is not None and (dist[b] is None or dist[a] + w < dist[b]):
                        dist[b] = dist[a] + w
            assert GD.trace_for("shortest_path_dag")(g, ids[0])["meta"]["result"] == dist


class TestFloyd:
    def test_matrix_and_city(self):
        for _ in range(60):
            ids = [chr(65 + i) for i in range(R.randint(2, 5))]
            edges = [(a, b, R.randint(0, 9)) for a, b in itertools.permutations(ids, 2)
                     if R.random() < 0.4]
            if not edges:
                continue
            text = ",".join(f"{a}>{b}:{w}" for a, b, w in edges)
            names = sorted({x for a, b, _ in edges for x in (a, b)})
            want = []
            for s in names:
                d = {x: None for x in names}
                d[s] = 0
                for _ in names:
                    for a, b, w in edges:
                        if d[a] is not None and (d[b] is None or d[a] + w < d[b]):
                            d[b] = d[a] + w
                want.append(["∞" if d[x] is None else d[x] for x in names])
            assert FW.run("floyd_warshall", text)["meta"]["result"] == want
        out = FW.run("city_fewest_neighbours", "0-1:3,1-2:1,1-3:4,2-3:1", 4)
        assert out["meta"]["result"] == "3"


def _stock_brute(p, k=None, cooldown=False, fee=0):
    def go(i, holding, trades, rest):
        if i == len(p):
            return 0 if not holding else float("-inf")
        opts = [go(i + 1, holding, trades, False)]
        if holding:
            opts.append(p[i] - fee + go(i + 1, False, trades, cooldown))
        elif not rest and (k is None or trades < k):
            opts.append(-p[i] + go(i + 1, True, trades + 1, False))
        return max(opts)
    return go(0, False, 0, False)


class TestStocksLIS:
    def test_stocks(self):
        for _ in range(60):
            p = [R.randint(0, 9) for _ in range(R.randint(1, 7))]
            t = ",".join(map(str, p))
            assert SL.run("stock_ii", t)["meta"]["result"] == _stock_brute(p)
            assert SL.run("stock_iii", t)["meta"]["result"] == _stock_brute(p, k=2)
            k = R.randint(1, 3)
            assert SL.run("stock_iv", t, k)["meta"]["result"] == _stock_brute(p, k=k)
            assert SL.run("stock_cooldown", t)["meta"]["result"] == \
                _stock_brute(p, cooldown=True)
            fee = R.randint(0, 3)
            assert SL.run("stock_fee", t, fee)["meta"]["result"] == _stock_brute(p, fee=fee)

    def test_lis_family(self):
        for _ in range(60):
            a = [R.randint(1, 12) for _ in range(R.randint(1, 8))]
            t = ",".join(map(str, a))
            idx = [c for r in range(1, len(a) + 1) for c in itertools.combinations(range(len(a)), r)
                   if all(a[x] < a[y] for x, y in zip(c, c[1:]))]
            L = max(len(c) for c in idx)
            got = SL.run("print_lis", t)["meta"]["result"]
            assert len(got) == L and any([a[i] for i in c] == got for c in idx if len(c) == L)
            assert SL.run("number_of_lis", t)["meta"]["result"] == \
                sum(1 for c in idx if len(c) == L)
            s = sorted(set(a))
            divs = [c for r in range(1, len(s) + 1) for c in itertools.combinations(s, r)
                    if all(y % x == 0 for x, y in zip(c, c[1:]))]
            assert len(SL.run("largest_divisible_subset", t)["meta"]["result"]) == \
                max(len(c) for c in divs)
            bit = max(len(c) for r in range(1, len(a) + 1) for c in itertools.combinations(a, r)
                      if any(all(x < y for x, y in zip(c[:m + 1], c[1:m + 1])) and
                             all(x > y for x, y in zip(c[m:], c[m + 1:]))
                             for m in range(len(c))))
            assert SL.run("longest_bitonic", t)["meta"]["result"] == bit
        assert SL.run("longest_string_chain", "a,b,ba,bca,bda,bdca")["meta"]["result"] == 4
        assert SL.run("longest_string_chain", "xbc,pcxbcf,xb,cxbc,pcxbc")["meta"]["result"] == 5


class TestEndpoints:
    def test_text_ids(self):
        samples = {
            "number_of_islands": ("1,0/0,1", None), "rotten_oranges": ("2,1/1,1", None),
            "nearest_one_distance": ("0,1/1,0", None), "surrounded_regions": ("X,O/O,X", None),
            "number_of_enclaves": ("0,0,0/0,1,0/0,0,0", None),
            "binary_maze_path": ("1,1/0,1", None), "min_effort_path": ("1,2/3,4", None),
            "swim_rising_water": ("0,2/1,3", None), "largest_island": ("1,0/0,1", None),
            "islands_ii": ("2x2 | 0:0 1:1", None), "floyd_warshall": ("A>B:1,B>C:2", None),
            "city_fewest_neighbours": ("A-B:1,B-C:2", 2), "stock_ii": ("7,1,5", None),
            "stock_iii": ("3,5,0,4", None), "stock_iv": ("3,2,6", 1),
            "stock_cooldown": ("1,2,3", None), "stock_fee": ("1,3,2,8", 2),
            "print_lis": ("3,1,2", None), "largest_divisible_subset": ("1,2,3", None),
            "longest_string_chain": ("a,ab", None), "longest_bitonic": ("1,3,2", None),
            "number_of_lis": ("1,3,2", None),
        }
        for algo, (text, t) in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)

    def test_graph_ids(self):
        graph = {"nodes": [{"id": x} for x in "ABCD"],
                 "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"]]}
        for mod in (GU, GD):
            for algo in mod.TITLES:
                r = client.post("/api/trace", json={"algorithm": algo, "graph": graph,
                                                    "start": "A"})
                assert r.status_code == 200, (algo, r.text)

    def test_bad_inputs_and_detect(self):
        for p in ({"algorithm": "rotten_oranges", "text": "3,1"},
                  {"algorithm": "binary_maze_path", "text": "0,1/1,1"},
                  {"algorithm": "islands_ii", "text": "3x3"},
                  {"algorithm": "floyd_warshall", "text": "A~B:1"},
                  {"algorithm": "stock_iv", "text": "1,2", "target": 9}):
            assert client.post("/api/trace", json=p).status_code == 400, p
        for mod in (GG, GP, GU, GD, FW, SL):
            for algo in mod.TITLES:
                body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
                assert body["algorithm"] == algo, algo
