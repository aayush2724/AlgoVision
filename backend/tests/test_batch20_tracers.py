"""Batch 20 (greedy) — Jump Game I/II, Candy, Lemonade Change, Assign Cookies,
Minimum Platforms. Each tracer's result is checked against an independent
reference (brute force or a second implementation).
"""

from collections import deque

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    jump_game, jump_game_ii, candy, lemonade_change, assign_cookies,
    min_platforms,
)

client = TestClient(app)


# ── references ───────────────────────────────────────────────────────────────

def _reach_ref(nums):
    n = len(nums)
    if n <= 1:
        return True
    dp = [False] * n
    dp[0] = True
    for i in range(n):
        if dp[i]:
            for k in range(1, nums[i] + 1):
                if i + k < n:
                    dp[i + k] = True
    return dp[-1]


def _minjumps_ref(nums):
    n = len(nums)
    if n <= 1:
        return 0
    seen = {0}
    q = deque([(0, 0)])
    while q:
        i, d = q.popleft()
        for k in range(1, nums[i] + 1):
            j = i + k
            if j >= n - 1:
                return d + 1
            if j not in seen:
                seen.add(j)
                q.append((j, d + 1))
    return -1


def _candy_ref(r):
    n = len(r)
    c = [1] * n
    for i in range(1, n):
        if r[i] > r[i - 1]:
            c[i] = c[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if r[i] > r[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)
    return sum(c)


def _lemonade_ref(bills):
    five = ten = 0
    for b in bills:
        if b == 5:
            five += 1
        elif b == 10:
            if not five:
                return False
            five -= 1
            ten += 1
        else:
            if ten and five:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True


def _cookies_ref(g, s):
    g, s = sorted(g), sorted(s)
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            i += 1
        j += 1
    return i


def _platforms_ref(a, d):
    a, d = sorted(a), sorted(d)
    i = j = plat = peak = 0
    while i < len(a):
        if a[i] <= d[j]:
            plat += 1
            peak = max(peak, plat)
            i += 1
        else:
            plat -= 1
            j += 1
    return peak


# ── tracer correctness ───────────────────────────────────────────────────────

class TestGreedyTracers:
    def test_jump_game(self):
        for nums in ([2, 3, 1, 1, 4], [3, 2, 1, 0, 4], [0], [2, 0, 0], [1, 1, 1]):
            assert jump_game.trace(nums)["meta"]["reachable"] == _reach_ref(nums), nums

    def test_jump_game_ii(self):
        for nums in ([2, 3, 1, 1, 4], [1, 1, 1, 1], [2, 1], [5, 1, 1, 1, 1], [1]):
            if _reach_ref(nums):
                assert jump_game_ii.trace(nums)["meta"]["jumps"] == _minjumps_ref(nums), nums

    def test_candy(self):
        for r in ([1, 0, 2], [1, 2, 2], [1, 3, 2, 2, 1], [1, 2, 3, 4], [5]):
            assert candy.trace(r)["meta"]["total"] == _candy_ref(r), r

    def test_lemonade(self):
        for bills in ([5, 5, 5, 10, 20], [5, 5, 10, 10, 20], [5, 10], [5, 5, 10, 20]):
            assert lemonade_change.trace(bills)["meta"]["served_all"] == _lemonade_ref(bills), bills

    def test_assign_cookies(self):
        for g, s in (([1, 2, 3], [1, 1]), ([1, 2], [1, 2, 3]), ([10, 9, 8, 7], [5, 6, 7, 8])):
            assert assign_cookies.trace(g, s)["meta"]["content"] == _cookies_ref(g, s), (g, s)

    def test_min_platforms(self):
        cases = [([900, 940, 950, 1100, 1500, 1800], [910, 1200, 1120, 1130, 1900, 2000]),
                 ([100, 200, 300], [150, 250, 350]), ([1, 2, 3], [10, 11, 12])]
        for a, d in cases:
            assert min_platforms.trace(a, d)["meta"]["platforms"] == _platforms_ref(a, d), (a, d)


# ── endpoints ────────────────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"jump_game", "jump_game_ii", "candy", "lemonade_change",
                "assign_cookies", "min_platforms"} <= ids

    def test_array_endpoints(self):
        for algo, arr in (("jump_game", [2, 3, 1, 1, 4]), ("jump_game_ii", [2, 3, 1, 1, 4]),
                          ("candy", [1, 0, 2]), ("lemonade_change", [5, 5, 5, 10, 20])):
            r = client.post("/api/trace", json={"algorithm": algo, "array": arr})
            assert r.status_code == 200, r.text
            assert r.json()["steps"]

    def test_text_endpoints(self):
        r1 = client.post("/api/trace", json={"algorithm": "assign_cookies", "text": "1,2,3 | 1,1"})
        assert r1.status_code == 200 and r1.json()["meta"]["content"] == 1
        r2 = client.post("/api/trace", json={"algorithm": "min_platforms",
                         "text": "900,940,950,1100,1500,1800 | 910,1200,1120,1130,1900,2000"})
        assert r2.status_code == 200 and r2.json()["meta"]["platforms"] == 3

    def test_validation(self):
        assert client.post("/api/trace", json={"algorithm": "lemonade_change", "array": [7]}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "jump_game", "array": [-1]}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "min_platforms", "text": "1,2 | 1"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "assign_cookies", "text": "1,2,3"}).status_code == 400

    def test_detect_resolves_ids(self):
        for algo in ("jump_game", "jump_game_ii", "candy", "lemonade_change",
                     "assign_cookies", "min_platforms"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
