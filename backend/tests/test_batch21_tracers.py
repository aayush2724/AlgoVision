"""Batch 21 — Heaps (min-heap, kth largest/smallest) and variable-size sliding
windows (longest-substring-no-repeat, max-consecutive-ones-III, longest-K-
distinct). Checked against reference implementations / sorted brute force.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    min_heap, kth_largest, kth_smallest, longest_substring_no_repeat,
    max_consecutive_ones_iii, longest_k_distinct,
)

client = TestClient(app)


def _is_min_heap(a):
    n = len(a)
    for i in range(n):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n and a[i] > a[c]:
                return False
    return True


class TestHeaps:
    def test_min_heap_property(self):
        heap = [nd["value"] for nd in
                min_heap.trace([5, 3, 8, 1, 12, 2])["steps"][-1]["structures"]["tree"]]
        assert heap[0] == 1
        assert _is_min_heap(heap)

    def test_kth_largest(self):
        for arr, k in (([3, 2, 1, 5, 6, 4], 2), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), ([1], 1)):
            assert kth_largest.trace(arr, k)["meta"]["kth"] == sorted(arr, reverse=True)[k - 1]

    def test_kth_smallest(self):
        for arr, k in (([7, 10, 4, 3, 20, 15], 3), ([1, 2, 3, 4, 5], 1), ([2, 1], 2)):
            assert kth_smallest.trace(arr, k)["meta"]["kth"] == sorted(arr)[k - 1]


def _lsnr_ref(s):
    best, seen, left = 0, {}, 0
    for r, c in enumerate(s):
        if c in seen and seen[c] >= left:
            left = seen[c] + 1
        seen[c] = r
        best = max(best, r - left + 1)
    return best


def _maxones_ref(a, k):
    best = left = zeros = 0
    for r, v in enumerate(a):
        zeros += v == 0
        while zeros > k:
            zeros -= a[left] == 0
            left += 1
        best = max(best, r - left + 1)
    return best


def _kdistinct_ref(s, k):
    from collections import Counter
    best = left = 0
    f = Counter()
    for r, c in enumerate(s):
        f[c] += 1
        while len(f) > k:
            f[s[left]] -= 1
            if not f[s[left]]:
                del f[s[left]]
            left += 1
        best = max(best, r - left + 1)
    return best


class TestSlidingWindows:
    def test_longest_no_repeat(self):
        for s in ("ABCABCBB", "BBBBB", "PWWKEW", "ABCDE", "AABAAB"):
            assert longest_substring_no_repeat.trace(s)["meta"]["length"] == _lsnr_ref(s), s

    def test_max_consecutive_ones(self):
        cases = [([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), ([0, 0, 1, 1, 0, 0, 1, 1, 1, 0], 3),
                 ([1, 1, 1, 1], 0), ([0, 0, 0], 0)]
        for a, k in cases:
            assert max_consecutive_ones_iii.trace(a, k)["meta"]["length"] == _maxones_ref(a, k), (a, k)

    def test_longest_k_distinct(self):
        for s, k in (("ECEBA", 2), ("AABBCC", 2), ("AAAA", 1), ("ABACCC", 2)):
            assert longest_k_distinct.trace(s, k)["meta"]["length"] == _kdistinct_ref(s, k), (s, k)


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"min_heap", "kth_largest", "kth_smallest",
                "longest_substring_no_repeat", "max_consecutive_ones_iii",
                "longest_k_distinct"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("min_heap", {"array": [5, 3, 8, 1]}),
            ("kth_largest", {"text": "3,2,1,5,6,4 | 2"}),
            ("kth_smallest", {"text": "7,10,4,3,20,15 | 3"}),
            ("longest_substring_no_repeat", {"text": "ABCABCBB"}),
            ("max_consecutive_ones_iii", {"text": "1,1,0,0,1 | 2"}),
            ("longest_k_distinct", {"text": "ECEBA | 2"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        assert client.post("/api/trace", json={"algorithm": "kth_largest", "text": "1,2,3"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "kth_largest", "text": "1,2,3 | 9"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "max_consecutive_ones_iii", "text": "1,2,0 | 1"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "longest_k_distinct", "text": "ECEBA"}).status_code == 400

    def test_detect_resolves(self):
        for algo in ("min_heap", "kth_largest", "kth_smallest",
                     "longest_substring_no_repeat", "max_consecutive_ones_iii",
                     "longest_k_distinct"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
