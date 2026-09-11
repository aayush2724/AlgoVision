from fastapi.testclient import TestClient

from app.main import app
from app.tracers import knapsack_01, lcs

client = TestClient(app)


class TestKnapsack:
    def test_classic_case(self):
        # items (w, v); capacity 8 → best is 3:4 + 5:6 = 10
        res = knapsack_01.trace([(2, 3), (3, 4), (4, 5), (5, 6)], 8)
        assert res["meta"]["result"] == 10
        grid = res["steps"][-1]["structures"]["grid"]
        assert grid[4][8] == 10

    def test_every_cell_filled(self):
        res = knapsack_01.trace([(2, 3), (3, 4)], 5)
        grid = res["steps"][-1]["structures"]["grid"]
        assert all(v is not None for row in grid for v in row)

    def test_item_too_heavy_never_taken(self):
        res = knapsack_01.trace([(9, 100)], 5)
        assert res["meta"]["result"] == 0

    def test_grid_monotone_along_rows(self):
        # more capacity can never hurt
        res = knapsack_01.trace([(2, 3), (3, 4), (4, 5)], 7)
        grid = res["steps"][-1]["structures"]["grid"]
        for row in grid:
            assert all(row[c] <= row[c + 1] for c in range(len(row) - 1))

    def test_counts_and_labels(self):
        res = knapsack_01.trace([(2, 3), (3, 4)], 4)
        assert res["steps"][-1]["structures"]["counts"]["cells"] == 2 * 5
        assert len(res["meta"]["row_labels"]) == 3
        assert len(res["meta"]["col_labels"]) == 5


class TestLCS:
    def test_classic_case(self):
        res = lcs.trace("ABCBDAB", "BDCAB")
        assert len(res["meta"]["result"]) == 4  # e.g. BDAB / BCAB
        grid = res["steps"][-1]["structures"]["grid"]
        assert grid[7][5] == 4

    def test_result_is_subsequence_of_both(self):
        res = lcs.trace("ABCBDAB", "BDCAB")
        sub = res["meta"]["result"]

        def is_subseq(s, t):
            it = iter(t)
            return all(c in it for c in s)

        assert is_subseq(sub, "ABCBDAB")
        assert is_subseq(sub, "BDCAB")

    def test_no_common(self):
        res = lcs.trace("ABC", "XYZ")
        assert res["meta"]["result"] == ""
        assert res["steps"][-1]["structures"]["grid"][3][3] == 0

    def test_identical_strings(self):
        res = lcs.trace("HELLO", "HELLO")
        assert res["meta"]["result"] == "HELLO"

    def test_traceback_path_recorded(self):
        res = lcs.trace("ABC", "AC")
        path = res["steps"][-1]["structures"]["path"]
        assert len(path) == 2  # A and C


class TestBatch4Endpoints:
    def test_knapsack_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "knapsack_01", "text": "2:3,3:4,4:5,5:6", "target": 8})
        assert r.status_code == 200
        assert r.json()["meta"]["result"] == 10
        assert r.json()["meta"]["view"] == "grid"

    def test_knapsack_validation(self):
        bad = [
            {"text": "2:3"},                                # missing capacity
            {"text": "abc", "target": 5},                   # malformed pairs
            {"text": "2:3", "target": 11},                  # capacity too big
            {"text": ",".join(["2:3"] * 7), "target": 5},   # too many items
            {"text": "0:5", "target": 5},                   # zero weight
        ]
        for payload in bad:
            r = client.post("/api/trace", json={"algorithm": "knapsack_01", **payload})
            assert r.status_code == 400, payload

    def test_lcs_api(self):
        r = client.post("/api/trace", json={"algorithm": "lcs", "text": "abcbdab, bdcab"})
        assert r.status_code == 200
        assert len(r.json()["meta"]["result"]) == 4  # case-normalised upstream

    def test_lcs_validation(self):
        for text in (None, "ONLYONE", "TOOLONGWORD9,AB", "AB,({)"):
            payload = {"algorithm": "lcs"}
            if text is not None:
                payload["text"] = text
            assert client.post("/api/trace", json=payload).status_code == 400, text

    def test_algorithms_listing_has_batch4_set(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"knapsack_01", "lcs"} <= ids

    def test_detect_grid_metas(self):
        for problem, scene in [("knapsack_01", "vault"), ("lcs", "dna")]:
            r = client.post("/api/detect", json={"code": "", "problem": problem})
            assert r.json()["algorithm"] == problem
            assert r.json()["realworld"]["scene"] == scene
