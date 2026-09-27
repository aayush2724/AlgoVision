"""Batches 50–54 — BST operations, heaps, string basics, sliding windows and
text-input graph problems (plus network delay on the drawn graph). Each
tracer is checked against a direct/brute-force reference on random input.
"""

import heapq
import itertools
import random
from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    bst_ops as B, heaps_more as H, strings_basic as S, window_more as W,
    graph_text as T, graph_directed as GD,
)
from app.tracers.common import Graph

client = TestClient(app)
R = random.Random(50)
res = lambda out: out["meta"]["result"]


def bst_path(vals, v):
    """Root-to-v path in the BST built by inserting `vals` in order."""
    left, right = {}, {}
    root = vals[0]
    for x in vals[1:]:
        cur = root
        while True:
            side = left if x < cur else right
            if cur not in side:
                side[cur] = x
                break
            cur = side[cur]
    path, cur = [], root
    while True:
        path.append(cur)
        if cur == v:
            return path
        cur = left[cur] if v < cur else right[cur]


class TestBST:
    def test_value_queries(self):
        for _ in range(80):
            vals = R.sample(range(1, 60), R.randint(1, 12))
            txt = ",".join(map(str, vals))
            s = sorted(vals)
            x = R.randint(0, 61)
            floors = [v for v in s if v <= x]
            ceils = [v for v in s if v >= x]
            assert res(B.run("floor_ceil_bst", f"{txt} | {x}")) == \
                [floors[-1] if floors else None, ceils[0] if ceils else None]
            below = [v for v in s if v < x]
            above = [v for v in s if v > x]
            assert res(B.run("successor_predecessor", f"{txt} | {x}")) == \
                [below[-1] if below else None, above[0] if above else None]
            k = R.randint(1, len(s))
            assert res(B.run("kth_bst", f"{txt} | {k}")) == [s[k - 1], s[-k]]
            t = R.randint(2, 120)
            assert res(B.run("two_sum_bst", f"{txt} | {t}")) is \
                any(a + b == t for a, b in itertools.combinations(s, 2))
            assert res(B.run("bst_from_preorder", txt)) == vals

    def test_lca(self):
        for _ in range(60):
            vals = R.sample(range(1, 60), R.randint(2, 12))
            a, b = R.sample(vals, 2)
            common = [x for x, y in zip(bst_path(vals, a), bst_path(vals, b)) if x == y]
            got = res(B.run("lca_bst", f"{','.join(map(str, vals))} | {a} {b}"))
            assert got == common[-1], (vals, a, b)

    def test_shape_checks(self):
        assert res(B.run("validate_bst", "2,1,3")) is True
        assert res(B.run("validate_bst", "5,1,4,null,null,3,6")) is False
        assert res(B.run("validate_bst", "5,4,6,null,null,3,7")) is False
        assert res(B.run("recover_bst", "3,1,4,null,null,2")) == [2, 3]
        assert res(B.run("recover_bst", "1,3,null,null,2")) == [1, 3]
        assert res(B.run("largest_bst", "10,5,15,1,8,null,7")) == 3
        assert res(B.run("largest_bst", "2,1,3")) == 3


class TestHeaps:
    def test_tree_heaps(self):
        for _ in range(60):
            a = [R.randint(0, 30) for _ in range(R.randint(1, 12))]
            txt = ",".join(map(str, a))
            is_min = all(a[i] <= a[c] for i in range(len(a)) for c in (2 * i + 1, 2 * i + 2)
                         if c < len(a))
            assert res(H.run("is_min_heap", txt)) is is_min
            mx = res(H.run("min_to_max_heap", txt))
            assert sorted(mx) == sorted(a) and all(
                mx[i] >= mx[c] for i in range(len(mx)) for c in (2 * i + 1, 2 * i + 2)
                if c < len(mx))
            sticks = [v + 1 for v in a]
            h, cost = sorted(sticks), 0
            while len(h) > 1:
                x, y = heapq.heappop(h), heapq.heappop(h)
                cost += x + y
                heapq.heappush(h, x + y)
            assert res(H.run("connect_sticks", ",".join(map(str, sticks)))) == cost

    def test_grid_heaps(self):
        for _ in range(60):
            a = [R.randint(1, 8) for _ in range(R.randint(1, 12))]
            txt = ",".join(map(str, a))
            rank = {v: i + 1 for i, v in enumerate(sorted(set(a)))}
            assert res(H.run("rank_replace", txt)) == [rank[v] for v in a]
            cnt = Counter(a)
            k = R.randint(1, len(cnt))
            want = sorted(cnt, key=lambda v: (-cnt[v], v))[:k]
            got = res(H.run("top_k_frequent", txt, k))
            assert sorted(cnt[v] for v in got) == sorted(cnt[v] for v in want)
            g = R.randint(1, len(a))
            c2, ok = Counter(a), len(a) % g == 0
            while ok and +c2:
                s0 = min(+c2)
                for v in range(s0, s0 + g):
                    if not c2[v]:
                        ok = False
                        break
                    c2[v] -= 1
                c2 = +c2
            assert res(H.run("hand_of_straights", txt, g)) is ok
            meds = [sorted(a[:i + 1]) for i in range(len(a))]
            want_med = [m[len(m) // 2] if len(m) % 2 else (m[len(m) // 2 - 1] + m[len(m) // 2]) / 2
                        for m in meds]
            assert res(H.run("median_stream", txt)) == want_med
        for tasks, n in (("A,A,A,B,B,B", 2), ("A,A,A,B,B,B", 0), ("A,A,A,A,B,C,D", 2)):
            cnt = Counter(tasks.split(","))
            m = max(cnt.values())
            want = max(len(tasks.split(",")),
                       (m - 1) * (n + 1) + sum(v == m for v in cnt.values()))
            assert res(H.run("task_scheduler", tasks, n)) == want


class TestStrings:
    def test_examples(self):
        cases = [("remove_outer_parens", "(()())(())", "()()()"),
                 ("reverse_words", "  hello   world ", "world hello"),
                 ("largest_odd_number", "4206", ""), ("largest_odd_number", "52", "5"),
                 ("longest_common_prefix", "dog,racecar,car", ""),
                 ("isomorphic_strings", "foo,bar", False),
                 ("isomorphic_strings", "paper,title", True),
                 ("rotate_string", "abcde,abced", False), ("max_nesting_depth", "(1)+((2))", 2),
                 ("roman_to_integer", "LVIII", 58), ("string_to_integer", "words 987", 0),
                 ("string_to_integer", "-91283472332", -2 ** 31)]
        for algo, text, want in cases:
            assert res(S.run(algo, text)) == want, (algo, text)

    def test_random(self):
        for _ in range(60):
            s = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
            cnt = Counter(s)
            got = res(S.run("sort_by_frequency", s))
            assert sorted(got) == sorted(s) and all(
                cnt[got[i]] >= cnt[got[i + 1]] for i in range(len(got) - 1))
            want = sum(max(Counter(s[i:j]).values()) - min(Counter(s[i:j]).values())
                       for i in range(len(s)) for j in range(i + 1, len(s) + 1))
            assert res(S.run("sum_of_beauty", s)) == want
            rot = s[len(s) // 2:] + s[:len(s) // 2]
            assert res(S.run("rotate_string", f"{s},{rot}")) is True


class TestWindows:
    def test_numeric(self):
        for _ in range(60):
            a = [R.randint(0, 3) for _ in range(R.randint(1, 12))]
            b = [v % 2 for v in a]
            subs = [(i, j) for i in range(len(a)) for j in range(i + 1, len(a) + 1)]
            g = R.randint(0, len(a))
            assert res(W.run("binary_subarray_sum", ",".join(map(str, b)), g)) == \
                sum(sum(b[i:j]) == g for i, j in subs)
            k = R.randint(0, len(a))
            assert res(W.run("nice_subarrays", ",".join(map(str, a)), k)) == \
                sum(sum(v % 2 for v in a[i:j]) == k for i, j in subs)
            kd = R.randint(1, len(a))
            assert res(W.run("subarrays_k_distinct", ",".join(map(str, a)), kd)) == \
                sum(len(set(a[i:j])) == kd for i, j in subs)
            kc = R.randint(1, len(a))
            assert res(W.run("max_card_points", ",".join(map(str, a)), kc)) == \
                max(sum(a[:l]) + sum(a[len(a) - (kc - l):]) for l in range(kc + 1))

    def test_strings(self):
        def is_sub(p, x):
            it = iter(x)
            return all(c in it for c in p)
        for _ in range(60):
            s = "".join(R.choice("abc") for _ in range(R.randint(1, 10)))
            n = len(s)
            spans = [(i, j) for i in range(n) for j in range(i + 1, n + 1)]
            assert res(W.run("substrings_all_three", s)) == \
                sum(set(s[i:j]) >= set("abc") for i, j in spans)
            k = R.randint(0, n)
            assert res(W.run("char_replacement", s, k)) == max(
                j - i for i, j in spans if (j - i) - max(Counter(s[i:j]).values()) <= k)
            t = "".join(R.choice("abc") for _ in range(R.randint(1, 3)))
            covers = [j - i for i, j in spans if not (Counter(t) - Counter(s[i:j]))]
            assert len(res(W.run("min_window_substring", f"{s},{t}"))) == min(covers, default=0)
            seq = sorted((j - i, i) for i, j in spans if is_sub(t, s[i:j]))
            want2 = s[seq[0][1]:seq[0][1] + seq[0][0]] if seq else ""
            assert res(W.run("min_window_subsequence", f"{s},{t}")) == want2


class TestGraphText:
    def test_examples(self):
        assert res(T.run("word_ladder", "hit,cog | hot,dot,dog,lot,log,cog")) == 5
        assert res(T.run("word_ladder", "hit,cog | hot,dot,dog,lot,log")) == 0
        assert len(res(T.run("word_ladder_ii", "hit,cog | hot,dot,dog,lot,log,cog"))) == 2
        order = res(T.run("alien_dictionary", "baa,abcd,abca,cab,cad"))
        assert order.index("b") < order.index("d") < order.index("a") < order.index("c")
        assert res(T.run("cheapest_flight_k",
                         "0>1:100,1>2:100,2>0:100,1>3:600,2>3:200 | 0 3 1")) == 700
        assert res(T.run("cheapest_flight_k", "0>1:100,1>2:100,0>2:500 | 0 2 0")) == 500
        assert res(T.run("ways_to_arrive",
                         "0-6:7,0-1:2,1-2:3,1-3:3,6-3:3,3-5:1,6-5:1,2-5:1,0-4:5,4-6:2 | 0 6")) == 4
        assert res(T.run("min_multiplications", "3 30 | 2,5,7")) == 2
        assert res(T.run("min_multiplications", "7 66175 | 3,4,65")) == 4
        assert res(T.run("most_stones", "0:0,0:1,1:0,1:2,2:1,2:2")) == 5

    def test_network_delay(self):
        for _ in range(40):
            ids = [str(i) for i in range(1, R.randint(2, 6) + 1)]
            edges = [[a, b, R.randint(1, 9)] for a, b in itertools.permutations(ids, 2)
                     if R.random() < 0.4]
            g = Graph(nodes=[{"id": x} for x in ids], edges=edges)
            d = {x: None for x in ids}
            d[ids[0]] = 0
            for _ in ids:
                for a, b, w in edges:
                    if d[a] is not None and (d[b] is None or d[a] + w < d[b]):
                        d[b] = d[a] + w
            want = -1 if None in d.values() else max(d.values())
            assert res(GD.trace_for("network_delay")(g, ids[0])) == want


class TestEndpoints:
    def test_every_text_id_runs(self):
        samples = {
            "floor_ceil_bst": "5,3,8 | 4", "kth_bst": "5,3,8 | 1", "lca_bst": "5,3,8 | 3 8",
            "successor_predecessor": "5,3,8 | 5", "two_sum_bst": "5,3,8 | 8",
            "bst_from_preorder": "5,3,8", "validate_bst": "2,1,3",
            "recover_bst": "3,1,4,null,null,2", "largest_bst": "2,1,3",
            "is_min_heap": "1,2,3", "min_to_max_heap": "1,2,3", "connect_sticks": "2,4,3",
            "rank_replace": "4,1", "median_stream": "5,1", "remove_outer_parens": "(())",
            "reverse_words": "a b", "largest_odd_number": "123",
            "longest_common_prefix": "ab,ac", "isomorphic_strings": "ab,cd",
            "rotate_string": "ab,ba", "sort_by_frequency": "aab", "max_nesting_depth": "(())",
            "roman_to_integer": "IV", "string_to_integer": "42", "sum_of_beauty": "abc",
            "substrings_all_three": "abc", "min_window_substring": "abc,b",
            "min_window_subsequence": "abc,ac", "word_ladder": "hit,hot | hot",
            "word_ladder_ii": "hit,hot | hot", "alien_dictionary": "ab,b",
            "cheapest_flight_k": "A>B:1 | A B 0", "ways_to_arrive": "A-B:1 | A B",
            "min_multiplications": "2 4 | 2", "most_stones": "0:0,0:1",
        }
        with_target = {"top_k_frequent": ("1,1,2", 1), "hand_of_straights": ("1,2", 2),
                       "task_scheduler": ("A,B", 1), "char_replacement": ("AB", 1),
                       "binary_subarray_sum": ("1,0", 1), "nice_subarrays": ("1,2", 1),
                       "max_card_points": ("1,2,3", 1), "subarrays_k_distinct": ("1,2", 1)}
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        g = {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [["A", "B", 2]]}
        assert client.post("/api/trace", json={"algorithm": "network_delay", "graph": g,
                                               "start": "A"}).status_code == 200
        for mod in (B, H, S, W, T):
            for algo in mod.TITLES:
                body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
                assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "kth_bst", "text": "5,3 | 9"},
                  {"algorithm": "lca_bst", "text": "5,3 | 3 99"},
                  {"algorithm": "floor_ceil_bst", "text": "5,5 | 1"},
                  {"algorithm": "remove_outer_parens", "text": "(()"},
                  {"algorithm": "task_scheduler", "text": "AB,C", "target": 1},
                  {"algorithm": "word_ladder", "text": "hit,cog"},
                  {"algorithm": "cheapest_flight_k", "text": "A>B:1 | A B 9"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
