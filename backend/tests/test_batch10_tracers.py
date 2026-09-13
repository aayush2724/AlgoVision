"""Batch 10 — graph-family tracers that reuse existing views:
connected components, bipartite check (both on the graph view), and flood
fill (on the grid view).

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random
from collections import deque

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import bipartite_check, connected_components, flood_fill
from app.tracers.common import Graph

client = TestClient(app)

ENVELOPE = {"i", "line", "structures", "highlight", "note"}


def _assert_envelope(res):
    """Every step carries the shared envelope and monotonic counters."""
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


# ── CONNECTED COMPONENTS ──────────────────────────────────────────────────

def _brute_components(nodes, edges):
    adj = {n: set() for n in nodes}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen, groups = set(), []
    for n in sorted(nodes):
        if n in seen:
            continue
        comp, stack = [], [n]
        seen.add(n)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        groups.append(sorted(comp))
    return sorted(groups)


class TestConnectedComponents:
    def test_two_islands(self):
        res = connected_components.trace(
            _graph("ABCDE", [("A", "B"), ("C", "D")]), "A")
        assert res["meta"]["component_count"] == 3  # AB, CD, E
        assert sorted(res["meta"]["components"]) == [["A", "B"], ["C", "D"], ["E"]]

    def test_fully_connected_is_one_component(self):
        res = connected_components.trace(
            _graph("ABC", [("A", "B"), ("B", "C")]), "A")
        assert res["meta"]["component_count"] == 1

    def test_no_edges_is_all_singletons(self):
        res = connected_components.trace(_graph("ABCD", []), "A")
        assert res["meta"]["component_count"] == 4

    def test_single_node(self):
        res = connected_components.trace(_graph("A", []), "A")
        assert res["meta"]["components"] == [["A"]]
        _assert_envelope(res)

    def test_start_node_component_is_traced_first(self):
        res = connected_components.trace(
            _graph("ABCD", [("A", "B"), ("C", "D")]), "C")
        # The first node highlighted after the intro is the chosen start.
        assert res["steps"][1]["highlight"]["node"] == "C"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nodes = [chr(65 + i) for i in range(rng.randint(1, 7))]
        edges = [(rng.choice(nodes), rng.choice(nodes))
                 for _ in range(rng.randint(0, 8))]
        edges = [(a, b) for a, b in edges if a != b]  # common.py allows loops,
        # but a self-loop is meaningless to component grouping either way.
        res = connected_components.trace(_graph(nodes, edges), nodes[0])
        assert sorted(res["meta"]["components"]) == _brute_components(nodes, edges)
        _assert_envelope(res)

    def test_every_node_lands_in_exactly_one_component(self):
        res = connected_components.trace(
            _graph("ABCDEF", [("A", "B"), ("B", "C"), ("D", "E")]), "A")
        flat = [n for comp in res["meta"]["components"] for n in comp]
        assert sorted(flat) == list("ABCDEF")


# ── BIPARTITE CHECK ───────────────────────────────────────────────────────

def _brute_bipartite(nodes, edges):
    adj = {n: set() for n in nodes}
    for a, b in edges:
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    color = {}
    for src in nodes:
        if src in color:
            continue
        color[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False
    return True


class TestBipartiteCheck:
    def test_even_cycle_is_bipartite(self):
        # A square A-B-C-D-A: 4-cycle, two clean sides.
        res = bipartite_check.trace(
            _graph("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]), "A")
        assert res["meta"]["bipartite"] is True

    def test_odd_cycle_is_not_bipartite(self):
        # A triangle cannot be 2-coloured.
        res = bipartite_check.trace(
            _graph("ABC", [("A", "B"), ("B", "C"), ("C", "A")]), "A")
        assert res["meta"]["bipartite"] is False
        assert res["meta"]["conflict_edge"] is not None

    def test_tree_is_always_bipartite(self):
        res = bipartite_check.trace(
            _graph("ABCDE", [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E")]), "A")
        assert res["meta"]["bipartite"] is True

    def test_disconnected_one_odd_piece_fails_overall(self):
        res = bipartite_check.trace(
            _graph("ABCDE", [("A", "B"), ("C", "D"), ("D", "E"), ("E", "C")]), "A")
        assert res["meta"]["bipartite"] is False

    def test_single_node_is_bipartite(self):
        res = bipartite_check.trace(_graph("A", []), "A")
        assert res["meta"]["bipartite"] is True
        _assert_envelope(res)

    def test_colouring_is_valid_when_bipartite(self):
        edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]
        res = bipartite_check.trace(_graph("ABCD", edges), "A")
        coloring = res["meta"]["coloring"]
        for a, b in edges:
            assert coloring[a] != coloring[b], "an edge joined same-side nodes"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nodes = [chr(65 + i) for i in range(rng.randint(1, 7))]
        edges = [(rng.choice(nodes), rng.choice(nodes))
                 for _ in range(rng.randint(0, 9))]
        edges = [(a, b) for a, b in edges if a != b]
        res = bipartite_check.trace(_graph(nodes, edges), nodes[0])
        assert res["meta"]["bipartite"] == _brute_bipartite(nodes, edges)
        _assert_envelope(res)


# ── FLOOD FILL ────────────────────────────────────────────────────────────

def _brute_flood(rows, cols, walls, start):
    walls = {tuple(w) for w in walls}
    sr, sc = start
    if not (0 <= sr < rows and 0 <= sc < cols) or (sr, sc) in walls:
        return set()
    seen = {(sr, sc)}
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in walls and (nr, nc) not in seen):
                seen.add((nr, nc))
                stack.append((nr, nc))
    return seen


class TestFloodFill:
    def test_open_grid_fills_everything(self):
        res = flood_fill.trace(3, 3, [], (0, 0))
        assert res["meta"]["filled_count"] == 9

    def test_wall_partitions_the_canvas(self):
        # A full column of walls at c=1 seals the left strip from the rest.
        walls = [(0, 1), (1, 1), (2, 1)]
        res = flood_fill.trace(3, 3, walls, (0, 0))
        assert res["meta"]["filled_count"] == 3  # only column 0

    def test_start_on_a_wall_fills_nothing(self):
        res = flood_fill.trace(3, 3, [(1, 1)], (1, 1))
        assert res["meta"]["filled_count"] == 0
        _assert_envelope(res)

    def test_diagonal_neighbours_do_not_connect(self):
        # (0,0) and (1,1) touch only at a corner — 4-connectivity keeps them apart.
        walls = [(0, 1), (1, 0)]
        res = flood_fill.trace(2, 2, walls, (0, 0))
        assert res["meta"]["filled_count"] == 1

    def test_filled_cells_match_the_region(self):
        walls = [(0, 1), (1, 1), (2, 1)]
        res = flood_fill.trace(3, 3, walls, (0, 0))
        got = {tuple(c) for c in res["meta"]["filled"]}
        assert got == _brute_flood(3, 3, walls, (0, 0))

    def test_grid_is_rectangular_at_every_step(self):
        for s in flood_fill.trace(4, 4, [(1, 1), (2, 2)], (0, 0))["steps"]:
            grid = s["structures"]["grid"]
            assert len({len(row) for row in grid}) == 1, "ragged grid"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        side = rng.randint(2, flood_fill.MAX_SIDE)
        cells = [(r, c) for r in range(side) for c in range(side)]
        walls = rng.sample(cells, rng.randint(0, side))
        start = rng.choice(cells)
        res = flood_fill.trace(side, side, walls, start)
        expected = _brute_flood(side, side, walls, start)
        assert {tuple(c) for c in res["meta"]["filled"]} == expected
        assert res["meta"]["filled_count"] == len(expected)
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"connected_components", "bipartite_check", "flood_fill"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "connected_components", "start": "A",
         "graph": {"nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
                   "edges": [["A", "B"]]}},
        {"algorithm": "bipartite_check", "start": "A",
         "graph": {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [["A", "B"]]}},
        {"algorithm": "flood_fill", "target": 3},
        {"algorithm": "flood_fill", "target": 4, "start": "1:1",
         "text": "0:1,1:0"},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "connected_components",
          "array": [1, 2]}, "requires a 'graph'"),
        ({"algorithm": "flood_fill"}, "requires 'target'"),
        ({"algorithm": "flood_fill", "target": 99}, "between 2 and"),
        ({"algorithm": "flood_fill", "target": 3, "start": "5:5"}, "within"),
        ({"algorithm": "flood_fill", "target": 3, "start": "0:0",
          "text": "0:0"}, "cannot be a wall"),
        ({"algorithm": "flood_fill", "target": 3, "text": "oops"}, "row:col"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id", [
        "connected_components", "bipartite_check", "flood_fill",
    ])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
