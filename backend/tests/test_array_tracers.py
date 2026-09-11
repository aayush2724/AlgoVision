from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import binary_search, merge_sort

client = TestClient(app)


class TestBinarySearchTracer:
    def test_found(self):
        res = binary_search.trace([1, 3, 5, 7, 9], 7)
        last = res["steps"][-1]["structures"]
        assert last["found"] is True
        assert res["steps"][-1]["highlight"]["index"] == 3
        assert res["meta"]["view"] == "array"

    def test_not_found(self):
        res = binary_search.trace([1, 3, 5, 7, 9], 4)
        assert res["steps"][-1]["structures"]["found"] is False

    def test_empty_array(self):
        res = binary_search.trace([], 5)
        assert res["steps"][-1]["structures"]["found"] is False

    def test_single_element(self):
        assert binary_search.trace([5], 5)["steps"][-1]["structures"]["found"] is True
        assert binary_search.trace([5], 6)["steps"][-1]["structures"]["found"] is False

    def test_duplicates_found(self):
        res = binary_search.trace([2, 2, 2, 2], 2)
        assert res["steps"][-1]["structures"]["found"] is True

    def test_window_narrows_monotonically(self):
        res = binary_search.trace([1, 2, 3, 4, 5, 6, 7, 8], 6)
        lows = [s["structures"]["low"] for s in res["steps"]]
        highs = [s["structures"]["high"] for s in res["steps"]]
        assert lows == sorted(lows)
        assert highs == sorted(highs, reverse=True)


class TestMergeSortTracer:
    def test_final_array_sorted(self):
        res = merge_sort.trace([7, 3, 9, 1, 12, 5])
        assert res["steps"][-1]["structures"]["array"] == [1, 3, 5, 7, 9, 12]

    def test_every_step_is_permutation_of_input(self):
        data = [4, 1, 3, 2, 4]
        res = merge_sort.trace(data)
        for step in res["steps"]:
            assert Counter(step["structures"]["array"]) == Counter(data)

    def test_empty_and_single(self):
        assert merge_sort.trace([])["steps"][-1]["structures"]["array"] == []
        assert merge_sort.trace([9])["steps"][-1]["structures"]["array"] == [9]

    def test_sorted_ranges_end_covering_whole(self):
        res = merge_sort.trace([5, 2, 8, 1])
        assert [0, 3] in res["steps"][-1]["structures"]["sorted_ranges"]

    def test_original_array_preserved_in_result(self):
        res = merge_sort.trace([3, 1, 2])
        assert res["array"] == [3, 1, 2]

    def test_stability_order_of_equal_keys(self):
        # left value wins ties (a <= b) — merge sort must be stable
        res = merge_sort.trace([2, 2, 1])
        assert res["steps"][-1]["structures"]["array"] == [1, 2, 2]


class TestArrayEndpoints:
    def test_binary_search_ok(self):
        r = client.post("/api/trace", json={
            "algorithm": "binary_search",
            "array": [1, 3, 5, 7], "target": 5,
        })
        assert r.status_code == 200
        body = r.json()
        assert body["meta"]["view"] == "array"
        assert body["steps"][-1]["structures"]["found"] is True

    def test_binary_search_requires_target(self):
        r = client.post("/api/trace", json={
            "algorithm": "binary_search", "array": [1, 2, 3],
        })
        assert r.status_code == 400

    def test_binary_search_rejects_unsorted(self):
        r = client.post("/api/trace", json={
            "algorithm": "binary_search", "array": [3, 1, 2], "target": 2,
        })
        assert r.status_code == 400

    def test_merge_sort_ok(self):
        r = client.post("/api/trace", json={
            "algorithm": "merge_sort", "array": [4, 2, 7, 1],
        })
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["array"] == [1, 2, 4, 7]

    def test_merge_sort_rejects_long_array(self):
        r = client.post("/api/trace", json={
            "algorithm": "merge_sort", "array": list(range(17)),
        })
        assert r.status_code == 400

    def test_graph_algo_requires_graph(self):
        r = client.post("/api/trace", json={
            "algorithm": "bfs", "array": [1, 2, 3],
        })
        assert r.status_code == 400

    def test_rejects_graph_and_array_together(self):
        r = client.post("/api/trace", json={
            "algorithm": "bfs",
            "graph": {"nodes": [{"id": "A"}], "edges": []},
            "array": [1, 2],
        })
        assert r.status_code == 400

    def test_rejects_out_of_range_values(self):
        r = client.post("/api/trace", json={
            "algorithm": "merge_sort", "array": [2_000_000, 1],
        })
        assert r.status_code == 400

    def test_algorithms_listing_includes_array_algos(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"dijkstra", "bfs", "binary_search", "merge_sort"} <= ids

    def test_detect_returns_meta_for_algorithm_id(self):
        r = client.post("/api/detect", json={"code": "", "problem": "merge_sort"})
        assert r.status_code == 200
        assert r.json()["algorithm"] == "merge_sort"
