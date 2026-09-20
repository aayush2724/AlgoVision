"""Batch 24 — DP remainder (Step 16): frog jump (1-D DP), best time to buy and
sell stock, coin change 2 (count ways), and longest common substring. Each is
checked against an independent reference implementation.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    frog_jump, buy_sell_stock, coin_change_2, longest_common_substring,
)

client = TestClient(app)


def _ref_frog(h):
    n = len(h)
    if n == 0:
        return 0
    dp = [0] * n
    for i in range(1, n):
        one = dp[i - 1] + abs(h[i] - h[i - 1])
        two = dp[i - 2] + abs(h[i] - h[i - 2]) if i >= 2 else float("inf")
        dp[i] = min(one, two)
    return dp[-1]


def _ref_stock(p):
    best, low = 0, float("inf")
    for x in p:
        low = min(low, x)
        best = max(best, x - low)
    return best


def _ref_cc2(coins, amt):
    dp = [0] * (amt + 1)
    dp[0] = 1
    for c in coins:
        for a in range(c, amt + 1):
            dp[a] += dp[a - c]
    return dp[amt]


def _ref_lcsubstr(a, b):
    n, m = len(a), len(b)
    g = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                g[i][j] = g[i - 1][j - 1] + 1
                best = max(best, g[i][j])
    return best


class TestDPTracers:
    def test_frog_jump(self):
        for h in ([10, 30, 40, 20], [30, 10, 60, 10, 60, 50], [10], [10, 10, 10],
                  [7, 4, 4, 2, 6, 6, 3, 4]):
            assert frog_jump.trace(h)["meta"]["result"] == _ref_frog(h), h

    def test_frog_route_valid(self):
        # the reconstructed route must start at 0, end at n-1, hop by 1 or 2
        h = [30, 10, 60, 10, 60, 50]
        route = frog_jump.trace(h)["meta"]["route"]
        assert route[0] == 0 and route[-1] == len(h) - 1
        assert all(0 < route[k] - route[k - 1] <= 2 for k in range(1, len(route)))

    def test_buy_sell(self):
        for p in ([7, 1, 5, 3, 6, 4], [7, 6, 4, 3, 1], [1, 2, 3, 4, 5], [5], [2, 4, 1]):
            assert buy_sell_stock.trace(p)["meta"]["result"] == _ref_stock(p), p

    def test_coin_change_2(self):
        cases = [([1, 2, 3], 4), ([2], 3), ([1], 0), ([1, 2, 5], 5), ([3, 5, 7], 12)]
        for coins, amt in cases:
            assert coin_change_2.trace(coins, amt)["meta"]["result"] == _ref_cc2(coins, amt), (coins, amt)

    def test_longest_common_substring(self):
        cases = [("ABCDE", "ZBCDF"), ("ABCDGH", "ACDGHR"), ("ABC", "XYZ"),
                 ("AAAA", "AA"), ("GEEKS", "GEEKSFORGEEKS")]
        for a, b in cases:
            out = longest_common_substring.trace(a, b)["meta"]
            assert out["length"] == _ref_lcsubstr(a, b), (a, b)
            # the recovered substring must actually appear in both strings
            if out["result"]:
                assert out["result"] in a and out["result"] in b, (a, b, out["result"])


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"frog_jump", "buy_sell_stock", "coin_change_2",
                "longest_common_substring"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("frog_jump", {"array": [30, 10, 60, 10, 60, 50]}),
            ("buy_sell_stock", {"array": [7, 1, 5, 3, 6, 4]}),
            ("coin_change_2", {"array": [1, 2, 3], "target": 4}),
            ("longest_common_substring", {"text": "ABCDE,ZBCDF"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        assert client.post("/api/trace", json={"algorithm": "frog_jump", "array": []}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "frog_jump", "array": [1, -2]}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "buy_sell_stock", "array": [1, 2.5]}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "coin_change_2", "array": [1, 2]}).status_code == 400  # no target
        assert client.post("/api/trace", json={"algorithm": "coin_change_2", "array": [1], "target": 99}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "longest_common_substring", "text": "ABC"}).status_code == 400

    def test_detect_resolves(self):
        for algo in ("frog_jump", "buy_sell_stock", "coin_change_2",
                     "longest_common_substring"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
