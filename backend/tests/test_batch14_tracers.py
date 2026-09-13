"""Batch 14 — heap sort (in-place, array view), find middle and merge two
sorted lists (list view).

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import find_middle, heap_sort, merge_two_sorted_lists

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


# ── HEAP SORT ─────────────────────────────────────────────────────────────

class TestHeapSort:
    def test_classic(self):
        assert heap_sort.trace([5, 3, 8, 1, 9, 2])["meta"]["result"] == [1, 2, 3, 5, 8, 9]

    def test_single_and_empty(self):
        assert heap_sort.trace([7])["meta"]["result"] == [7]
        assert heap_sort.trace([])["meta"]["result"] == []

    def test_already_sorted_and_reversed(self):
        assert heap_sort.trace([1, 2, 3, 4])["meta"]["result"] == [1, 2, 3, 4]
        assert heap_sort.trace([4, 3, 2, 1])["meta"]["result"] == [1, 2, 3, 4]

    def test_every_step_array_is_a_permutation(self):
        arr = [5, 3, 8, 1, 9, 2, 7]
        for s in heap_sort.trace(arr)["steps"]:
            assert sorted(s["structures"]["array"]) == sorted(arr)

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_builtin_sort(self, seed):
        rng = random.Random(seed)
        arr = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        res = heap_sort.trace(arr)
        assert res["meta"]["result"] == sorted(arr)
        if len(arr) > 1:
            _assert_envelope(res)


# ── FIND MIDDLE ───────────────────────────────────────────────────────────

class TestFindMiddle:
    def test_odd_length(self):
        assert find_middle.trace([10, 20, 30, 40, 50])["meta"]["middle_index"] == 2

    def test_even_length_takes_second_middle(self):
        # Standard slow/fast convention lands on the second of the two middles.
        assert find_middle.trace([10, 20, 30, 40])["meta"]["middle_index"] == 2

    def test_single(self):
        res = find_middle.trace([99])
        assert res["meta"]["middle_index"] == 0
        assert res["meta"]["middle_value"] == 99
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_halfway_index(self, seed):
        rng = random.Random(seed)
        vals = [rng.randint(0, 99) for _ in range(rng.randint(1, 12))]
        res = find_middle.trace(vals)
        assert res["meta"]["middle_index"] == len(vals) // 2
        assert res["meta"]["middle_value"] == vals[len(vals) // 2]
        _assert_envelope(res)


# ── MERGE TWO SORTED LISTS ────────────────────────────────────────────────

class TestMergeTwoSortedLists:
    def test_classic(self):
        assert merge_two_sorted_lists.trace([1, 3, 5], [2, 4, 6])["meta"][
            "merged"] == [1, 2, 3, 4, 5, 6]

    def test_one_empty(self):
        assert merge_two_sorted_lists.trace([], [2, 4])["meta"]["merged"] == [2, 4]
        assert merge_two_sorted_lists.trace([1, 2], [])["meta"]["merged"] == [1, 2]

    def test_interleaving_and_duplicates(self):
        assert merge_two_sorted_lists.trace([1, 1, 2], [1, 3])["meta"][
            "merged"] == [1, 1, 1, 2, 3]

    def test_one_list_entirely_before_the_other(self):
        assert merge_two_sorted_lists.trace([1, 2, 3], [4, 5, 6])["meta"][
            "merged"] == [1, 2, 3, 4, 5, 6]

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_sorted_concatenation(self, seed):
        rng = random.Random(seed)
        a = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 6)))
        b = sorted(rng.randint(0, 20) for _ in range(rng.randint(0, 6)))
        if not a and not b:
            a = [0]
        res = merge_two_sorted_lists.trace(a, b)
        assert res["meta"]["merged"] == sorted(a + b)
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"heap_sort", "find_middle", "merge_two_sorted_lists"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "heap_sort", "array": [5, 3, 8, 1, 9, 2]},
        {"algorithm": "find_middle", "array": [10, 20, 30, 40, 50]},
        {"algorithm": "merge_two_sorted_lists", "text": "1,3,5,7 | 2,4,6"},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "find_middle", "array": []}, "non-empty"),
        ({"algorithm": "merge_two_sorted_lists"}, "requires 'text'"),
        ({"algorithm": "merge_two_sorted_lists", "text": "1,2,3"}, "separated by a single"),
        ({"algorithm": "merge_two_sorted_lists", "text": "3,1 | 2,4"}, "sorted ascending"),
        ({"algorithm": "merge_two_sorted_lists", "text": "1,x | 2"}, "not a number"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id",
                             ["heap_sort", "find_middle", "merge_two_sorted_lists"])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
