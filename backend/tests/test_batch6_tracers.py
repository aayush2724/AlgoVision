"""Batch 6: topological sort, counting sort, prefix sums, next greater
element, edit distance, Floyd's cycle detection."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    counting_sort, edit_distance, floyd_cycle, next_greater_element,
    prefix_sums, topological_sort,
)
from app.tracers.common import Graph

client = TestClient(app)


def _final(res):
    return res["steps"][-1]["structures"]


def _every_step_has_counts(res):
    return all("counts" in s["structures"] for s in res["steps"])


# ── Topological sort ──────────────────────────────────────────────────────

DAG = Graph(
    nodes=[{"id": c} for c in "ABCDE"],
    edges=[["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["D", "E"]],
)


class TestTopologicalSort:
    def test_order_respects_every_edge(self):
        res = topological_sort.trace(DAG, "A")
        order = res["meta"]["order"]
        pos = {n: i for i, n in enumerate(order)}
        for a, b in [(str(e[0]), str(e[1])) for e in DAG.edges]:
            assert pos[a] < pos[b], f"{a} must come before {b} in {order}"

    def test_emits_every_node_exactly_once(self):
        order = topological_sort.trace(DAG, "A")["meta"]["order"]
        assert sorted(order) == sorted(n.id for n in DAG.nodes)

    def test_start_node_goes_first_when_it_has_no_prerequisites(self):
        # Two independent roots: whichever the student picks should lead.
        g = Graph(nodes=[{"id": c} for c in "XYZ"], edges=[["X", "Z"], ["Y", "Z"]])
        assert topological_sort.trace(g, "Y")["meta"]["order"][0] == "Y"
        assert topological_sort.trace(g, "X")["meta"]["order"][0] == "X"

    def test_cycle_is_reported_not_silently_truncated(self):
        cyc = Graph(nodes=[{"id": c} for c in "ABC"],
                    edges=[["A", "B"], ["B", "C"], ["C", "A"]])
        res = topological_sort.trace(cyc, "A")
        assert res["meta"]["cyclic"] is True
        assert res["meta"]["order"] == []
        assert "cycle" in res["steps"][-1]["note"].lower()

    def test_partial_cycle_stops_after_emitting_the_acyclic_part(self):
        # A → B, then a separate cycle D → E → D that never becomes ready.
        g = Graph(nodes=[{"id": c} for c in "ABDE"],
                  edges=[["A", "B"], ["D", "E"], ["E", "D"]])
        res = topological_sort.trace(g, "A")
        assert res["meta"]["cyclic"] is True
        assert sorted(res["meta"]["order"]) == ["A", "B"]

    def test_counts_present_and_view_is_graph(self):
        res = topological_sort.trace(DAG, "A")
        assert res["meta"]["view"] == "graph"
        assert _every_step_has_counts(res)
        assert _final(res)["counts"]["emitted"] == len(DAG.nodes)


# ── Counting sort ─────────────────────────────────────────────────────────

class TestCountingSort:
    @pytest.mark.parametrize("data", [
        [4, 2, 2, 8, 3, 3, 1],
        [0, 0, 0],
        [5],
        [9, 8, 7, 6],
        [1, 1, 2, 2, 3, 3],
    ])
    def test_sorts_correctly(self, data):
        res = counting_sort.trace(data)
        assert _final(res)["array"] == sorted(data)

    def test_output_is_a_permutation_of_the_input(self):
        data = [4, 2, 2, 8, 3, 3, 1]
        out = _final(counting_sort.trace(data))["array"]
        assert sorted(out) == sorted(data)

    def test_never_compares_values(self):
        res = counting_sort.trace([4, 2, 2, 8, 3, 3, 1])
        assert _final(res)["counts"]["comparisons"] == 0

    def test_writes_exactly_one_per_element(self):
        data = [4, 2, 2, 8, 3, 3, 1]
        res = counting_sort.trace(data)
        assert _final(res)["counts"]["writes"] == len(data)
        assert _final(res)["counts"]["tallies"] == len(data)

    def test_empty_array(self):
        res = counting_sort.trace([])
        assert _final(res)["array"] == []

    def test_rejects_negatives_and_fractions_at_the_api(self):
        for bad in ([-1, 2], [1.5, 2]):
            r = client.post("/api/trace",
                            json={"algorithm": "counting_sort", "array": bad})
            assert r.status_code == 400
            assert "whole numbers" in r.json()["detail"]

    def test_rejects_values_above_the_bucket_ceiling(self):
        r = client.post("/api/trace", json={
            "algorithm": "counting_sort",
            "array": [counting_sort.MAX_VALUE + 1],
        })
        assert r.status_code == 400


# ── Prefix sums ───────────────────────────────────────────────────────────

class TestPrefixSums:
    def test_prefix_array_is_cumulative(self):
        res = prefix_sums.trace([2, 4, 6, 8])
        assert _final(res)["prefix"] == [0, 2, 6, 12, 20]

    def test_prefix_zero_is_always_zero(self):
        # prefix[0] = 0 is what makes ranges starting at index 0 work.
        assert _final(prefix_sums.trace([5, -3, 7]))["prefix"][0] == 0

    def test_handles_negative_values(self):
        res = prefix_sums.trace([5, -3, 7])
        assert _final(res)["prefix"] == [0, 5, 2, 9]

    def test_range_query_matches_the_direct_sum(self):
        data = [3, 1, 4, 1, 5, 9]
        prefix = _final(prefix_sums.trace(data))["prefix"]
        lo, hi = 1, len(data) - 2
        assert prefix[hi + 1] - prefix[lo] == sum(data[lo:hi + 1])

    def test_additions_are_linear(self):
        data = [1, 2, 3, 4, 5]
        assert _final(prefix_sums.trace(data))["counts"]["additions"] == len(data)

    def test_empty_and_single(self):
        assert prefix_sums.trace([])["steps"]
        assert _final(prefix_sums.trace([7]))["prefix"] == [0, 7]


# ── Next greater element ──────────────────────────────────────────────────

def _brute_nge(arr):
    out = []
    for i, v in enumerate(arr):
        out.append(next((w for w in arr[i + 1:] if w > v), None))
    return out


class TestNextGreaterElement:
    @pytest.mark.parametrize("data", [
        [2, 1, 2, 4, 3],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [5, 5, 5],
        [7],
        [],
    ])
    def test_matches_the_brute_force_answer(self, data):
        res = next_greater_element.trace(data)
        assert res["meta"]["result"] == _brute_nge(data)

    def test_strictly_decreasing_input_has_no_answers(self):
        res = next_greater_element.trace([9, 7, 5, 3])
        assert res["meta"]["result"] == [None, None, None, None]

    def test_each_index_is_pushed_exactly_once(self):
        data = [2, 1, 2, 4, 3]
        final = _final(next_greater_element.trace(data))
        assert final["counts"]["pushes"] == len(data)
        assert final["counts"]["pops"] <= len(data)

    def test_leftover_stack_entries_stay_unanswered(self):
        res = next_greater_element.trace([4, 3, 2, 1])
        # Nothing was ever popped, so every answer is None.
        assert _final(res)["counts"]["pops"] == 0


# ── Edit distance ─────────────────────────────────────────────────────────

class TestEditDistance:
    @pytest.mark.parametrize("a,b,expected", [
        ("KITTEN", "SITTING", 3),
        ("FLAW", "LAWN", 2),
        ("ABC", "ABC", 0),
        ("A", "", 1),
        ("", "ABC", 3),
        ("SUNDAY", "SATURDAY", 3),
    ])
    def test_known_distances(self, a, b, expected):
        assert edit_distance.trace(a, b)["meta"]["result"] == expected

    def test_is_symmetric(self):
        assert (edit_distance.trace("KITTEN", "SITTING")["meta"]["result"]
                == edit_distance.trace("SITTING", "KITTEN")["meta"]["result"])

    def test_identical_words_need_no_edits_and_match_every_cell(self):
        res = edit_distance.trace("ABCD", "ABCD")
        assert res["meta"]["result"] == 0
        assert _final(res)["counts"]["free_matches"] == 4

    def test_distance_never_exceeds_the_longer_word(self):
        a, b = "ABCD", "WXYZ"
        assert edit_distance.trace(a, b)["meta"]["result"] <= max(len(a), len(b))

    def test_grid_dimensions_and_labels(self):
        res = edit_distance.trace("AB", "XYZ")
        grid = _final(res)["grid"]
        assert len(grid) == 3 and len(grid[0]) == 4
        assert res["meta"]["row_labels"] == ["∅", "A", "B"]
        assert res["meta"]["col_labels"] == ["∅", "X", "Y", "Z"]

    def test_view_is_grid(self):
        assert edit_distance.trace("AB", "AC")["meta"]["view"] == "grid"


# ── Floyd's cycle detection ───────────────────────────────────────────────

class TestFloydCycle:
    def test_finds_a_cycle_and_its_entrance(self):
        res = floyd_cycle.trace([1, 2, 3, 4, 5], 2)
        assert res["meta"]["has_cycle"] is True
        assert res["meta"]["cycle_start"] == 2

    @pytest.mark.parametrize("link_to", [0, 1, 2, 3, 4])
    def test_entrance_is_correct_for_every_link_point(self, link_to):
        res = floyd_cycle.trace([10, 20, 30, 40, 50], link_to)
        assert res["meta"]["cycle_start"] == link_to

    def test_terminated_list_reports_no_cycle(self):
        res = floyd_cycle.trace([1, 2, 3, 4, 5], -1)
        assert res["meta"]["has_cycle"] is False
        assert res["meta"]["cycle_start"] is None

    def test_self_loop_on_the_only_node(self):
        res = floyd_cycle.trace([7], 0)
        assert res["meta"]["has_cycle"] is True
        assert res["meta"]["cycle_start"] == 0

    def test_empty_list(self):
        res = floyd_cycle.trace([], -1)
        assert res["meta"]["has_cycle"] is False

    def test_fast_pointer_moves_twice_as_often_as_slow(self):
        # Only true during phase one, so check the step where they collide.
        res = floyd_cycle.trace([1, 2, 3, 4, 5, 6], 1)
        collision = next(s for s in res["steps"] if "lapped" in s["note"])
        c = collision["structures"]["counts"]
        assert c["fast_moves"] == 2 * c["slow_moves"]

    def test_view_is_list_and_next_pointers_form_the_cycle(self):
        res = floyd_cycle.trace([1, 2, 3, 4], 1)
        assert res["meta"]["view"] == "list"
        assert res["steps"][-1]["structures"]["next"][-1] == 1


# ── API surface ───────────────────────────────────────────────────────────

class TestBatch6Endpoints:
    def test_all_six_are_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"topological_sort", "counting_sort", "prefix_sums",
                "next_greater_element", "edit_distance", "floyd_cycle"} <= ids

    def test_topological_sort_runs_over_the_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "topological_sort",
            "start": "A",
            "graph": {"nodes": [{"id": c} for c in "ABC"],
                      "edges": [["A", "B"], ["B", "C"]]},
        })
        assert r.status_code == 200
        assert r.json()["meta"]["order"] == ["A", "B", "C"]

    @pytest.mark.parametrize("algo", ["counting_sort", "prefix_sums",
                                      "next_greater_element", "floyd_cycle"])
    def test_array_algorithms_require_an_array(self, algo):
        r = client.post("/api/trace", json={"algorithm": algo})
        assert r.status_code == 400
        assert "array" in r.json()["detail"].lower()

    def test_edit_distance_requires_two_comma_separated_words(self):
        r = client.post("/api/trace", json={"algorithm": "edit_distance"})
        assert r.status_code == 400
        r = client.post("/api/trace",
                        json={"algorithm": "edit_distance", "text": "ONLYONE"})
        assert r.status_code == 400
        r = client.post("/api/trace",
                        json={"algorithm": "edit_distance", "text": "kitten,sitting"})
        assert r.status_code == 200
        assert r.json()["meta"]["result"] == 3

    def test_floyd_rejects_an_out_of_range_link_index(self):
        r = client.post("/api/trace", json={
            "algorithm": "floyd_cycle", "array": [1, 2, 3], "target": 9,
        })
        assert r.status_code == 400
        assert "links back to" in r.json()["detail"]

    def test_floyd_defaults_to_no_cycle_without_a_target(self):
        r = client.post("/api/trace",
                        json={"algorithm": "floyd_cycle", "array": [1, 2, 3]})
        assert r.status_code == 200
        assert r.json()["meta"]["has_cycle"] is False
