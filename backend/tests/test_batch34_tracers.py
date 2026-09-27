"""Batch 34 — binary-search boundary variants (Step 4): lower/upper bound,
first & last occurrence, floor & ceil, kth missing positive, single element
in a sorted array. Checked against `bisect` and brute force on random input.
"""

import bisect
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import bs_variants

client = TestClient(app)


def _rand_sorted(rng):
    return sorted(rng.randint(0, 9) for _ in range(rng.randint(1, 16)))


class TestVariants:
    def test_bounds_and_occurrences(self):
        rng = random.Random(4)
        for _ in range(200):
            arr = _rand_sorted(rng)
            x = rng.randint(-1, 10)
            assert bs_variants.trace("lower_bound", arr, x)["meta"]["result"] == \
                bisect.bisect_left(arr, x)
            assert bs_variants.trace("upper_bound", arr, x)["meta"]["result"] == \
                bisect.bisect_right(arr, x)
            lo, hi = bisect.bisect_left(arr, x), bisect.bisect_right(arr, x)
            want = [lo, hi - 1] if lo < hi else [-1, -1]
            assert bs_variants.trace("first_last_occurrence", arr, x)["meta"]["result"] == want
            floors = [v for v in arr if v <= x]
            ceils = [v for v in arr if v >= x]
            assert bs_variants.trace("floor_ceil", arr, x)["meta"]["result"] == \
                [max(floors) if floors else None, min(ceils) if ceils else None]

    def test_unsorted_input_is_sorted_first(self):
        assert bs_variants.trace("lower_bound", [5, 1, 3], 3)["meta"]["result"] == 1

    def test_kth_missing(self):
        rng = random.Random(20)
        for _ in range(150):
            arr = sorted(rng.sample(range(1, 30), rng.randint(1, 10)))
            k = rng.randint(1, 20)
            missing = [v for v in range(1, 100) if v not in set(arr)]
            assert bs_variants.trace("kth_missing", arr, k)["meta"]["result"] == missing[k - 1]

    def test_single_element(self):
        rng = random.Random(39)
        for _ in range(100):
            vals = rng.sample(range(0, 50), rng.randint(1, 7))
            single = vals[0]
            arr = sorted([single] + [v for v in vals[1:] for _ in (0, 1)])
            assert bs_variants.trace("single_element_sorted", arr)["meta"]["result"] == single

    def test_validate(self):
        assert bs_variants.validate("kth_missing", [2, 2, 3], 1)
        assert bs_variants.validate("kth_missing", [0, 2], 1)
        assert bs_variants.validate("single_element_sorted", [1, 1, 2, 2], None)
        assert bs_variants.validate("single_element_sorted", [2, 1, 1], None)
        assert bs_variants.validate("lower_bound", [1, 2], None)
        assert bs_variants.validate("lower_bound", [1, 2], 1) is None


class TestEndpoints:
    def test_endpoints_ok(self):
        for algo, arr, t in (("lower_bound", [1, 2, 2, 3], 2), ("upper_bound", [1, 2, 2, 3], 2),
                             ("first_last_occurrence", [2, 8, 8, 9], 8),
                             ("floor_ceil", [3, 4, 7], 5), ("kth_missing", [2, 3, 4, 7, 11], 5),
                             ("single_element_sorted", [1, 1, 2, 3, 3], None)):
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr, "target": t})
            assert r.status_code == 200, (algo, r.text)

    def test_validation(self):
        for algo, arr, t in (("lower_bound", [1, 2], None), ("kth_missing", [3, 1], 2),
                             ("single_element_sorted", [1, 1, 2, 2], None),
                             ("floor_ceil", list(range(17)), 3)):
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr, "target": t})
            assert r.status_code == 400, (algo, arr, t)

    def test_detect_resolves(self):
        for algo in bs_variants.TITLES:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
