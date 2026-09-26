"""Batch 25 — Arrays & Binary Search (Steps 3-4): search in rotated sorted
array, Dutch national flag (sort 0/1/2), majority element (Boyer-Moore), and
next permutation. Each is checked against an independent reference.
"""

import itertools

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    search_rotated, dutch_flag, majority_element, next_permutation,
)

client = TestClient(app)


def _ref_next_perm(a):
    """Python's own next-permutation via itertools over a rotation of perms."""
    perms = sorted(set(itertools.permutations(a)))
    idx = perms.index(tuple(a))
    return list(perms[(idx + 1) % len(perms)])


class TestArrayTracers:
    def test_search_rotated_found(self):
        base = [4, 5, 6, 7, 0, 1, 2]
        for t in base:
            out = search_rotated.trace(base, t)["steps"][-1]["structures"]
            assert out["found"] is True, t

    def test_search_rotated_absent(self):
        base = [4, 5, 6, 7, 0, 1, 2]
        for t in (3, 8, -1, 100):
            out = search_rotated.trace(base, t)["steps"][-1]["structures"]
            assert out["found"] is False, t

    def test_search_rotated_all_rotations(self):
        vals = [0, 1, 2, 4, 5, 6, 7]
        for r in range(len(vals)):
            rot = vals[r:] + vals[:r]
            for t in vals + [99]:
                res = search_rotated.trace(rot, t)["steps"][-1]["structures"]["found"]
                assert res is (t in rot), (rot, t)

    def test_dutch_flag(self):
        cases = [[2, 0, 2, 1, 1, 0], [0, 1, 2], [2, 2, 1, 1, 0, 0], [1], [0, 0, 0]]
        for c in cases:
            assert dutch_flag.trace(c)["meta"]["result"] == sorted(c), c

    def test_dutch_flag_is_permutation(self):
        c = [2, 0, 2, 1, 1, 0, 2, 1, 0]
        out = dutch_flag.trace(c)["meta"]["result"]
        assert sorted(out) == sorted(c)

    def test_majority_present(self):
        for a, want in ([[2, 2, 1, 1, 1, 2, 2], 2], [[3, 3, 4], 3], [[1], 1],
                        [[5, 5, 5, 1, 2], 5]):
            assert majority_element.trace(a)["meta"]["majority"] == want, a

    def test_majority_absent(self):
        for a in ([1, 2, 3, 4], [1, 1, 2, 2], []):
            assert majority_element.trace(a)["meta"]["majority"] is None, a

    def test_next_permutation(self):
        cases = [[1, 2, 3], [1, 3, 2], [3, 2, 1], [1, 1, 5], [2, 3, 1],
                 [1, 5, 8, 4, 7, 6, 5, 3, 1]]
        for c in cases:
            assert next_permutation.trace(c)["meta"]["result"] == _ref_next_perm(c), c


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"search_rotated", "dutch_flag", "majority_element",
                "next_permutation"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("search_rotated", {"array": [4, 5, 6, 7, 0, 1, 2], "target": 0}),
            ("dutch_flag", {"array": [2, 0, 2, 1, 1, 0]}),
            ("majority_element", {"array": [2, 2, 1, 1, 1, 2, 2]}),
            ("next_permutation", {"array": [1, 2, 3]}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        assert client.post("/api/trace", json={"algorithm": "search_rotated", "array": [1, 2]}).status_code == 400  # no target
        assert client.post("/api/trace", json={"algorithm": "dutch_flag", "array": [0, 1, 3]}).status_code == 400  # not 0/1/2
        assert client.post("/api/trace", json={"algorithm": "majority_element", "array": []}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "next_permutation", "array": list(range(20))}).status_code == 400

    def test_detect_resolves(self):
        for algo in ("search_rotated", "dutch_flag", "majority_element",
                     "next_permutation"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
