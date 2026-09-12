"""Batch 8 (competitive-programming tier): KMP, segment tree, Fenwick tree."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import fenwick_tree, kmp_search, segment_tree

client = TestClient(app)


def _final(res):
    return res["steps"][-1]["structures"]


# ── KMP ───────────────────────────────────────────────────────────────────

def _brute_find(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1)
            if text[i:i + len(pattern)] == pattern]


class TestKMP:
    def test_textbook_failure_table(self):
        res = kmp_search.trace("ABABDABACDABABCABAB", "ABABCABAB")
        assert res["meta"]["lps"] == [0, 0, 1, 2, 0, 1, 2, 3, 4]

    def test_textbook_match_position(self):
        res = kmp_search.trace("ABABDABACDABABCABAB", "ABABCABAB")
        assert res["meta"]["matches"] == [10]

    @pytest.mark.parametrize("text,pattern", [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AAAAA", "AA"),
        ("ABCDE", "E"),
        ("ABCDE", "A"),
        ("ABCDE", "XY"),
        ("AABAACAADAABAABA", "AABA"),
    ])
    def test_matches_brute_force(self, text, pattern):
        res = kmp_search.trace(text, pattern)
        assert res["meta"]["matches"] == _brute_find(text, pattern)

    def test_finds_overlapping_occurrences(self):
        assert kmp_search.trace("AAAAA", "AA")["meta"]["matches"] == [0, 1, 2, 3]

    def test_lps_is_zero_when_no_character_repeats(self):
        assert kmp_search.trace("ABCDE", "ABC")["meta"]["lps"] == [0, 0, 0]

    def test_never_exceeds_the_naive_comparison_count_badly(self):
        res = kmp_search.trace("AABAACAADAABAABA", "AABA")
        c = _final(res)["counts"]
        # The point of KMP: linear-ish, well under text-length × pattern-length
        assert c["comparisons"] < c["naive_would_cost"]

    def test_view_is_array_and_cells_are_characters(self):
        res = kmp_search.trace("ABAB", "AB")
        assert res["meta"]["view"] == "array"
        assert _final(res)["array"] == ["A", "B", "A", "B"]

    def test_api_validation(self):
        r = client.post("/api/trace", json={"algorithm": "kmp_search"})
        assert r.status_code == 400
        r = client.post("/api/trace",
                        json={"algorithm": "kmp_search", "text": "ABC"})
        assert r.status_code == 400
        r = client.post("/api/trace",
                        json={"algorithm": "kmp_search", "text": "AB,ABCD"})
        assert r.status_code == 400
        assert "longer than" in r.json()["detail"]


# ── Segment tree ──────────────────────────────────────────────────────────

VALUES = [3, 1, 4, 1, 5, 9, 2, 6]


class TestSegmentTree:
    @pytest.mark.parametrize("lo,hi", [
        (0, 7), (2, 5), (0, 0), (7, 7), (3, 4), (1, 6),
    ])
    def test_range_sum_is_correct(self, lo, hi):
        res = segment_tree.trace(VALUES, lo, hi)
        assert res["meta"]["result"] == sum(VALUES[lo:hi + 1])

    def test_root_holds_the_total(self):
        res = segment_tree.trace(VALUES, 0, 7)
        root = next(n for n in _final(res)["tree"] if n["id"] == 0)
        assert float(root["value"]) == sum(VALUES)

    def test_query_visits_far_fewer_nodes_than_the_range_length(self):
        res = segment_tree.trace(VALUES, 0, 7)
        c = _final(res)["counts"]
        # A full-range query should resolve at the root alone.
        assert c["full_covers"] >= 1

    def test_leaf_count_matches_the_input(self):
        res = segment_tree.trace(VALUES, 0, 7)
        leaves = [n for n in _final(res)["tree"]
                  if n["left"] is None and n["right"] is None]
        assert len(leaves) == len(VALUES)

    def test_single_element_array(self):
        res = segment_tree.trace([42], 0, 0)
        assert res["meta"]["result"] == 42

    def test_view_is_tree(self):
        assert segment_tree.trace(VALUES, 0, 3)["meta"]["view"] == "tree"

    def test_api_rejects_a_bad_range(self):
        r = client.post("/api/trace", json={
            "algorithm": "segment_tree", "array": [1, 2, 3], "text": "1:9",
        })
        assert r.status_code == 400

    def test_api_defaults_to_the_whole_array(self):
        r = client.post("/api/trace",
                        json={"algorithm": "segment_tree", "array": [1, 2, 3]})
        assert r.status_code == 200
        assert r.json()["meta"]["result"] == 6


# ── Fenwick tree ──────────────────────────────────────────────────────────

class TestFenwickTree:
    @pytest.mark.parametrize("upto", range(len(VALUES)))
    def test_prefix_sum_is_correct(self, upto):
        res = fenwick_tree.trace(VALUES, upto)
        assert res["meta"]["result"] == sum(VALUES[:upto + 1])

    def test_internal_slots_follow_the_low_bit_rule(self):
        # tree[i] must equal the sum of the last (i & -i) elements ending at i.
        res = fenwick_tree.trace(VALUES, 0)
        tree = _final(res)["tree"]
        for i in range(1, len(VALUES) + 1):
            span = i & -i
            assert tree[i] == sum(VALUES[i - span:i]), i

    def test_query_reads_are_logarithmic(self):
        res = fenwick_tree.trace(VALUES, len(VALUES) - 1)
        # 8 elements → at most 4 slot reads
        assert _final(res)["counts"]["query_reads"] <= 4

    def test_handles_negative_values(self):
        vals = [5, -3, 7, -1]
        res = fenwick_tree.trace(vals, 3)
        assert res["meta"]["result"] == sum(vals)

    def test_single_element(self):
        assert fenwick_tree.trace([9], 0)["meta"]["result"] == 9

    def test_view_is_array(self):
        assert fenwick_tree.trace(VALUES, 2)["meta"]["view"] == "array"

    def test_api_rejects_an_out_of_range_index(self):
        r = client.post("/api/trace", json={
            "algorithm": "fenwick_tree", "array": [1, 2, 3], "target": 5,
        })
        assert r.status_code == 400


# ── API surface ───────────────────────────────────────────────────────────

class TestBatch8Endpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"kmp_search", "segment_tree", "fenwick_tree"} <= ids

    def test_kmp_runs_over_the_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "kmp_search", "text": "abababcabab,ababc",
        })
        assert r.status_code == 200
        assert r.json()["meta"]["matches"] == [2]

    def test_every_step_carries_counts(self):
        for res in (kmp_search.trace("ABAB", "AB"),
                    segment_tree.trace([1, 2, 3, 4], 1, 2),
                    fenwick_tree.trace([1, 2, 3, 4], 2)):
            assert all("counts" in s["structures"] for s in res["steps"])

    def test_catalog_is_still_growing_not_shrinking(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert len(ids) >= 36
