from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    balanced_brackets, bubble_sort, insertion_sort, linked_list_reverse,
    selection_sort,
)

client = TestClient(app)

DATA = [7, 3, 9, 1, 12, 5]
SORTED = [1, 3, 5, 7, 9, 12]


class TestSimpleSorts:
    def test_all_three_sort_correctly(self):
        for mod in (bubble_sort, insertion_sort, selection_sort):
            res = mod.trace(DATA)
            assert res["steps"][-1]["structures"]["array"] == SORTED, mod.__name__

    def test_permutation_invariant(self):
        for mod in (bubble_sort, insertion_sort, selection_sort):
            for step in mod.trace(DATA)["steps"]:
                assert Counter(step["structures"]["array"]) == Counter(DATA)

    def test_edge_cases(self):
        for mod in (bubble_sort, insertion_sort, selection_sort):
            assert mod.trace([])["steps"][-1]["structures"]["array"] == []
            assert mod.trace([5])["steps"][-1]["structures"]["array"] == [5]
            assert mod.trace([2, 2, 2])["steps"][-1]["structures"]["array"] == [2, 2, 2]

    def test_bubble_early_exit_on_sorted_input(self):
        res = bubble_sort.trace([1, 2, 3, 4, 5])
        notes = " ".join(s["note"] for s in res["steps"])
        assert "Early exit" in notes
        # one pass of n-1 comparisons, no swaps
        final = res["steps"][-1]["structures"]["counts"]
        assert final["comparisons"] == 4
        assert final["swaps"] == 0

    def test_insertion_counts(self):
        final = insertion_sort.trace([3, 2, 1])["steps"][-1]["structures"]["counts"]
        assert final["inserts"] == 2
        assert final["shifts"] == 3  # worst case: 1 + 2

    def test_selection_comparisons_fixed(self):
        # selection sort always does n(n-1)/2 comparisons
        final = selection_sort.trace([4, 3, 2, 1])["steps"][-1]["structures"]["counts"]
        assert final["comparisons"] == 6

    def test_final_step_fully_sorted_ranges(self):
        for mod in (bubble_sort, insertion_sort, selection_sort):
            last = mod.trace(DATA)["steps"][-1]["structures"]
            covered = set()
            for lo, hi in last["sorted_ranges"]:
                covered.update(range(lo, hi + 1))
            assert covered == set(range(len(DATA))), mod.__name__


class TestLinkedListReverse:
    def test_pointers_fully_reversed(self):
        res = linked_list_reverse.trace([10, 20, 30, 40])
        last = res["steps"][-1]["structures"]
        # node 0 becomes tail (None), each other node points to its predecessor
        assert last["next"] == [None, 0, 1, 2]
        assert last["prev"] == 3  # new head
        assert last["counts"]["flips"] == 4

    def test_edge_cases(self):
        assert linked_list_reverse.trace([])["steps"][-1]["structures"]["values"] == []
        one = linked_list_reverse.trace([5])["steps"][-1]["structures"]
        assert one["next"] == [None]

    def test_view_is_list(self):
        assert linked_list_reverse.trace([1, 2])["meta"]["view"] == "list"


class TestBalancedBrackets:
    def test_balanced(self):
        res = balanced_brackets.trace("({[]})")
        last = res["steps"][-1]["structures"]
        assert last["balanced"] is True
        assert last["counts"]["pushes"] == 3
        assert last["counts"]["pops"] == 3

    def test_mismatch_stops_early(self):
        res = balanced_brackets.trace("(]")
        last = res["steps"][-1]["structures"]
        assert last["balanced"] is False
        assert last["action"] == "mismatch"

    def test_unclosed_openers(self):
        res = balanced_brackets.trace("((")
        last = res["steps"][-1]["structures"]
        assert last["balanced"] is False
        assert last["action"] == "done"

    def test_close_on_empty_stack(self):
        assert balanced_brackets.trace(")")["steps"][-1]["structures"]["balanced"] is False

    def test_empty_is_balanced(self):
        assert balanced_brackets.trace("")["steps"][-1]["structures"]["balanced"] is True


class TestBatch1Endpoints:
    def test_sorts_via_api(self):
        for algo in ("bubble_sort", "insertion_sort", "selection_sort"):
            r = client.post("/api/trace", json={"algorithm": algo, "array": [3, 1, 2]})
            assert r.status_code == 200, algo
            assert r.json()["steps"][-1]["structures"]["array"] == [1, 2, 3]

    def test_linked_list_via_api(self):
        r = client.post("/api/trace",
                        json={"algorithm": "linked_list_reverse", "array": [1, 2, 3]})
        assert r.status_code == 200
        assert r.json()["meta"]["view"] == "list"

    def test_linked_list_length_cap(self):
        r = client.post("/api/trace",
                        json={"algorithm": "linked_list_reverse", "array": list(range(11))})
        assert r.status_code == 400

    def test_brackets_via_api(self):
        r = client.post("/api/trace",
                        json={"algorithm": "balanced_brackets", "text": "([])"})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["balanced"] is True

    def test_brackets_validation(self):
        assert client.post("/api/trace",
                           json={"algorithm": "balanced_brackets"}).status_code == 400
        assert client.post("/api/trace",
                           json={"algorithm": "balanced_brackets",
                                 "text": "(abc)"}).status_code == 400
        assert client.post("/api/trace",
                           json={"algorithm": "balanced_brackets",
                                 "text": "(" * 21}).status_code == 400

    def test_algorithms_listing_has_twelve(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert len(ids) == 12
        assert {"bubble_sort", "insertion_sort", "selection_sort",
                "linked_list_reverse", "balanced_brackets"} <= ids

    def test_detect_new_metas(self):
        for problem, scene in [("bubble_sort", "leaderboard"),
                               ("linked_list_reverse", "train"),
                               ("balanced_brackets", "plates")]:
            r = client.post("/api/detect", json={"code": "", "problem": problem})
            assert r.json()["algorithm"] == problem
            assert r.json()["realworld"]["scene"] == scene
