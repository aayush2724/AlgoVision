"""Batch 27 — more Stack & Binary Search (Steps 4, 9): trapping rainwater,
asteroid collision, minimum in a rotated sorted array (= rotation count), and
find peak element. Each is checked against an independent brute force.
"""

import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    trapping_rainwater, asteroid_collision, find_min_rotated, find_peak,
)

client = TestClient(app)


def _ref_water(h):
    return sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i])
               for i in range(len(h)))


def _ref_asteroids(a):
    """Simulate literally: repeatedly resolve the first adjacent → ← pair."""
    a = list(a)
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] > 0 > a[i + 1]:
                x, y = a[i], -a[i + 1]
                a[i:i + 2] = [] if x == y else ([a[i]] if x > y else [a[i + 1]])
                changed = True
                break
    return a


class TestStackTracers:
    def test_trapping_rainwater(self):
        cases = [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], [4, 2, 0, 3, 2, 5],
                 [1], [3, 0, 3], [1, 2, 3], [0, 0]]
        rng = random.Random(17)
        cases += [[rng.randint(0, 6) for _ in range(rng.randint(1, 16))]
                  for _ in range(80)]
        for c in cases:
            meta = trapping_rainwater.trace(c)["meta"]
            assert meta["result"] == _ref_water(c), c
            assert sum(meta["water"]) == meta["result"]

    def test_asteroid_collision(self):
        cases = [[5, 10, -5], [8, -8], [10, 2, -5], [-2, -1, 1, 2],
                 [5, 10, -5, 8, -8, 2, -12]]
        rng = random.Random(19)
        cases += [[rng.choice([-1, 1]) * rng.randint(1, 5)
                   for _ in range(rng.randint(1, 16))] for _ in range(80)]
        for c in cases:
            assert asteroid_collision.trace(c)["meta"]["result"] == \
                _ref_asteroids(c), c


class TestBinarySearchTracers:
    def test_find_min_all_rotations(self):
        base = [0, 1, 2, 4, 5, 6, 7]
        for k in range(len(base)):
            rot = base[-k:] + base[:-k] if k else base[:]
            meta = find_min_rotated.trace(rot)["meta"]
            assert meta["result"] == 0 and meta["rotations"] == k, rot

    def test_find_min_is_logarithmic(self):
        rot = list(range(9, 16)) + list(range(9))
        steps = find_min_rotated.trace(rot)["steps"]
        assert steps[-1]["structures"]["counts"]["comparisons"] <= 5

    def test_is_rotated_sorted(self):
        assert find_min_rotated.is_rotated_sorted([3, 4, 5, 1, 2])
        assert find_min_rotated.is_rotated_sorted([1])
        assert not find_min_rotated.is_rotated_sorted([3, 1, 2, 0])
        assert not find_min_rotated.is_rotated_sorted([2, 2, 1])

    def test_find_peak(self):
        rng = random.Random(13)
        cases = [[1, 2, 3, 1], [1, 2, 1, 3, 5, 6, 4], [5], [1, 2], [2, 1],
                 [1, 3, 2, 4, 6, 5, 2]]
        for _ in range(100):
            n = rng.randint(1, 16)
            a = [rng.randint(0, 20)]
            while len(a) < n:
                v = rng.randint(0, 20)
                if v != a[-1]:
                    a.append(v)
            cases.append(a)
        for a in cases:
            i = find_peak.trace(a)["meta"]["result"]
            left = a[i - 1] if i > 0 else float("-inf")
            right = a[i + 1] if i < len(a) - 1 else float("-inf")
            assert a[i] > left and a[i] > right, (a, i)


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"trapping_rainwater", "asteroid_collision", "find_min_rotated",
                "find_peak"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("trapping_rainwater", [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]),
            ("asteroid_collision", [5, 10, -5]),
            ("find_min_rotated", [4, 5, 6, 7, 0, 1, 2]),
            ("find_peak", [1, 3, 2, 4, 6, 5, 2]),
        ]
        for algo, arr in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        bad = [
            ("trapping_rainwater", [1, -1]),
            ("trapping_rainwater", []),
            ("asteroid_collision", [3, 0, -2]),
            ("find_min_rotated", [3, 1, 2, 0]),     # two drops
            ("find_min_rotated", [2, 2, 1]),        # duplicates
            ("find_peak", [1, 2, 2, 1]),            # equal neighbours
            ("find_peak", list(range(20))),
        ]
        for algo, arr in bad:
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr})
            assert r.status_code == 400, (algo, arr)

    def test_detect_resolves(self):
        for algo in ("trapping_rainwater", "asteroid_collision",
                     "find_min_rotated", "find_peak"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
