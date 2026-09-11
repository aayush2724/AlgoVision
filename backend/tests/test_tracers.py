import pytest
from pydantic import ValidationError

from app.tracers import bfs, dijkstra
from app.tracers.common import Graph, MAX_NODES


def sample_graph():
    return Graph(
        nodes=[
            {"id": "A"}, {"id": "B"}, {"id": "C"},
            {"id": "D"}, {"id": "E"},
        ],
        edges=[
            ["A", "B", 4], ["A", "C", 2], ["B", "D", 5],
            ["C", "D", 8], ["C", "E", 10], ["D", "E", 2],
        ],
    )


def final_dist(result):
    return result["steps"][-1]["structures"]["dist"]


class TestDijkstra:
    def test_shortest_distances(self):
        res = dijkstra.trace(sample_graph(), "A")
        dist = final_dist(res)
        assert dist["A"] == 0
        assert dist["B"] == 4
        assert dist["C"] == 2
        assert dist["D"] == 9   # A→B→D beats A→C→D
        assert dist["E"] == 11  # A→B→D→E beats A→C→E

    def test_unreachable_node_is_none(self):
        g = Graph(nodes=[{"id": "A"}, {"id": "B"}, {"id": "X"}],
                  edges=[["A", "B", 1]])
        dist = final_dist(dijkstra.trace(g, "A"))
        assert dist["X"] is None

    def test_meta_and_step_shape(self):
        res = dijkstra.trace(sample_graph(), "A")
        assert res["meta"]["algorithm"] == "dijkstra"
        for step in res["steps"]:
            assert {"i", "structures", "highlight", "note"} <= step.keys()


class TestBFS:
    def test_visits_all_reachable(self):
        res = bfs.trace(sample_graph(), "A")
        visited = res["steps"][-1]["structures"]["visited"]
        assert sorted(visited) == ["A", "B", "C", "D", "E"]

    def test_start_only_component(self):
        g = Graph(nodes=[{"id": "A"}, {"id": "B"}], edges=[])
        res = bfs.trace(g, "A")
        assert res["steps"][-1]["structures"]["visited"] == ["A"]


class TestGraphValidation:
    def test_rejects_edge_to_unknown_node(self):
        with pytest.raises(ValidationError):
            Graph(nodes=[{"id": "A"}], edges=[["A", "Z", 1]])

    def test_rejects_negative_weight(self):
        with pytest.raises(ValidationError):
            Graph(nodes=[{"id": "A"}, {"id": "B"}], edges=[["A", "B", -1]])

    def test_rejects_too_many_nodes(self):
        nodes = [{"id": f"n{i}"} for i in range(MAX_NODES + 1)]
        with pytest.raises(ValidationError):
            Graph(nodes=nodes, edges=[])
