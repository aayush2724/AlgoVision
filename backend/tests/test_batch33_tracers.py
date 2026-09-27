"""Batch 33 — loop-style recursion trees (Step 7): Subsets II, Combination
Sum II and III, palindrome partitioning, letter combinations. Each result is
checked against an itertools brute force, and every step's n-ary tree must be
well-formed (children revealed, one level deeper, marked nodes real).
"""

import itertools
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    subsets_ii, combination_sum_ii, combination_sum_iii, palindrome_partition,
    letter_combinations,
)

client = TestClient(app)


def _well_formed(out):
    for step in out["steps"]:
        st = step["structures"]
        by_id = {n["id"]: n for n in st["tree"]}
        for n in st["tree"]:
            for cid in n["children"]:
                assert cid in by_id and by_id[cid]["depth"] == n["depth"] + 1
        assert set(st["marked"]) <= set(by_id)


def _partitions(s):
    if not s:
        yield []
        return
    for i in range(1, len(s) + 1):
        if s[:i] == s[:i][::-1]:
            for rest in _partitions(s[i:]):
                yield [s[:i]] + rest


class TestLoopRecursion:
    def test_subsets_ii(self):
        rng = random.Random(32)
        cases = [[1, 2, 2], [2, 2, 2], [4, 4, 1, 4], [0]] + [
            [rng.randint(0, 2) for _ in range(rng.randint(1, 4))] for _ in range(30)]
        for arr in cases:
            out = subsets_ii.trace(arr)
            _well_formed(out)
            got = [tuple(s) for s in out["meta"]["result"]]
            want = {tuple(sorted(c)) for r in range(len(arr) + 1)
                    for c in itertools.combinations(arr, r)}
            assert len(got) == len(set(got)) and set(got) == want, arr

    def test_combination_sum_ii(self):
        rng = random.Random(12)
        cases = [([1, 1, 2, 5, 6, 7], 8), ([2, 5, 2, 1, 2], 5)] + [
            ([rng.randint(1, 5) for _ in range(rng.randint(1, 6))], rng.randint(1, 10))
            for _ in range(40)]
        for arr, t in cases:
            out = combination_sum_ii.trace(arr, t)
            _well_formed(out)
            got = [tuple(c) for c in out["meta"]["result"]]
            want = {tuple(sorted(c)) for r in range(1, len(arr) + 1)
                    for c in itertools.combinations(arr, r) if sum(c) == t}
            assert len(got) == len(set(got)) and set(got) == want, (arr, t)

    def test_combination_sum_iii(self):
        for k in range(1, 5):
            for n in range(1, 25):
                out = combination_sum_iii.trace(k, n)
                want = sorted(list(c) for c in itertools.combinations(range(1, 10), k)
                              if sum(c) == n)
                assert sorted(out["meta"]["result"]) == want, (k, n)

    def test_palindrome_partition(self):
        for s in ("aab", "aabb", "abc", "a", "raceca", "abba"):
            out = palindrome_partition.trace(s)
            _well_formed(out)
            assert sorted(out["meta"]["result"]) == sorted(_partitions(s)), s

    def test_letter_combinations(self):
        pad = letter_combinations.KEYPAD
        for d in ("2", "23", "79", "9"):
            out = letter_combinations.trace(d)
            _well_formed(out)
            want = ["".join(p) for p in itertools.product(*(pad[c] for c in d))]
            assert out["meta"]["result"] == want


class TestEndpoints:
    def test_endpoints_ok(self):
        payloads = [
            ("subsets_ii", {"array": [1, 2, 2]}),
            ("combination_sum_ii", {"array": [1, 1, 2, 5, 6, 7], "target": 8}),
            ("combination_sum_iii", {"array": [3, 9]}),
            ("palindrome_partition", {"text": "aabb"}),
            ("letter_combinations", {"text": "23"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)

    def test_validation(self):
        bad = [
            {"algorithm": "subsets_ii", "array": [1, 2, 3, 4, 5]},
            {"algorithm": "combination_sum_ii", "array": [1, 2]},            # no target
            {"algorithm": "combination_sum_iii", "array": [4, 20]},          # tree too big
            {"algorithm": "combination_sum_iii", "array": [3]},
            {"algorithm": "palindrome_partition", "text": "aaaaaa"},         # 64 calls
            {"algorithm": "palindrome_partition", "text": "ab1"},
            {"algorithm": "letter_combinations", "text": "123"},
            {"algorithm": "letter_combinations", "text": "1"},
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for algo in ("subsets_ii", "combination_sum_ii", "combination_sum_iii",
                     "palindrome_partition", "letter_combinations"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
