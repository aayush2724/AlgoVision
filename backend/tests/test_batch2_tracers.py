from fastapi.testclient import TestClient

from app.main import app
from app.tracers import bst_insert, bst_search, heap_insert

client = TestClient(app)

DATA = [8, 3, 10, 1, 6, 14, 4]


class TestBSTInsert:
    def test_inorder_reads_sorted(self):
        res = bst_insert.trace(DATA)
        tree = res["steps"][-1]["structures"]["tree"]
        # serialize() is in-order — values must come out sorted
        values = [n["value"] for n in tree]
        assert values == sorted(DATA)
        assert res["meta"]["view"] == "tree"

    def test_all_values_present(self):
        tree = bst_insert.trace(DATA)["steps"][-1]["structures"]["tree"]
        assert sorted(n["value"] for n in tree) == sorted(DATA)
        assert len(tree) == len(DATA)

    def test_degenerate_on_sorted_input(self):
        res = bst_insert.trace([1, 2, 3, 4, 5])
        tree = res["steps"][-1]["structures"]["tree"]
        assert max(n["depth"] for n in tree) == 4  # a pure chain
        assert "height 5" in res["steps"][-1]["note"]

    def test_empty(self):
        res = bst_insert.trace([])
        assert res["steps"][-1]["structures"]["tree"] == []

    def test_counts(self):
        final = bst_insert.trace(DATA)["steps"][-1]["structures"]["counts"]
        assert final["insertions"] == len(DATA)
        assert final["comparisons"] > 0

    def test_layout_bounds(self):
        for step in bst_insert.trace(DATA)["steps"]:
            for n in step["structures"]["tree"]:
                assert 0.0 <= n["x"] <= 1.0
                assert n["depth"] >= 0


class TestBSTSearch:
    def test_found(self):
        res = bst_search.trace(DATA, 6)
        assert res["steps"][-1]["structures"]["found"] is True

    def test_not_found(self):
        res = bst_search.trace(DATA, 7)
        assert res["steps"][-1]["structures"]["found"] is False

    def test_search_shorter_than_full_scan(self):
        # balanced-ish tree: comparisons well below n
        final = bst_search.trace(DATA, 4)["steps"][-1]["structures"]["counts"]
        assert final["comparisons"] <= 4

    def test_empty_tree(self):
        assert bst_search.trace([], 5)["steps"][-1]["structures"]["found"] is False


class TestHeapInsert:
    def test_final_heap_property(self):
        res = heap_insert.trace(DATA)
        tree = {n["id"]: n for n in res["steps"][-1]["structures"]["tree"]}
        for n in tree.values():
            for child in (n["left"], n["right"]):
                if child is not None:
                    assert n["value"] >= tree[child]["value"]

    def test_root_is_max(self):
        tree = heap_insert.trace(DATA)["steps"][-1]["structures"]["tree"]
        root = next(n for n in tree if n["id"] == 0)
        assert root["value"] == max(DATA)

    def test_all_values_kept(self):
        tree = heap_insert.trace(DATA)["steps"][-1]["structures"]["tree"]
        assert sorted(n["value"] for n in tree) == sorted(DATA)

    def test_swaps_counted(self):
        # ascending input: every insert must bubble to the root
        final = heap_insert.trace([1, 2, 3, 4])["steps"][-1]["structures"]["counts"]
        assert final["swaps"] >= 3

    def test_empty(self):
        assert heap_insert.trace([])["steps"][-1]["structures"]["tree"] == []


class TestBatch2Endpoints:
    def test_bst_insert_api(self):
        r = client.post("/api/trace", json={"algorithm": "bst_insert", "array": DATA})
        assert r.status_code == 200
        assert r.json()["meta"]["view"] == "tree"

    def test_bst_search_api(self):
        r = client.post("/api/trace",
                        json={"algorithm": "bst_search", "array": DATA, "target": 10})
        assert r.status_code == 200
        assert r.json()["steps"][-1]["structures"]["found"] is True

    def test_bst_search_requires_target(self):
        r = client.post("/api/trace", json={"algorithm": "bst_search", "array": DATA})
        assert r.status_code == 400

    def test_heap_api(self):
        r = client.post("/api/trace", json={"algorithm": "heap_insert", "array": [3, 9, 5]})
        assert r.status_code == 200

    def test_tree_length_cap(self):
        r = client.post("/api/trace",
                        json={"algorithm": "bst_insert", "array": list(range(13))})
        assert r.status_code == 400

    def test_algorithms_listing_has_batch2_set(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"bst_insert", "bst_search", "heap_insert"} <= ids

    def test_detect_tree_metas(self):
        for problem, scene in [("bst_insert", "files"), ("heap_insert", "scheduler")]:
            r = client.post("/api/detect", json={"code": "", "problem": problem})
            assert r.json()["algorithm"] == problem
            assert r.json()["realworld"]["scene"] == scene
