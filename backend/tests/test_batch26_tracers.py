"""Batch 26 — Recursion & Stack (Steps 7, 9): stock span and largest
rectangle in a histogram (monotonic stack), rat in a maze and word search
(grid backtracking). Each is checked against an independent brute force.
"""

import itertools
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import stock_span, largest_rectangle, rat_in_maze, word_search

client = TestClient(app)


def _ref_span(a):
    out = []
    for i in range(len(a)):
        k = i
        while k >= 0 and a[k] <= a[i]:
            k -= 1
        out.append(i - k)
    return out


def _ref_rect(h):
    return max((min(h[i:j + 1]) * (j - i + 1)
                for i in range(len(h)) for j in range(i, len(h))), default=0)


def _ref_maze(n, walls):
    """Every simple path by plain DFS, sorted — no shared code with the tracer."""
    out = []
    moves = {"D": (1, 0), "L": (0, -1), "R": (0, 1), "U": (-1, 0)}

    def go(r, c, seen, s):
        if (r, c) == (n - 1, n - 1):
            out.append(s)
            return
        for d, (dr, dc) in moves.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in walls | seen:
                go(nr, nc, seen | {(nr, nc)}, s + d)

    if (0, 0) not in walls and (n - 1, n - 1) not in walls:
        go(0, 0, {(0, 0)}, "")
    return sorted(out)


def _ref_word(board, word):
    rows, cols = len(board), len(board[0])

    def go(r, c, k, seen):
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        return any(go(nr, nc, k + 1, seen | {(nr, nc)})
                   for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                   if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen)

    return any(go(r, c, 0, {(r, c)}) for r in range(rows) for c in range(cols))


class TestStackTracers:
    def test_stock_span(self):
        cases = [[100, 80, 60, 70, 60, 75, 85], [1, 2, 3], [3, 2, 1],
                 [5, 5, 5], [7]]
        rng = random.Random(26)
        cases += [[rng.randint(0, 9) for _ in range(rng.randint(1, 16))]
                  for _ in range(50)]
        for c in cases:
            assert stock_span.trace(c)["meta"]["result"] == _ref_span(c), c

    def test_largest_rectangle(self):
        cases = [[2, 1, 5, 6, 2, 3], [2, 4], [1], [0, 0], [6, 2, 5, 4, 5, 1, 6],
                 [3, 3, 3]]
        rng = random.Random(39)
        cases += [[rng.randint(0, 9) for _ in range(rng.randint(1, 16))]
                  for _ in range(50)]
        for c in cases:
            meta = largest_rectangle.trace(c)["meta"]
            assert meta["result"] == _ref_rect(c), c
            if meta["range"]:
                lo, hi = meta["range"]
                assert min(c[lo:hi + 1]) * (hi - lo + 1) == meta["result"]


class TestBacktrackingTracers:
    def test_rat_striver_example(self):
        walls = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 2), (2, 3), (3, 0)]
        meta = rat_in_maze.trace(4, walls)["meta"]
        assert meta["result"] == ["DDRDRR", "DRDDRR"]

    def test_rat_matches_reference(self):
        rng = random.Random(7)
        for _ in range(40):
            n = rng.randint(2, 4)
            cells = [(r, c) for r in range(n) for c in range(n)
                     if (r, c) not in ((0, 0), (n - 1, n - 1))]
            walls = set(rng.sample(cells, rng.randint(0, len(cells))))
            meta = rat_in_maze.trace(n, list(walls))["meta"]
            want = _ref_maze(n, walls)
            assert meta["path_count"] == len(want), (n, walls)
            assert meta["result"] == want[:rat_in_maze.MAX_PATHS_LISTED]

    def test_rat_open_5x5_caps_steps_not_answer(self):
        out = rat_in_maze.trace(5, [])
        assert out["meta"]["path_count"] == 8512  # self-avoiding corner walks
        assert len(out["steps"]) <= rat_in_maze.MAX_STEPS + 1

    def test_rat_blocked_exit(self):
        assert rat_in_maze.trace(3, [(2, 2)])["meta"]["path_count"] == 0

    def test_word_search_classic(self):
        board = ["ABCE", "SFCS", "ADEE"]
        for word, want in (("ABCCED", True), ("SEE", True), ("ABCB", False)):
            meta = word_search.trace(board, word)["meta"]
            assert meta["result"] is want, word
            if want:
                assert "".join(board[r][c] for r, c in meta["path"]) == word

    def test_word_search_matches_reference(self):
        rng = random.Random(18)
        for _ in range(120):
            rows, cols = rng.randint(1, 4), rng.randint(1, 4)
            board = ["".join(rng.choice("AB") for _ in range(cols))
                     for _ in range(rows)]
            word = "".join(rng.choice("AB") for _ in range(rng.randint(1, 5)))
            got = word_search.trace(board, word)["meta"]["result"]
            assert got is _ref_word(board, word), (board, word)

    def test_word_search_path_is_adjacent_and_distinct(self):
        for board, word in (
            (["ABCE", "SFCS", "ADEE"], "ABCCED"),
            (["AAAA", "AAAA", "AAAB"], "AAAAAAAB"),
        ):
            p = word_search.trace(board, word)["meta"]["path"]
            assert len(set(map(tuple, p))) == len(p) == len(word)
            for (a, b), (c, d) in itertools.pairwise(p):
                assert abs(a - c) + abs(b - d) == 1


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"stock_span", "largest_rectangle", "rat_in_maze",
                "word_search"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("stock_span", {"array": [100, 80, 60, 70, 60, 75, 85]}),
            ("largest_rectangle", {"array": [2, 1, 5, 6, 2, 3]}),
            ("rat_in_maze", {"target": 4, "text": "0:1,0:2,0:3,1:2,2:2,2:3,3:0"}),
            ("rat_in_maze", {"target": 3}),
            ("word_search", {"text": "ABCE/SFCS/ADEE, abcced"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        bad = [
            {"algorithm": "stock_span", "array": []},
            {"algorithm": "stock_span", "array": [1, -2]},
            {"algorithm": "largest_rectangle", "array": list(range(20))},
            {"algorithm": "rat_in_maze"},                          # no side
            {"algorithm": "rat_in_maze", "target": 6},             # too big
            {"algorithm": "rat_in_maze", "target": 3, "text": "2:2"},  # exit walled
            {"algorithm": "rat_in_maze", "target": 3, "text": "5:5"},
            {"algorithm": "word_search", "text": "ABC/DE,AB"},     # ragged
            {"algorithm": "word_search", "text": "ABCDEF,AB"},     # too wide
            {"algorithm": "word_search", "text": "AB/CD,ABCDABCDA"},  # word too long
            {"algorithm": "word_search", "text": "AB/CD"},         # no word
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for algo in ("stock_span", "largest_rectangle", "rat_in_maze",
                     "word_search"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
