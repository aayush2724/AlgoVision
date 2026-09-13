"""Batch 13 — radix sort and sliding-window maximum (array view) and matrix
chain multiplication (grid view).

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random
from functools import lru_cache

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import matrix_chain, radix_sort, sliding_window_maximum

client = TestClient(app)

ENVELOPE = {"i", "line", "structures", "highlight", "note"}


def _assert_envelope(res):
    assert res["steps"], "a tracer must emit at least one step"
    for s in res["steps"]:
        assert ENVELOPE <= set(s), f"step {s.get('i')} is missing envelope keys"
        assert "counts" in s["structures"], "counters missing from structures"
        assert s["note"], "every step needs a note to narrate"
    for key in res["steps"][0]["structures"]["counts"]:
        seq = [s["structures"]["counts"][key] for s in res["steps"]]
        assert seq == sorted(seq), f"counter {key!r} went backwards: {seq}"


# ── RADIX SORT ────────────────────────────────────────────────────────────

class TestRadixSort:
    def test_classic(self):
        assert radix_sort.trace([170, 45, 75, 90, 2, 802, 24, 66])["meta"][
            "result"] == [2, 24, 45, 66, 75, 90, 170, 802]

    def test_single_and_empty(self):
        assert radix_sort.trace([5])["meta"]["result"] == [5]
        assert radix_sort.trace([])["meta"]["result"] == []

    def test_duplicates_and_zeros(self):
        assert radix_sort.trace([0, 0, 3, 3, 1])["meta"]["result"] == [0, 0, 1, 3, 3]

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_builtin_sort(self, seed):
        rng = random.Random(seed)
        arr = [rng.randint(0, 9999) for _ in range(rng.randint(0, 12))]
        res = radix_sort.trace(arr)
        assert res["meta"]["result"] == sorted(arr)
        if len(arr) > 1:
            _assert_envelope(res)

    def test_array_is_always_a_permutation_of_the_input(self):
        arr = [170, 45, 75, 90, 2, 802]
        for s in radix_sort.trace(arr)["steps"]:
            assert sorted(s["structures"]["array"]) == sorted(arr)


# ── SLIDING WINDOW MAXIMUM ────────────────────────────────────────────────

def _brute_window_max(arr, k):
    return [max(arr[i:i + k]) for i in range(len(arr) - k + 1)]


class TestSlidingWindowMaximum:
    def test_classic(self):
        assert sliding_window_maximum.trace([1, 3, -1, -3, 5, 3, 6, 7], 3)[
            "meta"]["maxes"] == [3, 3, 5, 5, 6, 7]

    def test_window_of_one_is_the_array(self):
        assert sliding_window_maximum.trace([4, 2, 9], 1)["meta"]["maxes"] == [4, 2, 9]

    def test_window_is_whole_array(self):
        assert sliding_window_maximum.trace([4, 2, 9, 1], 4)["meta"]["maxes"] == [9]

    def test_descending(self):
        assert sliding_window_maximum.trace([5, 4, 3, 2, 1], 2)["meta"][
            "maxes"] == [5, 4, 3, 2]

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        arr = [rng.randint(-20, 20) for _ in range(rng.randint(1, 13))]
        k = rng.randint(1, len(arr))
        res = sliding_window_maximum.trace(arr, k)
        assert res["meta"]["maxes"] == _brute_window_max(arr, k)
        _assert_envelope(res)


# ── MATRIX CHAIN ──────────────────────────────────────────────────────────

def _brute_matrix_chain(p):
    n = len(p) - 1

    @lru_cache(maxsize=None)
    def best(i, j):
        if i == j:
            return 0
        return min(best(i, k) + best(k + 1, j) + p[i] * p[k + 1] * p[j + 1]
                   for k in range(i, j))

    return best(0, n - 1) if n else 0


class TestMatrixChain:
    def test_classic(self):
        # Matrices 40x20, 20x30, 30x10, 10x30 → known optimum 26000.
        assert matrix_chain.trace([40, 20, 30, 10, 30])["meta"]["result"] == 26000

    def test_two_matrices_is_a_single_product(self):
        # 10x20 times 20x30 = one multiplication costing 10*20*30.
        assert matrix_chain.trace([10, 20, 30])["meta"]["result"] == 6000

    def test_single_matrix_costs_nothing(self):
        res = matrix_chain.trace([10, 20])
        assert res["meta"]["result"] == 0
        _assert_envelope(res)

    def test_diagonal_is_zero(self):
        res = matrix_chain.trace([5, 10, 3, 12])
        last = res["steps"][-1]["structures"]["grid"]
        for i in range(len(last)):
            assert last[i][i] == 0, "a single matrix must cost 0"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        p = [rng.randint(1, 40) for _ in range(rng.randint(2, 7))]
        res = matrix_chain.trace(p)
        assert res["meta"]["result"] == _brute_matrix_chain(p)
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"radix_sort", "sliding_window_maximum", "matrix_chain"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "radix_sort", "array": [170, 45, 75, 90, 2, 802]},
        {"algorithm": "sliding_window_maximum", "array": [1, 3, -1, 5, 3], "target": 3},
        {"algorithm": "matrix_chain", "array": [40, 20, 30, 10, 30]},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "radix_sort", "array": [-1]}, "from 0 to"),
        ({"algorithm": "sliding_window_maximum", "array": [1, 2]}, "window size"),
        ({"algorithm": "sliding_window_maximum", "array": [1, 2], "target": 9}, "between 1 and"),
        ({"algorithm": "matrix_chain", "array": [10]}, "at least 2"),
        ({"algorithm": "matrix_chain", "array": [10, 0]}, "from 1 to 1000"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id",
                             ["radix_sort", "sliding_window_maximum", "matrix_chain"])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
