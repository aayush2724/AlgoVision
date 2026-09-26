"""Batch 28 — Linked List (Step 6) + Tries (Step 17): reverse a doubly linked
list, delete all occurrences of a key in a DLL, remove the Nth node from the
end, and the longest word with all prefixes. Each is checked against plain
Python list/set logic, plus pointer-consistency checks on the DLL steps.
"""

import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    dll_reverse, dll_delete_key, remove_nth_from_end, longest_complete_word,
)

client = TestClient(app)


def _ref_complete(words):
    s = set(words)
    good = [w for w in s if all(w[:i] in s for i in range(1, len(w) + 1))]
    return min(good, key=lambda w: (-len(w), w)) if good else None


def _dll_consistent(st):
    """Every live node's next/prev must mirror each other."""
    nxt, prv = st["next"], st["prev_links"]
    removed = set(st.get("removed", []))
    for i, j in enumerate(nxt):
        if i in removed or j is None:
            continue
        assert prv[j] == i, (i, j, nxt, prv)


class TestLinkedLists:
    def test_dll_reverse(self):
        rng = random.Random(9)
        cases = [[10, 20, 30, 40], [7], [1, 2]] + [
            [rng.randint(0, 9) for _ in range(rng.randint(1, 10))] for _ in range(30)]
        for c in cases:
            out = dll_reverse.trace(c)
            assert out["meta"]["result"] == c[::-1], c
            for step in out["steps"]:
                _dll_consistent(step["structures"])

    def test_dll_delete_key(self):
        rng = random.Random(52)
        cases = [([2, 5, 2, 7, 2], 2), ([1, 1, 1], 1), ([3, 4], 9), ([4], 4)]
        cases += [([rng.randint(0, 3) for _ in range(rng.randint(1, 10))],
                   rng.randint(0, 3)) for _ in range(40)]
        for arr, key in cases:
            out = dll_delete_key.trace(arr, key)
            assert out["meta"]["result"] == [v for v in arr if v != key], (arr, key)
            for step in out["steps"]:
                _dll_consistent(step["structures"])

    def test_remove_nth_from_end(self):
        for size in range(1, 11):
            arr = list(range(1, size + 1))
            for n in range(1, size + 1):
                out = remove_nth_from_end.trace(arr, n)
                want = arr[:size - n] + arr[size - n + 1:]
                assert out["meta"]["result"] == want, (arr, n)
                assert out["meta"]["removed"] == size - n


class TestTrie:
    def test_classic(self):
        words = ["N", "NI", "NIN", "NINJ", "NINJA", "NINGA"]
        assert longest_complete_word.trace(words)["meta"]["result"] == "NINJA"

    def test_none_and_ties(self):
        assert longest_complete_word.trace(["AB", "BC"])["meta"]["result"] is None
        assert longest_complete_word.trace(["B", "A", "AB", "BA"])["meta"]["result"] == "AB"

    def test_matches_reference(self):
        rng = random.Random(3)
        for _ in range(150):
            words = ["".join(rng.choice("AB") for _ in range(rng.randint(1, 4)))
                     for _ in range(rng.randint(1, 7))]
            got = longest_complete_word.trace(words)["meta"]["result"]
            assert got == _ref_complete(words), words


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"dll_reverse", "dll_delete_key", "remove_nth_from_end",
                "longest_complete_word"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("dll_reverse", {"array": [10, 20, 30]}),
            ("dll_delete_key", {"array": [2, 5, 2], "target": 2}),
            ("remove_nth_from_end", {"array": [1, 2, 3, 4, 5], "target": 2}),
            ("longest_complete_word", {"text": "n, ni, nin, ninja"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        bad = [
            {"algorithm": "dll_reverse", "array": []},
            {"algorithm": "dll_reverse", "array": list(range(11))},
            {"algorithm": "dll_delete_key", "array": [1, 2]},            # no key
            {"algorithm": "remove_nth_from_end", "array": [1, 2], "target": 3},
            {"algorithm": "remove_nth_from_end", "array": [1, 2], "target": 0},
            {"algorithm": "longest_complete_word", "text": "A1,B"},
            {"algorithm": "longest_complete_word", "text": "A,B,C,D,E,F,G,H"},
        ]
        for p in bad:
            assert client.post("/api/trace", json=p).status_code == 400, p

    def test_detect_resolves(self):
        for algo in ("dll_reverse", "dll_delete_key", "remove_nth_from_end",
                     "longest_complete_word"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
