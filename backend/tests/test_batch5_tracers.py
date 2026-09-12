from fastapi.testclient import TestClient

from app.main import app
from app.tracers import kruskals_mst, prims_mst
from app.tracers.common import Graph

client = TestClient(app)

GRAPH = Graph(
    nodes=[{"id": c} for c in "ABCDEF"],
    edges=[
        ["A", "B", 4], ["A", "C", 2], ["B", "C", 1], ["B", "D", 5],
        ["C", "D", 8], ["C", "E", 10], ["D", "E", 2], ["D", "F", 6],
        ["E", "F", 3],
    ],
)
# Minimum spanning tree: B-C(1), A-C(2), D-E(2), E-F(3), B-D(5) = 13
EXPECTED_COST = 13


def _final(res):
    return res["steps"][-1]["structures"]


class TestPrims:
    def test_total_cost_is_minimum(self):
        assert prims_mst.trace(GRAPH, "A")["meta"]["total_weight"] == EXPECTED_COST

    def test_spans_every_node_with_n_minus_1_edges(self):
        res = prims_mst.trace(GRAPH, "A")
        final = _final(res)
        assert len(final["mst_edges"]) == len(GRAPH.nodes) - 1
        assert sorted(final["visited"]) == sorted(n.id for n in GRAPH.nodes)

    def test_cost_independent_of_start_node(self):
        costs = {n.id: prims_mst.trace(GRAPH, n.id)["meta"]["total_weight"]
                 for n in GRAPH.nodes}
        assert set(costs.values()) == {EXPECTED_COST}, costs

    def test_tree_is_acyclic_and_connected(self):
        # n-1 edges + all nodes reachable ⇒ a tree
        final = _final(prims_mst.trace(GRAPH, "A"))
        adj = {}
        for a, b in final["mst_edges"]:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        seen, stack = set(), ["A"]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack.extend(adj.get(u, []))
        assert seen == {n.id for n in GRAPH.nodes}

    def test_disconnected_graph_reports_unreachable(self):
        g = Graph(nodes=[{"id": "A"}, {"id": "B"}, {"id": "X"}],
                  edges=[["A", "B", 1]])
        res = prims_mst.trace(g, "A")
        assert "unreachable" in res["steps"][-1]["note"].lower()
        assert len(_final(res)["mst_edges"]) == 1

    def test_counts_present(self):
        final = _final(prims_mst.trace(GRAPH, "A"))
        assert final["counts"]["edges_added"] == len(GRAPH.nodes) - 1
        assert final["counts"]["edge_checks"] > 0


class TestKruskals:
    def test_same_minimum_as_prims(self):
        assert kruskals_mst.trace(GRAPH)["meta"]["total_weight"] == EXPECTED_COST

    def test_n_minus_1_edges(self):
        final = _final(kruskals_mst.trace(GRAPH))
        assert len(final["mst_edges"]) == len(GRAPH.nodes) - 1

    def test_ends_in_single_component(self):
        final = _final(kruskals_mst.trace(GRAPH))
        assert len(final["components"]) == 1

    def test_rejects_cycle_edges(self):
        # Triangle A-B-C plus a tail to D. The tree is not complete when A-C
        # comes up, so the cycle edge is genuinely examined and rejected.
        # (On a bare triangle Kruskal's stops at n-1 edges and never sees it.)
        g = Graph(nodes=[{"id": c} for c in "ABCD"],
                  edges=[["A", "B", 1], ["B", "C", 2], ["A", "C", 3],
                         ["C", "D", 4]])
        res = kruskals_mst.trace(g)
        assert res["meta"]["total_weight"] == 7  # 1 + 2 + 4, skipping A-C(3)
        assert _final(res)["counts"]["cycles_skipped"] == 1

    def test_edges_taken_in_nondecreasing_weight(self):
        res = kruskals_mst.trace(GRAPH)
        weights = {frozenset((str(e[0]), str(e[1]))): float(e[2])
                   for e in GRAPH.edges}
        taken = [weights[frozenset(e)] for e in _final(res)["mst_edges"]]
        assert taken == sorted(taken)

    def test_disconnected_yields_forest(self):
        g = Graph(nodes=[{"id": c} for c in "ABXY"],
                  edges=[["A", "B", 1], ["X", "Y", 2]])
        res = kruskals_mst.trace(g)
        final = _final(res)
        assert len(final["components"]) == 2
        assert "forest" in res["steps"][-1]["note"].lower()

    def test_no_edges(self):
        g = Graph(nodes=[{"id": "A"}, {"id": "B"}], edges=[])
        res = kruskals_mst.trace(g)
        assert res["meta"]["total_weight"] == 0
        assert _final(res)["mst_edges"] == []


class TestBatch5Endpoints:
    PAYLOAD = {
        "nodes": [{"id": c} for c in "ABCDEF"],
        "edges": [["A", "B", 4], ["A", "C", 2], ["B", "C", 1], ["B", "D", 5],
                  ["C", "D", 8], ["C", "E", 10], ["D", "E", 2], ["D", "F", 6],
                  ["E", "F", 3]],
    }

    def test_prims_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "prims_mst", "start": "A", "graph": self.PAYLOAD})
        assert r.status_code == 200
        assert r.json()["meta"]["total_weight"] == EXPECTED_COST
        assert r.json()["meta"]["view"] == "graph"

    def test_kruskals_api(self):
        r = client.post("/api/trace", json={
            "algorithm": "kruskals_mst", "start": "A", "graph": self.PAYLOAD})
        assert r.status_code == 200
        assert r.json()["meta"]["total_weight"] == EXPECTED_COST

    def test_mst_requires_graph(self):
        r = client.post("/api/trace", json={
            "algorithm": "prims_mst", "array": [1, 2, 3]})
        assert r.status_code == 400

    def test_prims_validates_start_node(self):
        r = client.post("/api/trace", json={
            "algorithm": "prims_mst", "start": "Z", "graph": self.PAYLOAD})
        assert r.status_code == 400

    def test_algorithms_listing_has_batch5_set(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"prims_mst", "kruskals_mst"} <= ids
        # A lower bound, not an exact count — later batches keep adding.
        assert len(ids) >= 22

    def test_detect_mst_metas(self):
        for problem in ("prims_mst", "kruskals_mst"):
            r = client.post("/api/detect", json={"code": "", "problem": problem})
            assert r.json()["algorithm"] == problem
            assert r.json()["realworld"]["scene"] == "grid_power"
