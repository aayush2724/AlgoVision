"""Batches 40–44 — level-order binary trees (traversals, views, checks) and
more table DP (grid DP, string DP). Trees are checked against small
independent recursive references on random shapes; DP against brute force.
"""

import itertools
import random
import re
from collections import deque

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    tree_traverse_more as TT, tree_views as TV, tree_checks as TC,
    dp_more as DM, dp_strings as DS, bt_common as bt,
)

client = TestClient(app)
R = random.Random(40)


# ── independent tree reference: nested tuples (val, left, right) ──
def rand_tree(depth=0, lo=-5, hi=9):
    if depth > 3 or (depth and R.random() < 0.3):
        return None
    return (R.randint(lo, hi), rand_tree(depth + 1, lo, hi), rand_tree(depth + 1, lo, hi))


def to_level(t):
    out, q = [], deque([t])
    while q:
        n = q.popleft()
        out.append(None if n is None else n[0])
        if n is not None:
            q.extend([n[1], n[2]])
    while out and out[-1] is None:
        out.pop()
    return ",".join("null" if v is None else str(v) for v in out)


def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def height(t): return 0 if t is None else 1 + max(height(t[1]), height(t[2]))


def levels(t):
    res, q = [], [t]
    while q:
        res.append([n[0] for n in q])
        q = [c for n in q for c in (n[1], n[2]) if c is not None]
    return res


def trees(n=60):
    out = []
    while len(out) < n:
        t = rand_tree()
        if t is not None and len(pre(t)) <= bt.MAX_NODES:
            out.append(t)
    return out


class TestTrees:
    def test_traversals(self):
        for t in trees():
            s = to_level(t)
            assert TT.run("iter_preorder", s)["meta"]["result"] == pre(t)
            assert TT.run("iter_inorder", s)["meta"]["result"] == ino(t)
            assert TT.run("postorder_two_stacks", s)["meta"]["result"] == post(t)
            assert TT.run("postorder_one_stack", s)["meta"]["result"] == post(t)
            want = [lv if i % 2 == 0 else lv[::-1] for i, lv in enumerate(levels(t))]
            assert TT.run("zigzag_traversal", s)["meta"]["result"] == want

    def test_views(self):
        for t in trees():
            s = to_level(t)
            lv = levels(t)
            assert TV.run("right_view", s)["meta"]["result"] == [l[-1] for l in lv]
            assert TV.run("right_view", s)["meta"]["left"] == [l[0] for l in lv]
            cells, q, k = [], deque([(t, 0, 0)]), 0
            while q:
                n, hd, d = q.popleft()
                cells.append((hd, d, k, n[0]))
                k += 1
                if n[1]:
                    q.append((n[1], hd - 1, d + 1))
                if n[2]:
                    q.append((n[2], hd + 1, d + 1))
            hds = sorted({c[0] for c in cells})
            top = [min((c for c in cells if c[0] == h), key=lambda c: c[2])[3] for h in hds]
            bottom = [max((c for c in cells if c[0] == h), key=lambda c: c[2])[3] for h in hds]
            vert = [[c[3] for c in sorted((c for c in cells if c[0] == h),
                                          key=lambda c: (c[1], c[3]))] for h in hds]
            assert TV.run("top_view", s)["meta"]["result"] == top
            assert TV.run("bottom_view", s)["meta"]["result"] == bottom
            assert TV.run("vertical_order", s)["meta"]["result"] == vert

    def test_max_width_and_boundary_examples(self):
        assert TV.run("max_width", "1,3,2,5,3,null,9")["meta"]["result"] == 4
        assert TV.run("max_width", "1,3,2,5,null,null,9,6,null,7")["meta"]["result"] == 7
        assert TV.run("boundary_traversal", "1,2,3,4,5,6,7,null,null,8,9")["meta"]["result"] \
            == [1, 2, 4, 8, 9, 6, 7, 3]

    def test_checks(self):
        def balanced(t):
            return t is None or (abs(height(t[1]) - height(t[2])) <= 1
                                 and balanced(t[1]) and balanced(t[2]))

        def mirror(a, b):
            if a is None or b is None:
                return a is b
            return a[0] == b[0] and mirror(a[1], b[2]) and mirror(a[2], b[1])

        def paths(t):
            if t[1] is None and t[2] is None:
                return [[t[0]]]
            return [[t[0]] + p for c in (t[1], t[2]) if c for p in paths(c)]

        def best_path(t):
            best = [None]

            def g(n):
                if n is None:
                    return 0
                l, r = max(0, g(n[1])), max(0, g(n[2]))
                cand = n[0] + l + r
                best[0] = cand if best[0] is None else max(best[0], cand)
                return n[0] + max(l, r)
            g(t)
            return best[0]

        for t in trees(80):
            s = to_level(t)
            assert TC.run("balanced_tree", s)["meta"]["result"] is balanced(t)
            assert TC.run("symmetric_tree", s)["meta"]["result"] is mirror(t[1], t[2])
            assert TC.run("max_path_sum", s)["meta"]["result"] == best_path(t)
            assert TC.run("root_to_leaf_paths", s)["meta"]["result"] == paths(t)

    def test_children_sum_holds_after(self):
        for t in trees(40):
            out = TC.run("children_sum", to_level(t))
            final = out["steps"][-1]["structures"]["tree"]
            by = {n["id"]: n for n in final}
            for n in final:
                kids = [by[c]["value"] for c in (n["left"], n["right"]) if c is not None]
                if kids:
                    assert n["value"] == sum(kids)

    def test_distance_burn_count(self):
        s = "3,5,1,6,2,0,8,null,null,7,4"
        assert TC.run("nodes_at_distance_k", s + " | 5 2")["meta"]["result"] == [1, 4, 7]
        assert TC.run("nodes_at_distance_k", s + " | 5 0")["meta"]["result"] == [5]
        assert TC.run("burn_tree", "1,2,3,4,null,5,6,null,7 | 2")["meta"]["result"] == 3
        for n in range(1, 16):
            full = ",".join(str(i) for i in range(1, n + 1))
            assert TC.run("count_complete_nodes", full)["meta"]["result"] == n

    def test_tree_validation(self):
        for algo, text in (("iter_preorder", "null,1"), ("iter_preorder", "1,a"),
                           ("burn_tree", "1,2,3"), ("burn_tree", "1,2,3 | 9"),
                           ("nodes_at_distance_k", "1,2 | 1"),
                           ("count_complete_nodes", "1,2,3,null,4"),
                           ("iter_inorder", ",".join(["1"] * 16))):
            mod = TT if algo in TT.TITLES else TC
            try:
                mod.run(algo, text)
            except ValueError:
                continue
            raise AssertionError((algo, text))


class TestDP:
    def test_frog_k(self):
        for _ in range(60):
            h = [R.randint(0, 50) for _ in range(R.randint(2, 8))]
            k = R.randint(1, len(h) - 1)
            best = {0: 0}
            for i in range(1, len(h)):
                best[i] = min(best[i - j] + abs(h[i] - h[i - j])
                              for j in range(1, k + 1) if i - j >= 0)
            got = DM.run("frog_jump_k", ",".join(map(str, h)), k)["meta"]["result"]
            assert got == best[len(h) - 1]

    def test_ninja_falling_triangle(self):
        for _ in range(40):
            days = [[R.randint(0, 20) for _ in range(3)] for _ in range(R.randint(1, 4))]
            want = max(sum(days[d][t] for d, t in enumerate(seq))
                       for seq in itertools.product(range(3), repeat=len(days))
                       if all(a != b for a, b in zip(seq, seq[1:])))
            txt = "/".join(",".join(map(str, r)) for r in days)
            assert DM.run("ninja_training", txt)["meta"]["result"] == want
            n = R.randint(1, 4)
            a = [[R.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            want = min(sum(a[r][c] for r, c in enumerate(cols))
                       for cols in itertools.product(range(n), repeat=n)
                       if all(abs(x - y) <= 1 for x, y in zip(cols, cols[1:])))
            txt = "/".join(",".join(map(str, r)) for r in a)
            assert DM.run("min_falling_path", txt)["meta"]["result"] == want
            tri = [[R.randint(-9, 9) for _ in range(i + 1)] for i in range(R.randint(1, 5))]
            want = min(sum(tri[r][c] for r, c in enumerate(cols))
                       for cols in itertools.product(range(len(tri)), repeat=len(tri))
                       if cols[0] == 0 and all(y - x in (0, 1) for x, y in zip(cols, cols[1:])))
            txt = "/".join(",".join(map(str, r)) for r in tri)
            assert DM.run("triangle_path", txt)["meta"]["result"] == want

    def test_subsets_and_knapsack(self):
        for _ in range(60):
            a = [R.randint(1, 6) for _ in range(R.randint(1, 6))]
            txt = ",".join(map(str, a))
            subs = [c for r in range(len(a) + 1) for c in itertools.combinations(a, r)]
            if sum(a) <= 24:
                assert DM.run("partition_equal_subset", txt)["meta"]["result"] is \
                    (sum(a) % 2 == 0 and any(sum(c) == sum(a) // 2 for c in subs))
            k = R.randint(0, 12)
            assert DM.run("count_subsets_sum_k", txt, k)["meta"]["result"] == \
                sum(1 for c in subs if sum(c) == k)
            items = [(R.randint(1, 5), R.randint(1, 20)) for _ in range(R.randint(1, 3))]
            cap = R.randint(1, 12)
            best = [0] * (cap + 1)
            for c in range(1, cap + 1):
                best[c] = max([best[c - w] + v for w, v in items if w <= c] + [0])
            txt = ",".join(f"{w}:{v}" for w, v in items)
            assert DM.run("unbounded_knapsack", txt, cap)["meta"]["result"] == best[cap]
        assert DM.run("rod_cutting", "1,5,8,9,10,17,17,20")["meta"]["result"] == 22


def _lcs_len(a, b):
    for r in range(min(len(a), len(b)), -1, -1):
        subs = {"".join(c) for c in itertools.combinations(a, r)}
        if any("".join(c) in subs for c in itertools.combinations(b, r)):
            return r


def _is_subseq(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


class TestStringDP:
    def test_lcs_family(self):
        for _ in range(60):
            a = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            b = "".join(R.choice("abc") for _ in range(R.randint(1, 6)))
            k = _lcs_len(a, b)
            lcs = DS.run("print_lcs", f"{a},{b}")["meta"]["result"]
            assert len(lcs) == k and _is_subseq(lcs, a) and _is_subseq(lcs, b)
            scs = DS.run("shortest_supersequence", f"{a},{b}")["meta"]["result"]
            assert len(scs) == len(a) + len(b) - k and _is_subseq(a, scs) and _is_subseq(b, scs)
            assert DS.run("min_ins_del", f"{a},{b}")["meta"]["result"] == \
                {"deletions": len(a) - k, "insertions": len(b) - k}
            lps = _lcs_len(a, a[::-1])
            assert DS.run("longest_palindromic_subseq", a)["meta"]["result"] == lps
            assert DS.run("min_insert_palindrome", a)["meta"]["result"] == len(a) - lps

    def test_distinct_and_wildcard(self):
        for _ in range(80):
            a = "".join(R.choice("ab") for _ in range(R.randint(1, 7)))
            b = "".join(R.choice("ab") for _ in range(R.randint(1, 3)))
            want = sum(1 for c in itertools.combinations(range(len(a)), len(b))
                       if "".join(a[i] for i in c) == b)
            assert DS.run("distinct_subsequences", f"{a},{b}")["meta"]["result"] == want
            p = "".join(R.choice("ab?*") for _ in range(R.randint(1, 5)))
            rx = "".join(".*" if c == "*" else "." if c == "?" else c for c in p)
            assert DS.run("wildcard_match", f"{a},{p}")["meta"]["result"] is \
                bool(re.fullmatch(rx, a)), (a, p)


class TestEndpoints:
    def test_every_id_runs_with_a_sample(self):
        samples = {
            **{k: ("1,2,3,4,5,6,7", None) for k in list(TT.TITLES) + list(TV.TITLES)},
            **{k: ("1,2,3,4,5,6,7", None) for k in ("balanced_tree", "symmetric_tree",
                                                     "max_path_sum", "root_to_leaf_paths",
                                                     "children_sum", "count_complete_nodes")},
            "nodes_at_distance_k": ("1,2,3,4,5 | 2 1", None),
            "burn_tree": ("1,2,3,4,5 | 4", None),
            "frog_jump_k": ("30,10,60,10", 2), "ninja_training": ("1,2,3/4,5,6", None),
            "min_falling_path": ("1,2/3,4", None), "triangle_path": ("2/3,4", None),
            "partition_equal_subset": ("1,5,11,5", None), "count_subsets_sum_k": ("1,2,3", 3),
            "unbounded_knapsack": ("2:5,4:11", 6), "rod_cutting": ("1,5,8", None),
            **{k: ("abc,abd", None) for k in DS.TITLES if k not in DS.ONE_WORD},
            **{k: ("abca", None) for k in DS.ONE_WORD},
        }
        for mod in (TT, TV, TC, DM, DS):
            for algo in mod.TITLES:
                text, t = samples[algo]
                r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
                assert r.status_code == 200, (algo, r.text)
                body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
                assert body["algorithm"] == algo, algo

    def test_bad_input_is_400(self):
        for p in ({"algorithm": "iter_preorder", "text": "null"},
                  {"algorithm": "burn_tree", "text": "1,2,3"},
                  {"algorithm": "frog_jump_k", "text": "1,2,3"},
                  {"algorithm": "triangle_path", "text": "1/2,3,4"},
                  {"algorithm": "wildcard_match", "text": "abc"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
