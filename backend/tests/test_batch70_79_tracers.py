"""Batches 70–79 — heuristic search, flows, binary lifting, bitmask DP, range
queries, number theory, suffix arrays, DAG/Euler graphs, algebra tricks and
game theory. Each tracer is checked against a brute-force reference; the
last class also guards the catalog's category list.
"""

import itertools
import math
import os
import random
import re
from collections import deque
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    algebra as AL, bitmask_dp as BM, flow as FL, games as GA, graph_more as GM,
    lifting as LF, number_theory as NT, range_queries as RQ, search_heuristic as SH,
    suffix_structs as SS,
)

client = TestClient(app)
R = random.Random(70)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))
MODS = (AL, BM, FL, GA, GM, LF, NT, RQ, SH, SS)


def bfs_len(g):
    rows, cols = len(g), len(g[0])
    s = next((r, c) for r in range(rows) for c in range(cols) if g[r][c] == "S")
    dist = {s: 0}
    q = deque([s])
    while q:
        r, c = q.popleft()
        if g[r][c] == "G":
            return dist[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))
    return -1


class TestSearch:
    def test_a_star_and_best_first(self):
        for _ in range(40):
            r, c = R.randint(2, 6), R.randint(2, 6)
            g = [[R.choice("...#") for _ in range(c)] for _ in range(r)]
            (a, b), (x, y) = R.sample([(i, j) for i in range(r) for j in range(c)], 2)
            g[a][b], g[x][y] = "S", "G"
            text = "/".join("".join(row) for row in g)
            want = bfs_len(g)
            assert res(SH.run("a_star_grid", text)) == want
            got = res(SH.run("best_first_grid", text))
            assert (got == -1) == (want == -1) and got >= want

    def test_zero_one(self):
        for _ in range(30):
            r, c = R.randint(1, 5), R.randint(1, 5)
            g = [[R.randint(0, 1) for _ in range(c)] for _ in range(r)]
            dist = {(0, 0): g[0][0]}                  # Bellman-style reference
            for _ in range(r * c):
                for (i, j), d in list(dist.items()):
                    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ni, nj = i + di, j + dj
                        if 0 <= ni < r and 0 <= nj < c and d + g[ni][nj] < dist.get((ni, nj), 99):
                            dist[(ni, nj)] = d + g[ni][nj]
            assert res(SH.run("zero_one_bfs", "/".join(csv(x) for x in g))) == dist[(r - 1, c - 1)]


class TestFlows:
    def test_max_flow_equals_min_cut(self):
        for _ in range(40):
            names = ["S", "A", "B", "C", "T"][:R.randint(2, 5)]
            names[-1] = "T"
            edges = {}
            for _ in range(R.randint(1, 10)):
                u, v = R.sample(names, 2)
                edges[(u, v)] = R.randint(1, 9)
            touched = {x for e in edges for x in e}
            if "S" not in touched or "T" not in touched:
                continue
            text = ", ".join(f"{u}>{v}:{w}" for (u, v), w in edges.items())
            others = [x for x in names if x not in ("S", "T")]
            best = min(sum(w for (u, v), w in edges.items() if u in side and v not in side)
                       for k in range(len(others) + 1)
                       for pick in itertools.combinations(others, k)
                       for side in [{"S", *pick}])
            assert res(FL.run("max_flow", text)) == best, text
            cut = res(FL.run("min_cut", text))
            assert sum(edges[tuple(e.split(">"))] for e in cut) == best

    def test_matching(self):
        for _ in range(30):
            left = [f"l{i}" for i in range(R.randint(1, 5))]
            rights = [f"r{i}" for i in range(R.randint(1, 5))]
            adj = {u: R.sample(rights, R.randint(1, len(rights))) for u in left}
            best = 0
            for k in range(len(left), 0, -1):
                if any(len(set(p)) == k
                       for us in itertools.combinations(left, k)
                       for p in itertools.product(*(adj[u] for u in us))):
                    best = k
                    break
            text = "; ".join(f"{u}: {' '.join(adj[u])}" for u in left)
            out = FL.run("bipartite_matching", text)
            assert res(out) == best
            pairs = out["meta"]["pairs"]
            assert len({v for _, v in pairs}) == len(pairs)
            assert all(v in adj[u] for u, v in pairs)


def rand_tree(n):
    vals = R.sample(range(1, 60), n)
    kids = {vals[0]: [None, None]}
    par = {vals[0]: None}
    for v in vals[1:]:
        while True:
            p = R.choice(list(kids))
            side = R.randint(0, 1)
            if kids[p][side] is None:
                kids[p][side] = v
                kids[v] = [None, None]
                par[v] = p
                break
    out, q = [], [vals[0]]
    while q:
        x = q.pop(0)
        out.append(x)
        if x is not None:
            q += kids[x]
    while out[-1] is None:
        out.pop()
    return ",".join("null" if v is None else str(v) for v in out), par, vals


class TestLifting:
    def test_lca_and_kth(self):
        for _ in range(40):
            text, par, vals = rand_tree(R.randint(1, 15))

            def anc(x):
                out = []
                while x is not None:
                    out.append(x)
                    x = par[x]
                return out
            a, b = R.choice(vals), R.choice(vals)
            la = anc(a)
            want = next(x for x in anc(b) if x in la)
            assert res(LF.run("lca_lifting", f"{text} | {a} {b}")) == want
            k = R.randint(0, 6)
            assert res(LF.run("kth_ancestor", f"{text} | {a} {k}")) == \
                (la[k] if k < len(la) else -1)


class TestBitmask:
    def test_tsp_and_assignment(self):
        for _ in range(20):
            n = R.randint(2, 5)
            d = [[0 if i == j else R.randint(1, 20) for j in range(n)] for i in range(n)]
            want = min(sum(d[a][b] for a, b in zip((0,) + p, p + (0,)))
                       for p in itertools.permutations(range(1, n)))
            assert res(BM.run("tsp_bitmask", "/".join(csv(r) for r in d))) == want
            m = R.randint(2, 4)
            c = [[R.randint(0, 20) for _ in range(m)] for _ in range(m)]
            want = min(sum(c[i][p[i]] for i in range(m)) for p in itertools.permutations(range(m)))
            assert res(BM.run("assignment_bitmask", "/".join(csv(r) for r in c))) == want


class TestRangeQueries:
    def test_all_three(self):
        for _ in range(40):
            a = [R.randint(-9, 9) for _ in range(R.randint(1, 8))]
            n = len(a)
            qs = []
            for _ in range(R.randint(1, 6)):
                lo = R.randint(0, n - 1)
                qs.append((lo, R.randint(lo, n - 1)))
            text = f"{csv(a)} | " + ", ".join(f"min {l} {r}" for l, r in qs)
            assert res(RQ.run("sparse_table", text)) == [min(a[l:r + 1]) for l, r in qs]
            arr, ops, want = a[:], [], []
            for _ in range(R.randint(1, 6)):
                if R.random() < 0.5:
                    lo = R.randint(0, n - 1)
                    hi = R.randint(lo, n - 1)
                    ops.append(f"sum {lo} {hi}")
                    want.append(sum(arr[lo:hi + 1]))
                else:
                    i, v = R.randint(0, n - 1), R.randint(-9, 9)
                    ops.append(f"set {i} {v}")
                    arr[i] = v
            assert res(RQ.run("sqrt_decomposition", f"{csv(a)} | " + ", ".join(ops))) == want
            arr, ops, want = a[:], [], []
            for _ in range(R.randint(1, 6)):
                lo = R.randint(0, n - 1)
                hi = R.randint(lo, n - 1)
                if R.random() < 0.5:
                    v = R.randint(-5, 5)
                    ops.append(f"add {lo} {hi} {v}")
                    for i in range(lo, hi + 1):
                        arr[i] += v
                else:
                    ops.append(f"sum {lo} {hi}")
                    want.append(sum(arr[lo:hi + 1]))
            assert res(RQ.run("lazy_segment_tree", f"{csv(a)} | " + ", ".join(ops))) == want


class TestNumberTheory:
    def test_gcd_inverse_ncr_phi(self):
        for _ in range(60):
            a, b = R.randint(0, 999), R.randint(1, 999)
            g, x, y = res(NT.run("extended_gcd", f"{a}, {b}"))
            assert g == math.gcd(a, b) and a * x + b * y == g
            m = R.randint(2, 99)
            inv = res(NT.run("mod_inverse", f"{b}, {m}"))
            assert inv == (pow(b, -1, m) if math.gcd(b, m) == 1 else -1)
            n = R.randint(0, 20)
            r = R.randint(0, n)
            assert res(NT.run("ncr_mod", f"{n}, {r}")) == math.comb(n, r) % (10 ** 9 + 7)
            k = R.randint(1, 3000)
            assert res(NT.run("euler_totient", str(k))) == \
                sum(math.gcd(i, k) == 1 for i in range(1, k + 1))

    def test_spf_and_crt(self):
        for x in range(2, 61):
            fac, v, p = [], x, 2
            while v > 1:
                while v % p == 0:
                    fac.append(p)
                    v //= p
                p += 1
            assert res(NT.run("spf_sieve", "60", x)) == fac
        for _ in range(40):
            mods = [R.randint(2, 12) for _ in range(R.randint(2, 3))]
            pairs = [(R.randint(0, m - 1), m) for m in mods]
            M = math.lcm(*mods)
            sol = next((x for x in range(M) if all(x % m == r for r, m in pairs)), None)
            got = res(NT.run("crt", ", ".join(f"{r} {m}" for r, m in pairs)))
            assert got == ([sol, M] if sol is not None else -1)


class TestSuffix:
    def test_sa_lcp_lrs(self):
        for _ in range(40):
            s = "".join(R.choice("ab") for _ in range(R.randint(2, 10)))
            sa = sorted(range(len(s)), key=lambda i: s[i:])
            assert res(SS.run("suffix_array", s)) == sa
            lcp = [0] + [len(os.path.commonprefix([s[sa[i - 1]:], s[sa[i]:]]))
                         for i in range(1, len(s))]
            assert res(SS.run("lcp_kasai", s)) == lcp
            got = res(SS.run("longest_repeated_substring", s))
            assert len(got) == max(lcp)
            assert not got or sum(s.startswith(got, i) for i in range(len(s))) >= 2


class TestGraphs:
    def test_euler(self):
        for _ in range(40):
            names = "ABCDE"[:R.randint(2, 5)]
            edges = [tuple(R.sample(names, 2)) for _ in range(R.randint(1, 8))]
            got = res(GM.run("euler_path", ", ".join(f"{u}-{v}" for u, v in edges)))
            verts = {x for e in edges for x in e}
            odd = sum(sum(v in e for e in edges) % 2 for v in verts)
            comp, st = {edges[0][0]}, [edges[0][0]]
            while st:
                x = st.pop()
                for u, v in edges:
                    y = v if u == x else u if v == x else None
                    if y is not None and y not in comp:
                        comp.add(y)
                        st.append(y)
            if odd not in (0, 2) or comp != verts:
                assert got is None
                continue
            assert len(got) == len(edges) + 1
            assert sorted(tuple(sorted(e)) for e in edges) == \
                sorted(tuple(sorted(p)) for p in zip(got, got[1:]))

    def test_dag(self):
        names = ["S", "A", "B", "C", "T"]
        for _ in range(40):
            edges = {}
            for _ in range(R.randint(1, 9)):
                i, j = sorted(R.sample(range(5), 2))
                edges[(names[i], names[j])] = R.randint(-5, 9)
            touched = {x for e in edges for x in e}
            if "S" not in touched:
                continue
            text = ", ".join(f"{u}>{v}:{w}" for (u, v), w in edges.items())
            paths = []

            def dfs(v, path, w):
                paths.append((w, path))
                for (a, b), c in edges.items():
                    if a == v:
                        dfs(b, path + [b], w + c)
            dfs("S", ["S"], 0)
            assert res(GM.run("longest_path_dag", text))[0] == max(w for w, _ in paths)
            if "T" in touched:
                assert res(GM.run("count_paths_dag", text)) == \
                    sum(1 for _, p in paths if p[-1] == "T")


class TestAlgebraGames:
    def test_algebra(self):
        fib = [0, 1]
        while len(fib) < 91:
            fib.append(fib[-1] + fib[-2])
        for n in range(91):
            assert res(AL.run("matrix_exponentiation", str(n))) == fib[n]
        for _ in range(30):
            k = R.randint(1, 11)
            vals = R.sample(range(1, 90), k)
            p = R.randint(0, k)
            a = sorted(vals[:p]) + [95] + sorted(vals[p:], reverse=True)
            assert res(AL.run("ternary_search", csv(a))) == 95
            b = [R.randint(-9, 9) for _ in range(R.randint(1, 8))]
            s = R.randint(-20, 30)
            want = sum(sum(c) <= s for k2 in range(len(b) + 1)
                       for c in itertools.combinations(b, k2))
            assert res(AL.run("meet_in_middle", csv(b), s)) == want

    def test_games(self):
        for _ in range(40):
            piles = [R.randint(0, 20) for _ in range(R.randint(1, 5))]
            out = res(GA.run("nim", csv(piles)))
            x = 0
            for p in piles:
                x ^= p
            assert out["first_wins"] == (x != 0)
            if x:
                i, new = out["move"]
                y = 0
                for p in piles[:i] + [new] + piles[i + 1:]:
                    y ^= p
                assert new < piles[i] and y == 0
            n, moves = R.randint(1, 20), sorted(R.sample(range(1, 6), R.randint(1, 3)))
            win = [False] * (n + 1)
            for i in range(1, n + 1):
                win[i] = any(m <= i and not win[i - m] for m in moves)
            g = res(GA.run("grundy_numbers", f"{n} | {csv(moves)}"))
            assert [v != 0 for v in g] == win
            coins = [R.randint(1, 20) for _ in range(R.randint(1, 8))]

            def best(i, j):
                if i > j:
                    return 0
                return max(coins[i] + sum(coins[i + 1:j + 1]) - best(i + 1, j),
                           coins[j] + sum(coins[i:j]) - best(i, j - 1))
            assert res(GA.run("optimal_game", csv(coins))) == best(0, len(coins) - 1)


class TestWiring:
    def test_every_id_through_api(self):
        samples = {
            "a_star_grid": "S./.G", "best_first_grid": "S./.G", "zero_one_bfs": "0,1/1,0",
            "max_flow": "S>A:3, A>T:2", "min_cut": "S>A:3, A>T:2",
            "bipartite_matching": "a: x", "lca_lifting": "1,2,3 | 2 3",
            "kth_ancestor": "1,2,3 | 2 1", "tsp_bitmask": "0,1/1,0",
            "assignment_bitmask": "1,2/3,4", "sparse_table": "3,1,2 | min 0 2",
            "sqrt_decomposition": "1,2,3 | sum 0 2",
            "lazy_segment_tree": "1,2 | add 0 1 1, sum 0 1", "extended_gcd": "12, 8",
            "mod_inverse": "3, 7", "ncr_mod": "5, 2", "euler_totient": "10",
            "crt": "1 2, 2 3", "suffix_array": "abab", "lcp_kasai": "abab",
            "longest_repeated_substring": "abab", "euler_path": "A-B",
            "longest_path_dag": "S>A:2", "count_paths_dag": "S>T",
            "matrix_exponentiation": "5", "ternary_search": "1,3,2", "nim": "1,2",
            "grundy_numbers": "5 | 1,2", "optimal_game": "3,9,1"}
        with_target = {"spf_sieve": ("12", 12), "meet_in_middle": ("1,2,3", 3)}
        every = set().union(*(m.TITLES for m in MODS))
        assert set(samples) | set(with_target) == every
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["meta"]["view"] == ("tree" if algo in LF.TITLES else "grid"), algo
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        for algo in every:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "a_star_grid", "text": "S./.."},
                  {"algorithm": "max_flow", "text": "A>B:3"},
                  {"algorithm": "bipartite_matching", "text": "a x"},
                  {"algorithm": "lca_lifting", "text": "1,2,3 | 2 9"},
                  {"algorithm": "tsp_bitmask", "text": "0,1,2/1,0,3"},
                  {"algorithm": "sparse_table", "text": "1,2 | min 1 0"},
                  {"algorithm": "extended_gcd", "text": "0, 0"},
                  {"algorithm": "spf_sieve", "text": "10", "target": 11},
                  {"algorithm": "crt", "text": "5 3, 1 4"},
                  {"algorithm": "suffix_array", "text": "a1"},
                  {"algorithm": "longest_path_dag", "text": "S>A, A>S"},
                  {"algorithm": "ternary_search", "text": "1,3,2,4"},
                  {"algorithm": "grundy_numbers", "text": "5"},
                  {"algorithm": "nim", "text": "70"}):
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_every_catalog_category_is_a_family(self):
        """Explore groups cards by ALGO_CATEGORIES; any other category would
        leave its algorithms invisible there."""
        data = (Path(__file__).resolve().parents[2] / "frontend/js/data.js").read_text()
        fams = set(re.search(r"ALGO_CATEGORIES = \[(.*?)\]", data).group(1)
                   .replace('"', "").replace(" ", "").split(","))
        cats = re.findall(r'^  \{ id: "[^"]+".*?category: "([^"]+)"', data, flags=re.M)
        assert cats and set(cats) <= fams, set(cats) - fams
