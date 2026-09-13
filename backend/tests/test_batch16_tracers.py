"""Batch 16 (Tier B, part 1) — Bellman-Ford: directed, negative-weight-aware
single-source shortest paths with negative-cycle detection, on the graph view.

Also covers the shared graph-model change: negative edge weights are now
accepted by the model, but Dijkstra / Prim / Kruskal reject them at the route
layer so their contracts are unchanged.

The tracer is checked against an independent reference implementation.
"""

import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import bellman_ford
from app.tracers.common import Graph

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


def _graph(nodes, edges):
    return Graph(nodes=[{"id": n} for n in nodes], edges=[list(e) for e in edges])


def _ref_bellman_ford(nodes, edges, start):
    inf = float("inf")
    dist = {n: inf for n in nodes}
    dist[start] = 0.0
    for _ in range(len(nodes) - 1):
        for a, b, w in edges:
            if dist[a] != inf and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
    neg = any(dist[a] != inf and dist[a] + w < dist[b] for a, b, w in edges)
    fmt = {k: (None if v == inf else v) for k, v in dist.items()}
    return fmt, neg


class TestBellmanFord:
    def test_negative_edge_no_cycle(self):
        # A -> B (4), A -> C (5), C -> B (-3): shortest to B is via C = 2.
        res = bellman_ford.trace(
            _graph("ABC", [("A", "B", 4), ("A", "C", 5), ("C", "B", -3)]), "A")
        assert res["meta"]["dist"] == {"A": 0, "B": 2, "C": 5}
        assert res["meta"]["negative_cycle"] is False

    def test_edges_are_directed(self):
        # B -> A only; from A nothing is reachable but A itself.
        res = bellman_ford.trace(_graph("AB", [("B", "A", 5)]), "A")
        assert res["meta"]["dist"] == {"A": 0, "B": None}

    def test_negative_cycle_detected(self):
        # A -> B (1), B -> C (-2), C -> A (-2): a cycle summing to -3.
        res = bellman_ford.trace(
            _graph("ABC", [("A", "B", 1), ("B", "C", -2), ("C", "A", -2)]), "A")
        assert res["meta"]["negative_cycle"] is True

    def test_unreachable_node(self):
        res = bellman_ford.trace(
            _graph("ABC", [("A", "B", 3)]), "A")
        assert res["meta"]["dist"]["C"] is None

    def test_single_node(self):
        res = bellman_ford.trace(_graph("A", []), "A")
        assert res["meta"]["dist"] == {"A": 0}
        _assert_envelope(res)

    def test_early_stop_when_settled(self):
        # A linear chain settles in far fewer than V-1 rounds.
        res = bellman_ford.trace(
            _graph("ABCD", [("A", "B", 1), ("B", "C", 1), ("C", "D", 1)]), "A")
        assert res["meta"]["dist"] == {"A": 0, "B": 1, "C": 2, "D": 3}

    @pytest.mark.parametrize("seed", range(40))
    def test_matches_reference(self, seed):
        rng = random.Random(seed)
        nodes = [chr(65 + i) for i in range(rng.randint(1, 6))]
        edges = []
        for _ in range(rng.randint(0, 10)):
            a, b = rng.choice(nodes), rng.choice(nodes)
            if a != b:
                edges.append((a, b, rng.randint(-3, 6)))
        res = bellman_ford.trace(_graph(nodes, edges), nodes[0])
        ref_dist, ref_neg = _ref_bellman_ford(nodes, edges, nodes[0])
        assert res["meta"]["negative_cycle"] == ref_neg
        if not ref_neg:
            assert res["meta"]["dist"] == ref_dist
        _assert_envelope(res)


# ── SHARED MODEL CHANGE ───────────────────────────────────────────────────

class TestNegativeWeightModel:
    def test_model_now_accepts_negative_weights(self):
        # Previously the Graph model rejected these outright.
        g = _graph("AB", [("A", "B", -5)])
        assert g.edges == [["A", "B", -5]]

    def test_model_still_rejects_out_of_range(self):
        with pytest.raises(ValueError):
            _graph("AB", [("A", "B", -2_000_000)])

    @pytest.mark.parametrize("algo", ["dijkstra", "prims_mst", "kruskals_mst"])
    def test_nonnegative_algorithms_reject_negative_weights(self, algo):
        res = client.post("/api/trace", json={
            "algorithm": algo, "start": "A",
            "graph": {"nodes": [{"id": "A"}, {"id": "B"}],
                      "edges": [["A", "B", -3]]}})
        assert res.status_code == 400
        assert "non-negative" in res.json()["detail"].lower()

    def test_bfs_still_works_with_negative_weights(self):
        # BFS ignores weights, so a negative weight must not break it.
        res = client.post("/api/trace", json={
            "algorithm": "bfs", "start": "A",
            "graph": {"nodes": [{"id": "A"}, {"id": "B"}],
                      "edges": [["A", "B", -3]]}})
        assert res.status_code == 200


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_is_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert "bellman_ford" in ids

    def test_endpoint_returns_a_trace(self):
        res = client.post("/api/trace", json={
            "algorithm": "bellman_ford", "start": "A",
            "graph": {"nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
                      "edges": [["A", "B", 4], ["A", "C", 5], ["C", "B", -3]]}})
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"]
        assert body["meta"]["algorithm"] == "bellman_ford"
        assert body["meta"]["dist"]["B"] == 2

    def test_detect_resolves_id(self):
        body = client.post("/api/detect",
                           json={"code": "", "problem": "bellman_ford"}).json()
        assert body["algorithm"] == "bellman_ford"
        assert body["realworld"]["scene"]
        assert body["realworld"]["title"]
