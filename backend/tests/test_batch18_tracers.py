"""Batch 18 (greedy) — Activity Selection / N-meetings-in-one-room.

Checked against a brute-force optimum: the greedy (earliest-finish-first) count
must equal the largest set of pairwise non-overlapping meetings.
"""

from itertools import combinations

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import activity_selection

client = TestClient(app)


def _brute_max(intervals):
    """Largest subset with no two meetings overlapping (half-open: a meeting
    ending at t and one starting at t do not clash)."""
    n = len(intervals)
    for r in range(n, 0, -1):
        for combo in combinations(intervals, r):
            s = sorted(combo, key=lambda iv: iv[1])
            if all(s[i][0] >= s[i - 1][1] for i in range(1, len(s))):
                return r
    return 0


class TestActivitySelection:
    def test_classic_case(self):
        r = activity_selection.trace([[1, 2], [3, 4], [0, 6], [5, 7], [8, 9], [5, 9]])
        assert r["meta"]["count"] == 4
        assert r["meta"]["chosen"] == [[1, 2], [3, 4], [5, 7], [8, 9]]

    def test_matches_brute_force(self):
        cases = [
            [[1, 3], [2, 4], [3, 5], [0, 6], [5, 7], [8, 9]],
            [[0, 5], [1, 2], [2, 3], [3, 4]],
            [[1, 2], [2, 3], [3, 4], [4, 5]],
            [[1, 10], [2, 3], [4, 5]],
        ]
        for c in cases:
            assert activity_selection.trace(c)["meta"]["count"] == _brute_max(c), c

    def test_chosen_are_non_overlapping(self):
        chosen = activity_selection.trace(
            [[1, 3], [2, 4], [3, 5], [0, 6], [5, 7]])["meta"]["chosen"]
        chosen.sort(key=lambda iv: iv[1])
        assert all(chosen[i][0] >= chosen[i - 1][1] for i in range(1, len(chosen)))

    def test_single_meeting(self):
        r = activity_selection.trace([[2, 5]])
        assert r["meta"]["count"] == 1

    def test_all_overlap_picks_one(self):
        r = activity_selection.trace([[1, 9], [2, 8], [3, 7]])
        assert r["meta"]["count"] == 1

    def test_steps_carry_array_and_counts(self):
        s = activity_selection.trace([[1, 2], [3, 4]])["steps"][-1]["structures"]
        assert "array" in s and "sorted_ranges" in s and "counts" in s


class TestEndpoints:
    def test_is_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert "activity_selection" in ids

    def test_endpoint_returns_a_trace(self):
        res = client.post("/api/trace", json={
            "algorithm": "activity_selection", "text": "1-2, 3-4, 0-6, 5-7"})
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"]
        assert body["meta"]["algorithm"] == "activity_selection"
        assert body["meta"]["count"] == 3

    def test_rejects_missing_text(self):
        res = client.post("/api/trace", json={"algorithm": "activity_selection"})
        assert res.status_code == 400

    def test_rejects_bad_pair(self):
        res = client.post("/api/trace", json={
            "algorithm": "activity_selection", "text": "5-2"})
        assert res.status_code == 400

    def test_detect_resolves_id(self):
        body = client.post("/api/detect",
                           json={"code": "", "problem": "activity_selection"}).json()
        assert body["algorithm"] == "activity_selection"
        assert body["realworld"]["scene"]
        assert body["realworld"]["title"]
