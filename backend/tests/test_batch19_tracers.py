"""Batch 19 (greedy) — Fractional Knapsack and Job Sequencing.

Fractional knapsack is checked against the closed-form greedy optimum (sort by
ratio, split the last item). Job sequencing is checked against a brute-force
optimum over all subsets that can be validly scheduled.
"""

from itertools import permutations

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import fractional_knapsack, job_sequencing

client = TestClient(app)


# ── Fractional Knapsack ──────────────────────────────────────────────────────

def _fk_optimum(items, cap):
    total, rem = 0.0, float(cap)
    for w, v in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        if rem <= 0:
            break
        take = min(w, rem)
        total += v * (take / w)
        rem -= take
    return round(total, 2)


class TestFractionalKnapsack:
    def test_classic_case(self):
        r = fractional_knapsack.trace([[10, 60], [20, 100], [30, 120]], 50)
        assert r["meta"]["total_value"] == 240

    def test_matches_greedy_optimum(self):
        cases = [
            ([[10, 60], [20, 100], [30, 120]], 50),
            ([[5, 30], [10, 20], [15, 15]], 12),
            ([[1, 1], [3, 9], [2, 4]], 4),
        ]
        for items, cap in cases:
            assert fractional_knapsack.trace(items, cap)["meta"]["total_value"] \
                == _fk_optimum(items, cap), (items, cap)

    def test_capacity_exceeds_all_takes_everything(self):
        items = [[2, 10], [3, 12]]
        r = fractional_knapsack.trace(items, 100)
        assert r["meta"]["total_value"] == 22

    def test_steps_have_array_and_counts(self):
        s = fractional_knapsack.trace([[2, 10], [3, 12]], 4)["steps"][-1]["structures"]
        assert "array" in s and "counts" in s


# ── Job Sequencing ───────────────────────────────────────────────────────────

def _js_optimum(jobs):
    """Brute force: best total profit over every ordering placed greedily into
    latest free slots — equivalently, the max-profit schedulable subset."""
    max_d = max((d for d, _ in jobs), default=0)
    best = 0
    n = len(jobs)
    for perm in permutations(range(n)):
        slots = [False] * max_d
        profit = 0
        for i in perm:
            d, p = jobs[i]
            for t in range(min(d, max_d), 0, -1):
                if not slots[t - 1]:
                    slots[t - 1] = True
                    profit += p
                    break
        best = max(best, profit)
    return best


class TestJobSequencing:
    def test_classic_case(self):
        r = job_sequencing.trace([[2, 100], [1, 19], [2, 27], [1, 25], [3, 15]])
        assert r["meta"]["total_profit"] == 142
        assert r["meta"]["count"] == 3

    def test_matches_brute_force(self):
        cases = [
            [[2, 100], [1, 19], [2, 27], [1, 25], [3, 15]],
            [[4, 20], [1, 10], [1, 40], [1, 30]],
            [[2, 50], [2, 60], [2, 20]],
            [[1, 5], [1, 6], [1, 7]],
        ]
        for jobs in cases:
            assert job_sequencing.trace(jobs)["meta"]["total_profit"] \
                == _js_optimum(jobs), jobs

    def test_slot_timeline_only_holds_scheduled(self):
        r = job_sequencing.trace([[2, 100], [2, 27], [1, 25]])
        slots = r["steps"][-1]["structures"]["array"]
        filled = [c for c in slots if c != "·"]
        assert len(filled) == r["meta"]["count"]


# ── Endpoints ────────────────────────────────────────────────────────────────

class TestEndpoints:
    def test_both_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"fractional_knapsack", "job_sequencing"} <= ids

    def test_fk_endpoint(self):
        res = client.post("/api/trace", json={
            "algorithm": "fractional_knapsack", "text": "10:60, 20:100, 30:120 | 50"})
        assert res.status_code == 200, res.text
        assert res.json()["meta"]["total_value"] == 240

    def test_js_endpoint(self):
        res = client.post("/api/trace", json={
            "algorithm": "job_sequencing", "text": "2:100, 1:19, 2:27, 1:25, 3:15"})
        assert res.status_code == 200, res.text
        assert res.json()["meta"]["total_profit"] == 142

    def test_fk_requires_capacity(self):
        assert client.post("/api/trace", json={
            "algorithm": "fractional_knapsack", "text": "10:60, 20:100"}).status_code == 400

    def test_js_rejects_bad_pair(self):
        assert client.post("/api/trace", json={
            "algorithm": "job_sequencing", "text": "2-100"}).status_code == 400

    def test_detect_resolves_ids(self):
        for algo in ("fractional_knapsack", "job_sequencing"):
            body = client.post("/api/detect",
                               json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
