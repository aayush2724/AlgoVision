"""Batch 11 — DP classics on the grid view: house robber (1-D DP),
longest increasing subsequence (O(n²) DP), and subset sum (boolean DP grid).

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random
from itertools import combinations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import house_robber, lis, subset_sum

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


def _assert_rectangular(res):
    for s in res["steps"]:
        grid = s["structures"]["grid"]
        assert len({len(row) for row in grid}) == 1, "ragged grid"


# ── HOUSE ROBBER ──────────────────────────────────────────────────────────

def _brute_rob(nums):
    best = 0
    n = len(nums)
    for mask in range(1 << n):
        chosen = [i for i in range(n) if mask & (1 << i)]
        if any(b - a == 1 for a, b in zip(chosen, chosen[1:])):
            continue  # adjacent houses — illegal
        best = max(best, sum(nums[i] for i in chosen))
    return best


class TestHouseRobber:
    def test_classic(self):
        assert house_robber.trace([2, 7, 9, 3, 1])["meta"]["result"] == 12

    def test_adjacent_pick_is_avoided(self):
        # Robbing 5 and 5 (adjacent) is illegal; best is a single 5.
        assert house_robber.trace([5, 5])["meta"]["result"] == 5

    def test_single_house(self):
        assert house_robber.trace([9])["meta"]["result"] == 9

    def test_empty(self):
        res = house_robber.trace([])
        assert res["meta"]["result"] == 0
        _assert_envelope(res)

    def test_robbed_houses_are_never_adjacent(self):
        robbed = house_robber.trace([2, 7, 9, 3, 1, 8])["meta"]["robbed"]
        for a, b in zip(robbed, robbed[1:]):
            assert b - a >= 2, "reconstructed houses must not be adjacent"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nums = [rng.randint(0, 20) for _ in range(rng.randint(0, 9))]
        res = house_robber.trace(nums)
        assert res["meta"]["result"] == _brute_rob(nums)
        # The reconstructed subset must actually sum to the reported best.
        assert sum(nums[i] for i in res["meta"]["robbed"]) == res["meta"]["result"]
        if nums:
            _assert_envelope(res)
            _assert_rectangular(res)


# ── LONGEST INCREASING SUBSEQUENCE ────────────────────────────────────────

def _brute_lis(nums):
    best = 0
    n = len(nums)
    for mask in range(1 << n):
        chosen = [nums[i] for i in range(n) if mask & (1 << i)]
        if all(a < b for a, b in zip(chosen, chosen[1:])):
            best = max(best, len(chosen))
    return best


class TestLIS:
    def test_classic(self):
        # [2,3,7,101] is one LIS of length 4.
        assert lis.trace([10, 9, 2, 5, 3, 7, 101, 18])["meta"]["result"] == 4

    def test_strictly_increasing_input(self):
        assert lis.trace([1, 2, 3, 4])["meta"]["result"] == 4

    def test_all_equal_is_length_one(self):
        assert lis.trace([5, 5, 5])["meta"]["result"] == 1

    def test_decreasing_is_length_one(self):
        assert lis.trace([5, 4, 3, 2])["meta"]["result"] == 1

    def test_empty(self):
        res = lis.trace([])
        assert res["meta"]["result"] == 0
        _assert_envelope(res)

    def test_recovered_subsequence_is_strictly_increasing(self):
        sub = lis.trace([3, 1, 8, 2, 5])["meta"]["subsequence"]
        assert all(a < b for a, b in zip(sub, sub[1:]))

    def test_indices_are_increasing_and_match_values(self):
        res = lis.trace([3, 1, 8, 2, 5, 6])
        idx = res["meta"]["indices"]
        assert idx == sorted(idx), "indices must keep original order"
        assert idx == sorted(set(idx)), "indices must be distinct"
        assert len(idx) == res["meta"]["result"]

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nums = [rng.randint(0, 15) for _ in range(rng.randint(0, 9))]
        res = lis.trace(nums)
        assert res["meta"]["result"] == _brute_lis(nums)
        if nums:
            _assert_envelope(res)
            _assert_rectangular(res)


# ── SUBSET SUM ────────────────────────────────────────────────────────────

def _brute_subset(nums, target):
    for r in range(len(nums) + 1):
        for combo in combinations(nums, r):
            if sum(combo) == target:
                return True
    return False


class TestSubsetSum:
    def test_reachable(self):
        assert subset_sum.trace([3, 4, 5], 9)["meta"]["result"] is True  # 4+5

    def test_unreachable(self):
        assert subset_sum.trace([2, 4, 6], 5)["meta"]["result"] is False

    def test_target_zero_is_always_reachable(self):
        assert subset_sum.trace([3, 4], 0)["meta"]["result"] is True

    def test_exact_single_element(self):
        assert subset_sum.trace([3, 8, 5], 8)["meta"]["result"] is True

    def test_witness_subset_sums_to_target(self):
        res = subset_sum.trace([2, 3, 5, 6], 11)  # 5+6 or 2+3+6
        assert res["meta"]["result"] is True
        assert sum(res["meta"]["subset"]) == 11

    def test_grid_is_rectangular(self):
        _assert_rectangular(subset_sum.trace([1, 2, 3], 6))

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nums = [rng.randint(1, subset_sum.MAX_VALUE)
                for _ in range(rng.randint(1, subset_sum.MAX_ITEMS))]
        target = rng.randint(0, subset_sum.MAX_TARGET)
        res = subset_sum.trace(nums, target)
        assert res["meta"]["result"] == _brute_subset(nums, target)
        if res["meta"]["result"]:
            assert sum(res["meta"]["subset"]) == target
        _assert_envelope(res)
        _assert_rectangular(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"house_robber", "lis", "subset_sum"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "house_robber", "array": [2, 7, 9, 3, 1]},
        {"algorithm": "lis", "array": [10, 9, 2, 5, 3, 7]},
        {"algorithm": "subset_sum", "array": [3, 4, 5], "target": 9},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "house_robber", "array": [1, -2]}, "0 or more"),
        ({"algorithm": "subset_sum", "array": [1, 2]}, "requires a 'target'"),
        ({"algorithm": "subset_sum", "array": [1], "target": 99}, "from 0 to"),
        ({"algorithm": "subset_sum", "array": [0], "target": 3}, "from 1 to"),
        ({"algorithm": "lis"}, "requires an 'array'"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id", ["house_robber", "lis", "subset_sum"])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
