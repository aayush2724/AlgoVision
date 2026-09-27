"""Batch 29 — linked-list stragglers (Step 6): palindrome check, odd/even
segregation, rotate right by k, delete the middle node. Each is checked
against the equivalent Python list operation; the palindrome check must also
leave the list's arrows exactly as it found them.
"""

import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import ll_palindrome, odd_even_list, rotate_list, delete_middle

client = TestClient(app)


def _rand_lists(seed, count=40, lo=1, hi=10, vals=3):
    rng = random.Random(seed)
    return [[rng.randint(0, vals) for _ in range(rng.randint(lo, hi))]
            for _ in range(count)]


class TestLinkedLists:
    def test_palindrome(self):
        cases = [[1, 2, 3, 2, 1], [1, 2, 2, 1], [1, 2], [7], [1, 2, 3]]
        cases += _rand_lists(43, vals=1)
        for c in cases:
            out = ll_palindrome.trace(c)
            assert out["meta"]["result"] is (c == c[::-1]), c
            final_next = out["steps"][-1]["structures"]["next"]
            assert final_next == [i + 1 if i < len(c) - 1 else None
                                  for i in range(len(c))], c

    def test_odd_even(self):
        for c in [[1, 2, 3, 4, 5], [2, 1, 3, 5, 6, 4, 7], [1], [1, 2]] + _rand_lists(44):
            assert odd_even_list.trace(c)["meta"]["result"] == c[0::2] + c[1::2], c

    def test_rotate(self):
        for c in [[1, 2, 3, 4, 5], [0, 1, 2], [9]] + _rand_lists(56, count=15):
            for k in range(0, 2 * len(c) + 2):
                e = k % len(c)
                want = c[-e:] + c[:-e] if e else c
                assert rotate_list.trace(c, k)["meta"]["result"] == want, (c, k)

    def test_delete_middle(self):
        for n in range(1, 11):
            c = list(range(n))
            meta = delete_middle.trace(c)["meta"]
            assert meta["result"] == c[:n // 2] + c[n // 2 + 1:], n
            assert meta["removed"] == n // 2


class TestEndpoints:
    def test_endpoints_ok(self):
        payloads = [
            ("ll_palindrome", {"array": [1, 2, 3, 2, 1]}),
            ("odd_even_list", {"array": [1, 2, 3, 4]}),
            ("rotate_list", {"array": [1, 2, 3], "target": 4}),
            ("delete_middle", {"array": [1, 3, 4, 7]}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        bad = [
            {"algorithm": "ll_palindrome", "array": []},
            {"algorithm": "odd_even_list", "array": list(range(11))},
            {"algorithm": "rotate_list", "array": [1, 2]},
            {"algorithm": "rotate_list", "array": [1, 2], "target": 101},
            {"algorithm": "rotate_list", "array": [1, 2], "target": 1.5},
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for algo in ("ll_palindrome", "odd_even_list", "rotate_list", "delete_middle"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
