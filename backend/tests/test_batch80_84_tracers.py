"""Batches 80–84 — Aho–Corasick and substring hashing, Tarjan SCC / 2-SAT /
lexicographic topo, geometry, advanced DP patterns and Fenwick tricks. Each
tracer is checked against a brute-force reference on random input.
"""

import itertools
import math
import random
from collections import deque

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    bit_more as BM, dp_adv as DA, geometry as GE, graph_scc as GS, string_auto as SA,
)

client = TestClient(app)
R = random.Random(80)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))
MODS = (BM, DA, GE, GS, SA)


def rand_tree(n, lo=1, hi=60):
    """Random binary tree: (level-order text, kids by index, values by index)."""
    vals = [R.randint(lo, hi) for _ in range(n)]
    kids = {0: [None, None]}
    for i in range(1, n):
        while True:
            p = R.choice(list(kids))
            side = R.randint(0, 1)
            if kids[p][side] is None:
                kids[p][side] = i
                kids[i] = [None, None]
                break
    out, q = [], [0]
    while q:
        x = q.pop(0)
        out.append(None if x is None else vals[x])
        if x is not None:
            q += kids[x]
    while out[-1] is None:
        out.pop()
    return ",".join("null" if v is None else str(v) for v in out), kids, vals


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


class TestStrings:
    def test_aho(self):
        for _ in range(40):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 14)))
            pats = list(dict.fromkeys("".join(R.choice("ab") for _ in range(R.randint(1, 4)))
                                      for _ in range(R.randint(1, 4))))
            want = sorted([p, i] for p in pats for i in range(len(s)) if s.startswith(p, i))
            got = res(SA.run("aho_corasick", f"{s} | {', '.join(pats)}"))
            assert sorted(got) == want, (s, pats)

    def test_hash(self):
        for _ in range(40):
            s = "".join(R.choice("ab") for _ in range(R.randint(2, 14)))
            qs = []
            for _ in range(R.randint(1, 5)):
                ln = R.randint(1, len(s))
                qs.append((R.randint(0, len(s) - ln), R.randint(0, len(s) - ln), ln))
            text = f"{s} | " + ", ".join(f"{a} {b} {l}" for a, b, l in qs)
            assert res(SA.run("substring_hash", text)) == \
                [s[a:a + l] == s[b:b + l] for a, b, l in qs]


class TestGraphs:
    def test_tarjan(self):
        for _ in range(40):
            names = "ABCDEF"[:R.randint(2, 6)]
            edges = sorted({tuple(R.sample(names, 2)) for _ in range(R.randint(1, 12))})
            verts = sorted({x for e in edges for x in e})
            reach = {v: {v} for v in verts}
            for _ in verts:
                for u, v in edges:
                    for x in verts:
                        if u in reach[x]:
                            reach[x].add(v)
            comps = {tuple(sorted(v for v in verts if u in reach[v] and v in reach[u]))
                     for u in verts}
            got = res(GS.run("tarjan_scc", ", ".join(f"{u}>{v}" for u, v in edges)))
            assert got == sorted(list(c) for c in comps)

    def test_two_sat(self):
        for _ in range(60):
            names = "abc"[:R.randint(1, 3)]
            clauses = [[(R.choice(names), R.random() < 0.5) for _ in range(2)]
                       for _ in range(R.randint(1, 8))]
            text = ", ".join("|".join(("!" if n else "") + x for x, n in c) for c in clauses)
            used = sorted({x for c in clauses for x, _ in c})
            sat = lambda val: all(any(val[x] != n for x, n in c) for c in clauses)
            brute = any(sat(dict(zip(used, bits)))
                        for bits in itertools.product([False, True], repeat=len(used)))
            got = res(GS.run("two_sat", text))
            assert (got is not None) == brute, text
            if got:
                assert sat(got)

    def test_lex_topo(self):
        for _ in range(40):
            names = "ABCDEF"[:R.randint(2, 6)]
            edges = sorted({tuple(R.sample(names, 2)) for _ in range(R.randint(1, 8))})
            verts = sorted({x for e in edges for x in e})
            want = None
            for perm in itertools.permutations(verts):
                pos = {v: i for i, v in enumerate(perm)}
                if all(pos[u] < pos[v] for u, v in edges):
                    want = list(perm)
                    break
            got = res(GS.run("lexicographic_topo", ", ".join(f"{u}>{v}" for u, v in edges)))
            assert got == want


class TestGeometry:
    def test_hull(self):
        for _ in range(40):
            pts = list({(R.randint(0, 9), R.randint(0, 9)) for _ in range(R.randint(3, 12))})
            got = [tuple(p) for p in
                   res(GE.run("convex_hull", "; ".join(f"{x} {y}" for x, y in pts)))]
            assert set(got) <= set(pts)
            n = len(got)
            if n >= 3:                         # CCW, every point on or inside, strict corners
                for i in range(n):
                    a, b = got[i], got[(i + 1) % n]
                    assert all(cross(a, b, p) >= 0 for p in pts)
                    assert cross(got[i - 1], a, b) > 0

    def test_area_and_closest(self):
        for _ in range(40):
            w, h = R.randint(1, 9), R.randint(1, 9)
            x0, y0 = R.randint(0, 9 - w), R.randint(0, 9 - h)
            rect = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
            if R.random() < 0.5:
                rect.reverse()
            assert res(GE.run("polygon_area", "; ".join(f"{x} {y}" for x, y in rect))) == w * h
            pts = list({(R.randint(0, 9), R.randint(0, 9)) for _ in range(R.randint(2, 10))})
            if len(pts) < 2:
                continue
            best = min(math.dist(a, b) for a, b in itertools.combinations(pts, 2))
            d, pair = res(GE.run("closest_pair", "; ".join(f"{x} {y}" for x, y in pts)))
            assert abs(d - best) < 1e-3 and abs(math.dist(*pair) - best) < 1e-9


class TestDP:
    def test_digit_dp(self):
        for _ in range(40):
            n, s = R.randint(0, 3000), R.randint(0, 20)
            want = sum(sum(map(int, str(x))) == s for x in range(n + 1))
            assert res(DA.run("digit_dp", str(n), s)) == want

    def test_tree_robber_and_reroot(self):
        for _ in range(30):
            text, kids, vals = rand_tree(R.randint(1, 10), 0, 20)
            n = len(vals)
            adj = {i: [] for i in range(n)}
            for p, pair in kids.items():
                for c in pair:
                    if c is not None:
                        adj[p].append(c)
                        adj[c].append(p)
            best = 0
            for m in range(1 << n):
                chosen = [i for i in range(n) if m >> i & 1]
                if all(b not in adj[a] for a in chosen for b in chosen):
                    best = max(best, sum(vals[i] for i in chosen))
            assert res(DA.run("tree_robber", text)) == best
            order, q = [], deque([0])          # the tracer numbers nodes in BFS order
            while q:
                x = q.popleft()
                order.append(x)
                q += [c for c in kids[x] if c is not None]

            def total(src):
                dist, dq = {src: 0}, deque([src])
                while dq:
                    x = dq.popleft()
                    for y in adj[x]:
                        if y not in dist:
                            dist[y] = dist[x] + 1
                            dq.append(y)
                return sum(dist.values())
            assert res(DA.run("sum_distances_tree", text)) == [total(x) for x in order]

    def test_sos(self):
        for _ in range(30):
            size = R.choice([2, 4, 8, 16])
            a = [R.randint(-9, 9) for _ in range(size)]
            want = [sum(a[s] for s in range(size) if s & m == s) for m in range(size)]
            assert res(DA.run("sos_dp", csv(a))) == want


class TestFenwick:
    def test_kth_and_inversions(self):
        for _ in range(40):
            bag, ops, want = [], [], []
            for _ in range(R.randint(1, 12)):
                kind = R.choice(["add", "add", "remove", "kth"])
                if kind == "kth":
                    k = R.randint(1, 6)
                    ops.append(f"kth {k}")
                    want.append(sorted(bag)[k - 1] if k <= len(bag) else None)
                else:
                    v = R.randint(1, 16)
                    ops.append(f"{kind} {v}")
                    if kind == "add":
                        bag.append(v)
                    elif v in bag:
                        bag.remove(v)
            assert res(BM.run("bit_kth", ", ".join(ops))) == want
            a = [R.randint(1, 16) for _ in range(R.randint(1, 10))]
            assert res(BM.run("inversions_bit", csv(a))) == \
                sum(a[i] > a[j] for i in range(len(a)) for j in range(i + 1, len(a)))

    def test_prefix_2d(self):
        for _ in range(30):
            r, c = R.randint(1, 5), R.randint(1, 5)
            g = [[R.randint(-9, 9) for _ in range(c)] for _ in range(r)]
            qs = []
            for _ in range(R.randint(1, 4)):
                r1, r2 = sorted(R.randint(0, r - 1) for _ in range(2))
                c1, c2 = sorted(R.randint(0, c - 1) for _ in range(2))
                qs.append((r1, c1, r2, c2))
            text = "/".join(csv(row) for row in g) + " | " + \
                ", ".join(" ".join(map(str, q)) for q in qs)
            assert res(BM.run("prefix_sum_2d", text)) == \
                [sum(g[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
                 for r1, c1, r2, c2 in qs]


class TestWiring:
    def test_every_id_through_api(self):
        samples = {"aho_corasick": "abab | ab, b", "substring_hash": "abab | 0 2 2",
                   "tarjan_scc": "A>B, B>A", "two_sat": "a|b", "lexicographic_topo": "B>A",
                   "convex_hull": "0 0; 2 0; 1 2", "polygon_area": "0 0; 2 0; 0 2",
                   "closest_pair": "0 0; 3 4", "tree_robber": "3,2,3",
                   "sos_dp": "1,2,3,4", "sum_distances_tree": "1,2,3",
                   "bit_kth": "add 3, kth 1", "inversions_bit": "3,1,2",
                   "prefix_sum_2d": "1,2/3,4 | 0 0 1 1"}
        with_target = {"digit_dp": ("50", 5)}
        every = set().union(*(m.TITLES for m in MODS))
        assert set(samples) | set(with_target) == every
        tree = {"aho_corasick", "tree_robber", "sum_distances_tree"}
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["meta"]["view"] == ("tree" if algo in tree else "grid"), algo
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        for algo in every:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "aho_corasick", "text": "abc"},
                  {"algorithm": "substring_hash", "text": "abc | 0 2 5"},
                  {"algorithm": "tarjan_scc", "text": "A-B"},
                  {"algorithm": "two_sat", "text": "a|b|c"},
                  {"algorithm": "convex_hull", "text": "0 0; 10 1"},
                  {"algorithm": "polygon_area", "text": "0 0; 1 1"},
                  {"algorithm": "digit_dp", "text": "100", "target": 50},
                  {"algorithm": "sos_dp", "text": "1,2,3"},
                  {"algorithm": "tree_robber", "text": "1,-5"},
                  {"algorithm": "bit_kth", "text": "add 20"},
                  {"algorithm": "inversions_bit", "text": "0,1"},
                  {"algorithm": "prefix_sum_2d", "text": "1,2/3,4 | 1 1 0 0"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
