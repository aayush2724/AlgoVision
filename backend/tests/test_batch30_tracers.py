"""Batch 30 — binary search on the answer (Step 4): Koko eating bananas,
min-max partition (book allocation / painter's / ship-in-D-days / split
array), and aggressive cows. Each is checked against a brute force that
tries every candidate answer.
"""

import itertools
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import koko_bananas, min_max_partition, aggressive_cows

client = TestClient(app)


def _ref_koko(piles, h):
    return next(k for k in range(1, max(piles) + 1)
                if sum(-(-p // k) for p in piles) <= h)


def _ref_partition(arr, k):
    """Try every way to cut into at most k contiguous groups."""
    n, best = len(arr), None
    for g in range(1, k + 1):
        for cuts in itertools.combinations(range(1, n), g - 1):
            bounds = (0, *cuts, n)
            worst = max(sum(arr[a:b]) for a, b in zip(bounds, bounds[1:]))
            best = worst if best is None else min(best, worst)
    return best


def _ref_cows(stalls, c):
    s = sorted(stalls)
    return max(min(b - a for a, b in zip(pick, pick[1:]))
               for pick in itertools.combinations(s, c))


class TestAnswerSearch:
    def test_koko(self):
        assert koko_bananas.trace([3, 6, 7, 11], 8)["meta"]["result"] == 4
        assert koko_bananas.trace([30, 11, 23, 4, 20], 5)["meta"]["result"] == 30
        rng = random.Random(16)
        for _ in range(80):
            piles = [rng.randint(1, 60) for _ in range(rng.randint(1, 8))]
            h = rng.randint(len(piles), len(piles) * 6)
            assert koko_bananas.trace(piles, h)["meta"]["result"] == _ref_koko(piles, h)

    def test_partition(self):
        assert min_max_partition.trace([12, 34, 67, 90], 2)["meta"]["result"] == 113
        assert min_max_partition.trace([7, 2, 5, 10, 8], 2)["meta"]["result"] == 18
        rng = random.Random(22)
        for _ in range(80):
            arr = [rng.randint(1, 30) for _ in range(rng.randint(1, 8))]
            k = rng.randint(1, len(arr))
            assert min_max_partition.trace(arr, k)["meta"]["result"] == \
                _ref_partition(arr, k), (arr, k)

    def test_cows(self):
        assert aggressive_cows.trace([0, 3, 4, 7, 10, 9], 4)["meta"]["result"] == 3
        rng = random.Random(21)
        for _ in range(80):
            stalls = rng.sample(range(0, 60), rng.randint(2, 8))
            c = rng.randint(2, len(stalls))
            assert aggressive_cows.trace(stalls, c)["meta"]["result"] == \
                _ref_cows(stalls, c), (stalls, c)

    def test_answer_line_shrinks(self):
        steps = koko_bananas.trace([3, 6, 7, 11], 8)["steps"]
        widths = [s["structures"]["answer"]["hi"] - s["structures"]["answer"]["lo"]
                  for s in steps]
        assert widths[-1] < widths[0]


class TestEndpoints:
    def test_endpoints_ok(self):
        for algo, arr, t in (("koko_bananas", [3, 6, 7, 11], 8),
                             ("min_max_partition", [12, 34, 67, 90], 2),
                             ("aggressive_cows", [0, 3, 4, 7, 10, 9], 4)):
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr, "target": t})
            assert r.status_code == 200, (algo, r.text)

    def test_validation(self):
        bad = [
            ("koko_bananas", [3, 6, 7], 2),          # fewer hours than piles
            ("koko_bananas", [0, 6], 5),             # empty pile
            ("min_max_partition", [1, 2], 3),        # more groups than items
            ("min_max_partition", [1, 2.5], 1),
            ("aggressive_cows", [1, 1, 5], 2),       # duplicate stalls
            ("aggressive_cows", [1, 5], 3),          # more cows than stalls
            ("aggressive_cows", [1, 5], None),
        ]
        for algo, arr, t in bad:
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr, "target": t})
            assert r.status_code == 400, (algo, arr, t)

    def test_detect_resolves(self):
        for algo in ("koko_bananas", "min_max_partition", "aggressive_cows"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
