from fastapi.testclient import TestClient

from app.main import app
from app.tracers import kadanes, sliding_window, two_sum_sorted

client = TestClient(app)


class TestTwoSumSorted:
    def test_found(self):
        res = two_sum_sorted.trace([1, 3, 5, 7, 9, 12], 16)
        last = res["steps"][-1]["structures"]
        assert last["found"] is True
        assert last["sum"] == 16

    def test_not_found(self):
        res = two_sum_sorted.trace([1, 3, 5, 7], 100)
        assert res["steps"][-1]["structures"]["found"] is False

    def test_single_pass_bound(self):
        # pointers converge: at most n-1 moves
        res = two_sum_sorted.trace([1, 2, 3, 4, 5, 6, 7, 8], 100)
        assert res["steps"][-1]["structures"]["counts"]["moves"] <= 7

    def test_too_few_values(self):
        assert two_sum_sorted.trace([5], 5)["steps"][-1]["structures"]["found"] is False

    def test_pointers_always_valid(self):
        for step in two_sum_sorted.trace([1, 2, 3, 4, 5], 6)["steps"]:
            s = step["structures"]
            if s["left"] is not None and s["right"] is not None:
                assert 0 <= s["left"] <= s["right"] <= 4


class TestSlidingWindow:
    def test_finds_best_window(self):
        # windows of 3: 15, 18, 17, 16, 15 — best is [1..3] = 2+9+7
        res = sliding_window.trace([4, 2, 9, 7, 1, 8, 6], 3)
        last = res["steps"][-1]["structures"]
        assert last["best"] == 18
        assert last["best_window"] == [1, 3]

    def test_k_equals_n(self):
        res = sliding_window.trace([1, 2, 3], 3)
        assert res["steps"][-1]["structures"]["best"] == 6

    def test_k_one_picks_max(self):
        res = sliding_window.trace([3, 9, 2], 1)
        assert res["steps"][-1]["structures"]["best"] == 9

    def test_additions_linear_not_quadratic(self):
        n, k = 10, 4
        res = sliding_window.trace(list(range(n)), k)
        adds = res["steps"][-1]["structures"]["counts"]["additions"]
        assert adds == k + (n - k)  # first window + one per slide
        assert adds < (n - k + 1) * k  # beats naive

    def test_negative_values(self):
        res = sliding_window.trace([-5, -1, -3], 2)
        assert res["steps"][-1]["structures"]["best"] == -4


class TestKadanes:
    def test_classic_leetcode_case(self):
        res = kadanes.trace([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        last = res["steps"][-1]["structures"]
        assert last["best"] == 6
        assert last["best_window"] == [3, 6]  # [4, -1, 2, 1]

    def test_all_negative(self):
        res = kadanes.trace([-8, -3, -6])
        last = res["steps"][-1]["structures"]
        assert last["best"] == -3
        assert last["best_window"] == [1, 1]

    def test_all_positive_takes_everything(self):
        res = kadanes.trace([1, 2, 3])
        assert res["steps"][-1]["structures"]["best_window"] == [0, 2]

    def test_restarts_counted(self):
        res = kadanes.trace([-2, 1, -3, 4])
        assert res["steps"][-1]["structures"]["counts"]["restarts"] >= 2

    def test_empty(self):
        assert kadanes.trace([])["steps"][-1]["structures"]["best"] is None


class TestBatch3Endpoints:
    def test_two_sum_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "two_sum_sorted", "array": [1, 3, 5, 7], "target": 8})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["found"] is True

    def test_two_sum_requires_sorted(self):
        r = client.post("/api/trace", json={
            "algorithm": "two_sum_sorted", "array": [5, 1, 3], "target": 8})
        assert r.status_code == 400

    def test_two_sum_requires_target(self):
        r = client.post("/api/trace", json={
            "algorithm": "two_sum_sorted", "array": [1, 2, 3]})
        assert r.status_code == 400

    def test_sliding_window_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "sliding_window", "array": [1, 2, 3, 4], "target": 2})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["best"] == 7

    def test_sliding_window_k_validation(self):
        for bad_k in (0, 5, 2.5):
            r = client.post("/api/trace", json={
                "algorithm": "sliding_window", "array": [1, 2, 3, 4], "target": bad_k})
            assert r.status_code == 400, bad_k

    def test_kadanes_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "kadanes", "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4]})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["best"] == 6

    def test_algorithms_listing_has_eighteen(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert len(ids) == 18
        assert {"two_sum_sorted", "sliding_window", "kadanes"} <= ids

    def test_detect_pattern_metas(self):
        for problem, scene in [("two_sum_sorted", "market"),
                               ("sliding_window", "stocks"),
                               ("kadanes", "stocks")]:
            r = client.post("/api/detect", json={"code": "", "problem": problem})
            assert r.json()["algorithm"] == problem
            assert r.json()["realworld"]["scene"] == scene
