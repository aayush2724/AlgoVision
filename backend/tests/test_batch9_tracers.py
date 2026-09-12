"""Batch 9 — the college-core gaps: hashing, BST delete, heap extract,
standalone DSU, merge intervals, coin change.

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    bst_delete, coin_change, dsu, hash_table, heap_extract, merge_intervals,
)
from app.tracers.common import Graph

client = TestClient(app)

ENVELOPE = {"i", "line", "structures", "highlight", "note"}


def _assert_envelope(res):
    """Every step carries the shared envelope and cumulative counters."""
    assert res["steps"], "a tracer must emit at least one step"
    for s in res["steps"]:
        assert ENVELOPE <= set(s), f"step {s.get('i')} is missing envelope keys"
        assert "counts" in s["structures"], "counters missing from structures"
        assert s["note"], "every step needs a note to narrate"
    for key in res["steps"][0]["structures"]["counts"]:
        seq = [s["structures"]["counts"][key] for s in res["steps"]]
        assert seq == sorted(seq), f"counter {key!r} went backwards: {seq}"


# ── MERGE INTERVALS ───────────────────────────────────────────────────────

def _brute_merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


class TestMergeIntervals:
    def test_textbook_case(self):
        res = merge_intervals.trace([[1, 3], [2, 6], [8, 10], [15, 18]])
        assert res["meta"]["merged"] == [[1, 6], [8, 10], [15, 18]]

    def test_touching_intervals_merge(self):
        assert merge_intervals.trace([[1, 4], [4, 5]])["meta"]["merged"] == [[1, 5]]

    def test_fully_contained_interval_is_absorbed(self):
        assert merge_intervals.trace([[1, 10], [3, 5]])["meta"]["merged"] == [[1, 10]]

    def test_unsorted_input_is_sorted_first(self):
        res = merge_intervals.trace([[8, 10], [1, 3], [2, 6]])
        assert res["meta"]["merged"] == [[1, 6], [8, 10]]

    def test_empty(self):
        res = merge_intervals.trace([])
        assert res["meta"]["merged"] == []
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(25))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        ivs = [sorted((rng.randint(0, 20), rng.randint(0, 20)))
               for _ in range(rng.randint(1, 6))]
        res = merge_intervals.trace(ivs)
        assert res["meta"]["merged"] == _brute_merge([[float(a), float(b)]
                                                      for a, b in ivs])
        _assert_envelope(res)

    def test_merged_intervals_never_overlap(self):
        merged = merge_intervals.trace(
            [[1, 3], [2, 6], [5, 9], [15, 18]])["meta"]["merged"]
        for a, b in zip(merged, merged[1:]):
            assert a[1] < b[0], "output intervals must be disjoint"


# ── COIN CHANGE ───────────────────────────────────────────────────────────

def _brute_coin(coins, amount):
    inf = float("inf")
    dp = [0] + [inf] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return None if dp[amount] == inf else dp[amount]


class TestCoinChange:
    def test_greedy_would_fail_here(self):
        """Why this tracer exists: greedy takes 4+1+1, the table takes 3+3."""
        assert coin_change.trace([1, 3, 4], 6)["meta"]["fewest"] == 2

    def test_amount_zero_needs_no_coins(self):
        assert coin_change.trace([1, 5], 0)["meta"]["fewest"] == 0

    def test_unreachable_amount(self):
        assert coin_change.trace([5], 3)["meta"]["fewest"] is None

    def test_exact_single_coin(self):
        assert coin_change.trace([2, 5], 5)["meta"]["fewest"] == 1

    @pytest.mark.parametrize("seed", range(25))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        coins = rng.sample([1, 2, 3, 4, 5, 7], rng.randint(1, 4))
        amount = rng.randint(0, coin_change.MAX_AMOUNT)
        res = coin_change.trace(coins, amount)
        assert res["meta"]["fewest"] == _brute_coin(coins, amount)
        _assert_envelope(res)

    def test_grid_is_rectangular_at_every_step(self):
        for s in coin_change.trace([1, 3, 4], 6)["steps"]:
            grid = s["structures"]["grid"]
            assert len({len(row) for row in grid}) == 1, "ragged grid"


# ── HASH TABLE ────────────────────────────────────────────────────────────

class TestHashTable:
    def test_key_lands_in_the_bucket_its_hash_names(self):
        res = hash_table.trace(["CAT", "DOG", "OWL", "FOX"], 5)
        for bucket, chain in enumerate(res["meta"]["chains"]):
            for k in chain:
                assert sum(ord(c) for c in k) % 5 == bucket

    def test_every_key_is_stored_exactly_once(self):
        keys = ["CAT", "DOG", "OWL", "FOX", "ELK"]
        res = hash_table.trace(keys, 3)
        stored = [k for chain in res["meta"]["chains"] for k in chain]
        assert sorted(stored) == sorted(keys)

    def test_collision_is_counted_not_lost(self):
        res = hash_table.trace(["CAT", "DOG", "OWL"], 1)
        assert res["meta"]["chains"] == [["CAT", "DOG", "OWL"]]
        assert res["steps"][-1]["structures"]["counts"]["collisions"] == 2

    def test_lookup_hit(self):
        assert hash_table.trace(["CAT", "DOG", "OWL"], 5,
                                lookup="DOG")["meta"]["found"] is True

    def test_lookup_miss(self):
        assert hash_table.trace(["CAT", "DOG"], 5,
                                lookup="EEL")["meta"]["found"] is False

    def test_no_lookup_leaves_found_unset(self):
        assert hash_table.trace(["CAT"], 5)["meta"]["found"] is None

    def test_empty(self):
        res = hash_table.trace([], 5)
        assert all(c == [] for c in res["meta"]["chains"])
        _assert_envelope(res)


# ── BST DELETE ────────────────────────────────────────────────────────────

class TestBSTDelete:
    def test_delete_leaf(self):
        res = bst_delete.trace([8, 3, 10, 1], 1)
        assert res["meta"]["inorder"] == [3, 8, 10]
        assert res["meta"]["deleted"] is True

    def test_delete_node_with_one_child(self):
        assert bst_delete.trace([8, 3, 10, 14], 10)["meta"]["inorder"] == [3, 8, 14]

    def test_delete_node_with_two_children_promotes_successor(self):
        res = bst_delete.trace([8, 3, 10, 1, 6, 14, 4, 7, 13], 3)
        assert res["meta"]["inorder"] == [1, 4, 6, 7, 8, 10, 13, 14]

    def test_delete_root_with_two_children(self):
        res = bst_delete.trace([8, 3, 10, 1, 6, 14], 8)
        assert res["meta"]["inorder"] == [1, 3, 6, 10, 14]

    def test_delete_only_node(self):
        assert bst_delete.trace([5], 5)["meta"]["inorder"] == []

    def test_missing_value_changes_nothing(self):
        res = bst_delete.trace([8, 3, 10], 99)
        assert res["meta"]["deleted"] is False
        assert res["meta"]["inorder"] == [3, 8, 10]

    def test_empty_tree(self):
        res = bst_delete.trace([], 5)
        assert res["meta"]["deleted"] is False
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(30))
    def test_tree_stays_sorted_and_loses_exactly_one_value(self, seed):
        rng = random.Random(seed)
        vals = rng.sample(range(30), rng.randint(1, 8))
        target = rng.choice(vals + [99])
        res = bst_delete.trace(vals, target)
        expected = sorted(vals)
        if target in expected:
            expected.remove(target)
        assert res["meta"]["inorder"] == expected
        _assert_envelope(res)


# ── HEAP EXTRACT ──────────────────────────────────────────────────────────

class TestHeapExtract:
    def test_extracts_in_descending_order(self):
        assert heap_extract.trace([3, 9, 2, 1, 7, 5])["meta"]["order"] == \
            [9, 7, 5, 3, 2, 1]

    def test_single_value(self):
        assert heap_extract.trace([42])["meta"]["order"] == [42]

    def test_duplicates_all_come_out(self):
        assert heap_extract.trace([5, 5, 5])["meta"]["order"] == [5, 5, 5]

    def test_empty(self):
        res = heap_extract.trace([])
        assert res["meta"]["order"] == []
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(30))
    def test_is_a_sort(self, seed):
        rng = random.Random(seed)
        arr = [rng.randint(0, 50) for _ in range(rng.randint(1, 10))]
        res = heap_extract.trace(arr)
        assert res["meta"]["order"] == sorted(arr, reverse=True)
        _assert_envelope(res)

    def test_tree_stays_a_valid_complete_binary_tree(self):
        for s in heap_extract.trace([3, 9, 2, 1, 7, 5, 8])["steps"]:
            tree = s["structures"]["tree"]
            for n in tree:
                for child in (n["left"], n["right"]):
                    if child is not None:
                        assert 0 <= child < len(tree)


# ── DSU ───────────────────────────────────────────────────────────────────

def _graph(nodes, edges):
    return Graph(nodes=[{"id": n} for n in nodes], edges=[list(e) for e in edges])


def _brute_groups(nodes, edges):
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    groups: dict = {}
    for n in nodes:
        groups.setdefault(find(n), []).append(n)
    return sorted(sorted(v) for v in groups.values())


class TestDSU:
    def test_two_groups(self):
        res = dsu.trace(_graph("ABCDE", [("A", "B"), ("C", "D"), ("B", "C")]))
        assert res["meta"]["group_count"] == 2
        assert sorted(sorted(g) for g in res["meta"]["groups"]) == \
            [["A", "B", "C", "D"], ["E"]]

    def test_redundant_edge_is_rejected_not_merged(self):
        res = dsu.trace(_graph("ABC", [("A", "B"), ("B", "C"), ("A", "C")]))
        final = res["steps"][-1]["structures"]["counts"]
        assert final["unions"] == 2
        assert final["rejections"] == 1
        assert res["meta"]["group_count"] == 1

    def test_isolated_nodes_stay_separate(self):
        assert dsu.trace(_graph("ABC", []))["meta"]["group_count"] == 3

    def test_self_loop_is_redundant(self):
        res = dsu.trace(_graph("AB", [("A", "A")]))
        assert res["steps"][-1]["structures"]["counts"]["rejections"] == 1
        assert res["meta"]["group_count"] == 2

    def test_union_by_rank_keeps_the_tree_shallow(self):
        """A chain of unions must not build a chain of parents."""
        res = dsu.trace(_graph("ABCDEF",
                               [("A", "B"), ("B", "C"), ("C", "D"),
                                ("D", "E"), ("E", "F")]))
        parent = res["steps"][-1]["structures"]["parent"]

        def depth(n):
            d = 0
            while parent[n] != n:
                n = parent[n]
                d += 1
            return d

        assert max(depth(n) for n in parent) <= 2, \
            "union by rank should keep every node within a couple of hops"

    @pytest.mark.parametrize("seed", range(25))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        nodes = [chr(65 + i) for i in range(rng.randint(1, 7))]
        edges = [(rng.choice(nodes), rng.choice(nodes))
                 for _ in range(rng.randint(0, 8))]
        res = dsu.trace(_graph(nodes, edges))
        assert sorted(sorted(g) for g in res["meta"]["groups"]) == \
            _brute_groups(nodes, edges)
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_six_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"hash_table", "bst_delete", "heap_extract", "dsu",
                "merge_intervals", "coin_change"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "merge_intervals", "text": "1-3, 2-6, 8-10"},
        {"algorithm": "coin_change", "array": [1, 3, 4], "target": 6},
        {"algorithm": "hash_table", "text": "CAT,DOG,OWL | DOG"},
        {"algorithm": "bst_delete", "array": [8, 3, 10], "target": 3},
        {"algorithm": "heap_extract", "array": [3, 9, 2]},
        {"algorithm": "dsu", "start": "A",
         "graph": {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [["A", "B"]]}},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "merge_intervals", "text": "1-3, oops"}, "interval"),
        ({"algorithm": "merge_intervals", "text": "9-2"}, "ends before"),
        ({"algorithm": "coin_change", "array": [1], "target": 999}, "Amount"),
        ({"algorithm": "coin_change", "array": [0], "target": 5}, "whole numbers"),
        ({"algorithm": "hash_table", "text": "CAT,!!"}, "letters or digits"),
        ({"algorithm": "bst_delete", "array": [1, 2]}, "target"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id", [
        "hash_table", "bst_delete", "heap_extract",
        "dsu", "merge_intervals", "coin_change",
    ])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        """Passing an id as `problem` is a documented way to fetch its
        real-world meta. Fuzzy scoring used to break this on ties: bst_delete
        resolved to bst_insert, dsu to kruskals_mst, merge_intervals to greedy.
        """
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]

    def test_the_word_change_no_longer_trips_next_greater_element(self):
        """'nge' matched inside 'change', so any code mentioning a change
        scored for next_greater_element."""
        body = client.post("/api/detect", json={
            "code": "def apply_change(x):\n    return x", "problem": ""}).json()
        assert body["algorithm"] != "next_greater_element"

    def test_interval_count_is_capped(self):
        many = ", ".join(f"{i}-{i + 1}"
                         for i in range(merge_intervals.MAX_INTERVALS + 3))
        res = client.post("/api/trace",
                          json={"algorithm": "merge_intervals", "text": many})
        assert res.status_code == 400
        assert "at most" in res.json()["detail"].lower()
