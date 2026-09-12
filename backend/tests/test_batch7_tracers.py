"""Batch 7: tree traversals, trie, N-Queens, unique paths, sieve."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import n_queens, sieve, tree_traversal, trie_insert, unique_paths

client = TestClient(app)


def _final(res):
    return res["steps"][-1]["structures"]


# ── Tree traversals ───────────────────────────────────────────────────────

TREE = [8, 3, 10, 1, 6, 14, 4]


class TestTreeTraversal:
    def test_inorder_of_a_bst_is_sorted(self):
        res = tree_traversal.trace(TREE)
        inorder = [float(v) for v in res["meta"]["results"]["inorder"]]
        assert inorder == sorted(TREE)

    def test_preorder_starts_at_the_root(self):
        res = tree_traversal.trace(TREE)
        assert res["meta"]["results"]["preorder"][0] == "8"

    def test_postorder_ends_at_the_root(self):
        res = tree_traversal.trace(TREE)
        assert res["meta"]["results"]["postorder"][-1] == "8"

    def test_every_walk_visits_every_node_once(self):
        res = tree_traversal.trace(TREE)
        for mode, order in res["meta"]["results"].items():
            assert len(order) == len(TREE), mode
            assert sorted(float(v) for v in order) == sorted(TREE), mode

    def test_known_orders_for_a_known_tree(self):
        res = tree_traversal.trace(TREE)
        r = res["meta"]["results"]
        assert r["preorder"] == ["8", "3", "1", "6", "4", "10", "14"]
        assert r["postorder"] == ["1", "4", "6", "3", "14", "10", "8"]

    def test_single_node_and_empty(self):
        one = tree_traversal.trace([5])["meta"]["results"]
        assert one["inorder"] == one["preorder"] == one["postorder"] == ["5"]
        assert tree_traversal.trace([])["steps"]

    def test_tree_nodes_carry_layout_fields(self):
        node = _final(tree_traversal.trace(TREE))["tree"][0]
        assert {"id", "value", "depth", "x", "left", "right"} <= set(node)

    def test_view_is_tree(self):
        assert tree_traversal.trace(TREE)["meta"]["view"] == "tree"


# ── Trie ──────────────────────────────────────────────────────────────────

class TestTrieInsert:
    def test_shared_prefix_is_reused_not_duplicated(self):
        res = trie_insert.trace(["CAT", "CAR"])
        c = _final(res)["counts"]
        # C and A are shared; T and R branch. Root + C,A,T,R = 5 nodes.
        assert c["nodes_created"] == 4
        assert c["prefix_reuses"] == 2

    def test_disjoint_words_share_nothing(self):
        res = trie_insert.trace(["CAT", "DOG"])
        assert _final(res)["counts"]["prefix_reuses"] == 0
        assert _final(res)["counts"]["nodes_created"] == 6

    def test_node_count_matches_distinct_prefixes(self):
        words = ["CAT", "CAR", "DOG"]
        res = trie_insert.trace(words)
        distinct = {w[:i] for w in words for i in range(1, len(w) + 1)}
        # +1 for the root
        assert len(_final(res)["tree"]) == len(distinct) + 1

    def test_terminal_marker_distinguishes_word_from_prefix(self):
        # CAR is a whole word; CA is only a prefix.
        res = trie_insert.trace(["CAR"])
        values = [n["value"] for n in _final(res)["tree"]]
        assert "R▪" in values
        assert "A" in values and "A▪" not in values

    def test_a_word_that_is_a_prefix_of_another(self):
        res = trie_insert.trace(["CAR", "CARS"])
        assert _final(res)["counts"]["words_added"] == 2
        values = [n["value"] for n in _final(res)["tree"]]
        assert "R▪" in values and "S▪" in values

    def test_api_rejects_non_letters_and_too_many_words(self):
        r = client.post("/api/trace",
                        json={"algorithm": "trie_insert", "text": "CAT,C4R"})
        assert r.status_code == 400
        r = client.post("/api/trace", json={
            "algorithm": "trie_insert",
            "text": ",".join(["WORD"] * (trie_insert.MAX_WORDS + 1)),
        })
        assert r.status_code == 400


# ── N-Queens ──────────────────────────────────────────────────────────────

def _is_valid(solution, n):
    if len(solution) != n:
        return False
    cols = [c for _, c in solution]
    if len(set(cols)) != n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            if abs(cols[i] - cols[j]) == abs(solution[i][0] - solution[j][0]):
                return False
    return True


class TestNQueens:
    @pytest.mark.parametrize("n", [4, 5, 6])
    def test_finds_a_valid_solution(self, n):
        res = n_queens.trace(n)
        assert _is_valid(res["meta"]["solution"], n), res["meta"]["solution"]

    def test_four_queens_matches_the_known_answer(self):
        # For n=4 the first solution found column-by-column is [1,3,0,2].
        assert n_queens.trace(4)["meta"]["solution"] == [[0, 1], [1, 3], [2, 0], [3, 2]]

    def test_backtracking_actually_happens(self):
        # n=4 cannot be solved without retracting at least one queen.
        assert _final(n_queens.trace(4))["counts"]["backtracks"] > 0

    def test_board_shows_exactly_n_queens_at_the_end(self):
        n = 5
        grid = _final(n_queens.trace(n))["grid"]
        placed = sum(1 for row in grid for cell in row if cell == n_queens.QUEEN)
        assert placed == n

    def test_stops_at_the_first_solution(self):
        assert _final(n_queens.trace(5))["counts"]["solutions"] == 1

    def test_api_rejects_boards_that_are_too_small_or_large(self):
        for bad in (3, 7):
            r = client.post("/api/trace",
                            json={"algorithm": "n_queens", "target": bad})
            assert r.status_code == 400


# ── Unique paths ──────────────────────────────────────────────────────────

def _binomial_paths(n):
    from math import comb
    return comb(2 * (n - 1), n - 1)


class TestUniquePaths:
    @pytest.mark.parametrize("n", [2, 3, 4, 5])
    def test_open_grid_matches_the_binomial_formula(self, n):
        assert unique_paths.trace(n, n)["meta"]["result"] == _binomial_paths(n)

    def test_wall_reduces_the_count(self):
        assert unique_paths.trace(3, 3)["meta"]["result"] == 6
        assert unique_paths.trace(3, 3, [[1, 1]])["meta"]["result"] == 2

    def test_fully_blocked_row_means_no_route(self):
        res = unique_paths.trace(3, 3, [[1, 0], [1, 1], [1, 2]])
        assert res["meta"]["result"] == 0
        assert "no route" in res["steps"][-1]["note"].lower()

    def test_every_cell_is_computed_once(self):
        res = unique_paths.trace(4, 4)
        assert _final(res)["counts"]["cells"] == 16

    def test_first_row_and_column_are_all_ones(self):
        grid = _final(unique_paths.trace(4, 4))["grid"]
        assert all(grid[0][c] == 1 for c in range(4))
        assert all(grid[r][0] == 1 for r in range(4))

    def test_api_rejects_a_wall_on_the_start_square(self):
        r = client.post("/api/trace", json={
            "algorithm": "unique_paths", "target": 3, "text": "0:0",
        })
        assert r.status_code == 400
        assert "start square" in r.json()["detail"]

    def test_api_rejects_out_of_range_walls(self):
        r = client.post("/api/trace", json={
            "algorithm": "unique_paths", "target": 3, "text": "5:5",
        })
        assert r.status_code == 400


# ── Sieve ─────────────────────────────────────────────────────────────────

def _brute_primes(n):
    return [p for p in range(2, n + 1)
            if all(p % d for d in range(2, int(p ** 0.5) + 1))]


class TestSieve:
    @pytest.mark.parametrize("n", [10, 20, 30, 50])
    def test_matches_trial_division(self, n):
        assert sieve.trace(n)["meta"]["primes"] == _brute_primes(n)

    def test_zero_and_one_are_never_prime(self):
        primes = sieve.trace(30)["meta"]["primes"]
        assert 0 not in primes and 1 not in primes

    def test_crossings_happen_at_least_once(self):
        assert _final(sieve.trace(30))["counts"]["crossings"] > 0

    def test_primes_above_sqrt_n_need_no_crossing_pass(self):
        # 7 > √30, so it is reported as prime without scanning multiples.
        assert _final(sieve.trace(30))["counts"]["skipped_as_done"] > 0

    def test_array_marks_survivors_with_one(self):
        final = _final(sieve.trace(20))
        for p in (2, 3, 5, 7, 11, 13, 17, 19):
            assert final["array"][p] == 1
        for composite in (4, 6, 8, 9, 10):
            assert final["array"][composite] == 0

    def test_api_range_validation(self):
        for bad in (5, 100):
            r = client.post("/api/trace",
                            json={"algorithm": "sieve", "target": bad})
            assert r.status_code == 400


# ── API surface ───────────────────────────────────────────────────────────

class TestBatch7Endpoints:
    def test_all_five_are_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"tree_traversal", "trie_insert", "n_queens",
                "unique_paths", "sieve"} <= ids

    @pytest.mark.parametrize("algo,payload,check", [
        ("tree_traversal", {"array": [5, 3, 8]}, lambda d: d["meta"]["view"] == "tree"),
        ("trie_insert", {"text": "CAT,CAR"}, lambda d: d["meta"]["words"] == ["CAT", "CAR"]),
        ("n_queens", {"target": 4}, lambda d: len(d["meta"]["solution"]) == 4),
        ("unique_paths", {"target": 3}, lambda d: d["meta"]["result"] == 6),
        ("sieve", {"target": 20}, lambda d: d["meta"]["primes"][0] == 2),
    ])
    def test_each_runs_over_the_api(self, algo, payload, check):
        r = client.post("/api/trace", json={"algorithm": algo, **payload})
        assert r.status_code == 200, r.text
        assert check(r.json())

    @pytest.mark.parametrize("algo", ["n_queens", "unique_paths", "sieve"])
    def test_number_algorithms_require_a_target(self, algo):
        r = client.post("/api/trace", json={"algorithm": algo})
        assert r.status_code == 400
        assert "target" in r.json()["detail"]

    def test_every_step_of_every_new_tracer_carries_counts(self):
        for res in (tree_traversal.trace([5, 3, 8]), trie_insert.trace(["CAT"]),
                    n_queens.trace(4), unique_paths.trace(3, 3), sieve.trace(20)):
            assert all("counts" in s["structures"] for s in res["steps"])
