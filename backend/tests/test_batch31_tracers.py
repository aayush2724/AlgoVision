"""Batch 31 — recursion trees (Step 7): subsets (power set, subset sums,
subsequences with sum K), generate parentheses, binary strings without
consecutive 1s, combination sum. Results are checked against itertools /
direct references, and every step's tree must be well-formed (children point
at revealed nodes, one level deeper, and marked leaves are real answers).
"""

import itertools

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    subsets_recursion, generate_parentheses, binary_strings, combination_sum,
)

client = TestClient(app)


def _well_formed(out):
    for step in out["steps"]:
        st = step["structures"]
        by_id = {n["id"]: n for n in st["tree"]}
        for n in st["tree"]:
            assert 0 <= n["x"] <= 1
            for side in ("left", "right"):
                cid = n[side]
                if cid in by_id:
                    assert by_id[cid]["depth"] == n["depth"] + 1
        assert set(st["marked"]) <= set(by_id)


def _balanced(s):
    bal = 0
    for ch in s:
        bal += 1 if ch == "(" else -1
        if bal < 0:
            return False
    return bal == 0


class TestRecursionTrees:
    def test_subsets_power_set(self):
        for arr in ([1, 2, 3], [5], [1, 2, 3, 4], [2, 2]):
            out = subsets_recursion.trace(arr)
            _well_formed(out)
            want = sorted(sorted(c) for r in range(len(arr) + 1)
                          for c in itertools.combinations(arr, r))
            assert sorted(sorted(s) for s in out["meta"]["result"]) == want
            assert sorted(out["meta"]["sums"]) == sorted(sum(s) for s in want)

    def test_subsets_sum_k(self):
        arr = [1, 2, 3, 4]
        for k in range(0, 12):
            out = subsets_recursion.trace(arr, k)
            want = sum(1 for r in range(5) for c in itertools.combinations(arr, r)
                       if sum(c) == k)
            assert out["meta"]["matches"] == want, k
            assert len(out["steps"][-1]["structures"]["marked"]) == want

    def test_parentheses(self):
        catalan = {1: 1, 2: 2, 3: 5}
        for n in (1, 2, 3):
            out = generate_parentheses.trace(n)
            _well_formed(out)
            res = out["meta"]["result"]
            assert len(res) == len(set(res)) == catalan[n]
            assert all(len(s) == 2 * n and _balanced(s) for s in res)

    def test_binary_strings(self):
        for n in (1, 2, 3, 4):
            out = binary_strings.trace(n)
            _well_formed(out)
            want = sorted("".join(b) for b in itertools.product("01", repeat=n)
                          if "11" not in "".join(b))
            assert sorted(out["meta"]["result"]) == want

    def test_combination_sum(self):
        cases = [([2, 3, 6, 7], 7), ([2, 3, 5], 8), ([2], 1), ([3, 4], 12)]
        for cands, t in cases:
            out = combination_sum.trace(cands, t)
            _well_formed(out)
            want = set()
            for r in range(1, t + 1):
                for combo in itertools.combinations_with_replacement(sorted(cands), r):
                    if sum(combo) == t:
                        want.add(combo)
            got = [tuple(c) for c in out["meta"]["result"]]
            assert len(got) == len(set(got)) and set(got) == want, (cands, t)

    def test_tree_size_matches_trace(self):
        for cands, t in (([2, 3, 6, 7], 7), ([2, 3, 5], 8)):
            nodes = len(combination_sum.trace(cands, t)["steps"][-1]["structures"]["tree"])
            assert combination_sum.tree_size(cands, t) == nodes


class TestEndpoints:
    def test_endpoints_ok(self):
        payloads = [
            ("subsets_recursion", {"array": [1, 2, 3]}),
            ("subsets_recursion", {"array": [1, 2, 3], "target": 3}),
            ("generate_parentheses", {"target": 3}),
            ("binary_strings", {"target": 4}),
            ("combination_sum", {"array": [2, 3, 6, 7], "target": 7}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)

    def test_validation(self):
        bad = [
            {"algorithm": "subsets_recursion", "array": [1, 2, 3, 4, 5]},
            {"algorithm": "subsets_recursion", "array": [10]},
            {"algorithm": "generate_parentheses", "target": 4},
            {"algorithm": "binary_strings"},
            {"algorithm": "combination_sum", "array": [1, 2], "target": 12},  # tree too big
            {"algorithm": "combination_sum", "array": [2, 2], "target": 4},   # duplicates
            {"algorithm": "combination_sum", "array": [2, 3], "target": 13},
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for algo in ("subsets_recursion", "generate_parentheses",
                     "binary_strings", "combination_sum"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
