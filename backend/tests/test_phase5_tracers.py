from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import dfs, fibonacci_dp, quick_sort
from app.tracers.common import Graph

client = TestClient(app)


def sample_graph():
    return Graph(
        nodes=[{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}, {"id": "X"}],
        edges=[["A", "B", 1], ["A", "C", 1], ["B", "D", 1]],
    )


class TestDFS:
    def test_visits_all_reachable(self):
        res = dfs.trace(sample_graph(), "A")
        visited = res["steps"][-1]["structures"]["visited"]
        assert sorted(visited) == ["A", "B", "C", "D"]  # X unreachable
        assert res["meta"]["view"] == "graph"

    def test_backtrack_steps_present(self):
        res = dfs.trace(sample_graph(), "A")
        notes = [s["note"] for s in res["steps"]]
        assert any("backtrack" in n.lower() for n in notes)
        final = res["steps"][-1]["structures"]["counts"]
        assert final["visits"] == 4
        assert final["backtracks"] == 4  # one pop per visited node

    def test_stack_empties_at_end(self):
        res = dfs.trace(sample_graph(), "A")
        assert res["steps"][-1]["structures"]["stack"] == []

    def test_goes_deep_before_wide(self):
        # From A (neighbors B, C sorted), DFS must reach D (via B) before C
        res = dfs.trace(sample_graph(), "A")
        order = [s["highlight"]["node"] for s in res["steps"]
                 if s["note"].startswith(("Start", "Go deeper"))]
        assert order.index("D") < order.index("C")


class TestQuickSort:
    def test_final_sorted(self):
        res = quick_sort.trace([7, 3, 9, 1, 12, 5])
        assert res["steps"][-1]["structures"]["array"] == [1, 3, 5, 7, 9, 12]

    def test_every_step_is_permutation(self):
        data = [4, 1, 3, 2, 4, 0]
        res = quick_sort.trace(data)
        for step in res["steps"]:
            assert Counter(step["structures"]["array"]) == Counter(data)

    def test_all_positions_locked(self):
        res = quick_sort.trace([5, 2, 8, 1])
        locked = {r[0] for r in res["steps"][-1]["structures"]["sorted_ranges"]}
        assert locked == {0, 1, 2, 3}

    def test_edge_cases(self):
        assert quick_sort.trace([])["steps"][-1]["structures"]["array"] == []
        assert quick_sort.trace([9])["steps"][-1]["structures"]["array"] == [9]
        assert quick_sort.trace([2, 2, 2])["steps"][-1]["structures"]["array"] == [2, 2, 2]

    def test_counts(self):
        res = quick_sort.trace([3, 1, 2])
        final = res["steps"][-1]["structures"]["counts"]
        assert final["comparisons"] >= 2
        assert final["partitions"] >= 1


class TestFibonacciDP:
    def test_correct_value(self):
        res = fibonacci_dp.trace(10)
        assert res["meta"]["result"] == 55
        table = res["steps"][-1]["structures"]["table"]
        assert table["10"] == 55 and table["0"] == 0 and table["1"] == 1

    def test_cache_hits_present(self):
        res = fibonacci_dp.trace(8)
        final = res["steps"][-1]["structures"]["counts"]
        assert final["cache_hits"] > 0
        assert final["computes"] == 9  # each of 0..8 computed exactly once
        assert any(s["structures"]["cache_hit"] for s in res["steps"])

    def test_base_cases(self):
        assert fibonacci_dp.trace(0)["meta"]["result"] == 0
        assert fibonacci_dp.trace(1)["meta"]["result"] == 1

    def test_view_is_table(self):
        assert fibonacci_dp.trace(5)["meta"]["view"] == "table"


class TestPhase5Endpoints:
    def test_dfs_endpoint(self):
        r = client.post("/api/trace", json={
            "algorithm": "dfs", "start": "A",
            "graph": {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [["A", "B", 1]]},
        })
        assert r.status_code == 200
        assert r.json()["meta"]["algorithm"] == "dfs"

    def test_quick_sort_endpoint(self):
        r = client.post("/api/trace", json={"algorithm": "quick_sort", "array": [3, 1, 2]})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["array"] == [1, 2, 3]

    def test_fibonacci_endpoint(self):
        r = client.post("/api/trace", json={"algorithm": "fibonacci_dp", "target": 7})
        assert r.status_code == 200
        assert r.json()["meta"]["result"] == 13

    def test_fibonacci_validation(self):
        assert client.post("/api/trace", json={"algorithm": "fibonacci_dp"}).status_code == 400
        assert client.post("/api/trace",
                           json={"algorithm": "fibonacci_dp", "target": 19}).status_code == 400
        assert client.post("/api/trace",
                           json={"algorithm": "fibonacci_dp", "target": 5.5}).status_code == 400
        assert client.post("/api/trace",
                           json={"algorithm": "fibonacci_dp", "target": -1}).status_code == 400

    def test_algorithms_listing_has_phase5_set(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"dijkstra", "bfs", "dfs", "binary_search",
                "merge_sort", "quick_sort", "fibonacci_dp"} <= ids

    def test_detect_quick_sort_meta(self):
        r = client.post("/api/detect", json={"code": "", "problem": "quick_sort"})
        assert r.json()["algorithm"] == "quick_sort"
        assert r.json()["realworld"]["scene"] == "leaderboard"
