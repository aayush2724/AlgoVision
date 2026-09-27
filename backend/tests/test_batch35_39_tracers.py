"""Batches 35–39 — numeric answer search (sqrt, nth root, bouquets), 2-D
matrix searches, list arithmetic, more monotonic stacks, array fundamentals.
Every tracer is checked against a brute-force reference on random input.
"""

import itertools
import math
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    answer_numeric, matrix_search, list_arith, stack_more, array_basics,
)

client = TestClient(app)
R = random.Random(35)


class TestAnswerNumeric:
    def test_sqrt(self):
        for n in list(range(1, 200)) + [10**6, 999_999]:
            assert answer_numeric.trace("sqrt_search", [n])["meta"]["result"] == math.isqrt(n)

    def test_nth_root(self):
        for p in range(1, 7):
            for m in range(1, 400):
                x = round(m ** (1 / p))
                want = next((c for c in (x - 1, x, x + 1) if c >= 1 and c ** p == m), -1)
                assert answer_numeric.trace("nth_root", [p, m])["meta"]["result"] == want, (p, m)

    def test_bouquets(self):
        for _ in range(150):
            bloom = [R.randint(1, 20) for _ in range(R.randint(1, 12))]
            m, k = R.randint(1, 4), R.randint(1, 3)

            def ok(day):
                made = run = 0
                for d in bloom:
                    run = run + 1 if d <= day else 0
                    if run == k:
                        made, run = made + 1, 0
                return made >= m
            want = next((d for d in range(1, 21) if ok(d)), -1)
            got = answer_numeric.trace("min_bouquets", bloom, f"{m},{k}")["meta"]["result"]
            assert got == want, (bloom, m, k)


class TestMatrix:
    def test_search_2d(self):
        for _ in range(100):
            r, c = R.randint(1, 5), R.randint(1, 5)
            flat = sorted(R.randint(0, 40) for _ in range(r * c))
            g = [flat[i * c:(i + 1) * c] for i in range(r)]
            x = R.randint(-1, 41)
            assert matrix_search.trace("search_2d_matrix", g, x)["meta"]["result"] is (x in flat)

    def test_search_2d_ii(self):
        for _ in range(100):
            r, c = R.randint(1, 5), R.randint(1, 5)
            g = [[0] * c for _ in range(r)]
            for i in range(r):
                for j in range(c):
                    g[i][j] = max(g[i][j - 1] if j else 0, g[i - 1][j] if i else 0) \
                        + R.randint(0, 3)
            assert matrix_search.validate("search_2d_matrix_ii", g, 1) is None
            x = R.randint(0, 25)
            want = any(x in row for row in g)
            assert matrix_search.trace("search_2d_matrix_ii", g, x)["meta"]["result"] is want

    def test_row_max_ones(self):
        for _ in range(100):
            r, c = R.randint(1, 5), R.randint(1, 6)
            g = [[0] * (c - k) + [1] * k for k in (R.randint(0, c) for _ in range(r))]
            counts = [sum(row) for row in g]
            best = max(counts)
            want = counts.index(best) if best else -1
            assert matrix_search.trace("row_max_ones", g)["meta"]["result"] == want


def _num(ds):
    return int("".join(map(str, reversed(ds))))


class TestListArith:
    def test_add_two(self):
        for _ in range(150):
            a = [R.randint(0, 9) for _ in range(R.randint(1, 8))]
            b = [R.randint(0, 9) for _ in range(R.randint(1, 8))]
            got = list_arith.trace("add_two_numbers", [a, b])["meta"]["result"]
            assert _num(got) == _num(a) + _num(b), (a, b, got)
            assert len(got) in (max(len(a), len(b)), max(len(a), len(b)) + 1)

    def test_add_one(self):
        for _ in range(150):
            d = [R.randint(0, 9) for _ in range(R.randint(1, 8))]
            want = str(int("".join(map(str, d))) + 1).rjust(len(d), "0")
            got = "".join(map(str, list_arith.trace("add_one_list", [d])["meta"]["result"]))
            assert got == want, d


def _brute_next(arr, better, circular):
    n, out = len(arr), []
    for i in range(n):
        rng = range(i + 1, i + n) if circular else range(i + 1, n)
        out.append(next((arr[j % n] for j in rng if better(arr[j % n], arr[i])), None))
    return out


class TestStackMore:
    def test_next_smaller_and_circular(self):
        for _ in range(100):
            arr = [R.randint(0, 9) for _ in range(R.randint(1, 12))]
            assert stack_more.trace("next_smaller", arr)["meta"]["result"] == \
                _brute_next(arr, lambda a, b: a < b, False)
            assert stack_more.trace("nge_circular", arr)["meta"]["result"] == \
                _brute_next(arr, lambda a, b: a > b, True)

    def test_remove_k_digits(self):
        for _ in range(100):
            arr = [R.randint(0, 9) for _ in range(R.randint(1, 7))]
            k = R.randint(0, len(arr))
            best = min((int("".join(map(str, c))) if c else 0)
                       for c in itertools.combinations(arr, len(arr) - k))
            assert stack_more.trace("remove_k_digits", arr, k)["meta"]["result"] == str(best)

    def test_sum_subarray_mins(self):
        for _ in range(100):
            arr = [R.randint(0, 20) for _ in range(R.randint(1, 12))]
            want = sum(min(arr[i:j + 1]) for i in range(len(arr)) for j in range(i, len(arr)))
            assert stack_more.trace("sum_subarray_mins", arr)["meta"]["result"] == want


class TestArrayBasics:
    def test_all(self):
        for _ in range(150):
            arr = [R.randint(0, 6) for _ in range(R.randint(2, 12))]
            k = R.randint(0, 25)
            assert array_basics.trace("remove_duplicates_sorted", arr)["meta"]["result"] == len(set(arr))
            kk = k % len(arr)
            assert array_basics.trace("rotate_array_k", arr, k)["meta"]["result"] == arr[kk:] + arr[:kk]
            nz = [v for v in arr if v]
            assert array_basics.trace("move_zeros", arr)["meta"]["result"] == nz + [0] * (len(arr) - len(nz))
            assert array_basics.trace("leaders", arr)["meta"]["result"] == \
                [v for i, v in enumerate(arr) if all(v > w for w in arr[i + 1:])]
            longest = max((j - i + 1 for i in range(len(arr)) for j in range(i, len(arr))
                           if sum(arr[i:j + 1]) == k), default=0)
            assert array_basics.trace("longest_subarray_sum_k", arr, k)["meta"]["result"] == longest
            distinct = sorted(set(arr))
            want2 = distinct[-2] if len(distinct) > 1 else None
            assert array_basics.trace("second_largest", arr)["meta"]["result"] == want2


class TestEndpoints:
    def test_ok(self):
        cases = [
            {"algorithm": "sqrt_search", "array": [28]},
            {"algorithm": "nth_root", "array": [3, 27]},
            {"algorithm": "min_bouquets", "array": [7, 7, 7, 7, 13, 11, 12, 7], "text": "2, 3"},
            {"algorithm": "search_2d_matrix", "text": "1,3,5/7,9,11", "target": 9},
            {"algorithm": "search_2d_matrix_ii", "text": "1,4/2,5", "target": 5},
            {"algorithm": "row_max_ones", "text": "0,1/1,1"},
            {"algorithm": "add_two_numbers", "text": "2,4,3/5,6,4"},
            {"algorithm": "add_one_list", "text": "1,9,9"},
            {"algorithm": "next_smaller", "array": [4, 8, 5, 2]},
            {"algorithm": "nge_circular", "array": [1, 2, 1]},
            {"algorithm": "remove_k_digits", "array": [1, 4, 3, 2], "target": 2},
            {"algorithm": "sum_subarray_mins", "array": [3, 1, 2, 4]},
            {"algorithm": "rotate_array_k", "array": [1, 2, 3], "target": 1},
            {"algorithm": "longest_subarray_sum_k", "array": [2, 3, 5], "target": 5},
            {"algorithm": "move_zeros", "array": [0, 1]},
        ]
        for p in cases:
            r = client.post("/api/trace", json=p)
            assert r.status_code == 200, (p, r.text)

    def test_validation(self):
        bad = [
            {"algorithm": "sqrt_search", "array": [0]},
            {"algorithm": "nth_root", "array": [3]},
            {"algorithm": "min_bouquets", "array": [1, 2], "text": "x"},
            {"algorithm": "search_2d_matrix", "text": "3,1/5,7", "target": 1},
            {"algorithm": "search_2d_matrix", "text": "1,3/5", "target": 1},
            {"algorithm": "search_2d_matrix_ii", "text": "1,2/0,3", "target": 1},
            {"algorithm": "row_max_ones", "text": "1,0/0,1"},
            {"algorithm": "add_two_numbers", "text": "1,2"},
            {"algorithm": "add_one_list", "text": "1,12"},
            {"algorithm": "remove_k_digits", "array": [1, 2], "target": 3},
            {"algorithm": "longest_subarray_sum_k", "array": [1, -2], "target": 1},
            {"algorithm": "second_largest", "array": [4]},
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for mod in (answer_numeric, matrix_search, list_arith, stack_more, array_basics):
            for algo in mod.TITLES:
                body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
                assert body["algorithm"] == algo, algo
