"""Batch 12 — string algorithms on the array view: the Z-function, Rabin–Karp
rolling-hash search, and Manacher's longest palindrome.

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import manacher, rabin_karp, z_function

client = TestClient(app)

ENVELOPE = {"i", "line", "structures", "highlight", "note"}


def _assert_envelope(res):
    assert res["steps"], "a tracer must emit at least one step"
    for s in res["steps"]:
        assert ENVELOPE <= set(s), f"step {s.get('i')} is missing envelope keys"
        assert "counts" in s["structures"], "counters missing from structures"
        assert s["note"], "every step needs a note to narrate"
    for key in res["steps"][0]["structures"]["counts"]:
        seq = [s["structures"]["counts"][key] for s in res["steps"]]
        assert seq == sorted(seq), f"counter {key!r} went backwards: {seq}"


# ── Z-FUNCTION ────────────────────────────────────────────────────────────

def _brute_z(s):
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    for i in range(1, n):
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
    return z


class TestZFunction:
    def test_known_value(self):
        # "aabxaab": position 5 ("aab") matches the prefix for 2 chars.
        assert z_function.trace("AABXAAB")["meta"]["z"] == _brute_z("AABXAAB")

    def test_all_same_char(self):
        res = z_function.trace("AAAA")
        assert res["meta"]["z"] == [4, 3, 2, 1]
        assert res["meta"]["result"] == 3

    def test_no_internal_match(self):
        assert z_function.trace("ABCDE")["meta"]["result"] == 0

    def test_single_char(self):
        res = z_function.trace("A")
        assert res["meta"]["z"] == [1]
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        s = "".join(rng.choice("AB") for _ in range(rng.randint(1, 18)))
        res = z_function.trace(s)
        assert res["meta"]["z"] == _brute_z(s)
        _assert_envelope(res)


# ── RABIN–KARP ────────────────────────────────────────────────────────────

def _brute_find(text, pattern):
    m = len(pattern)
    return [i for i in range(len(text) - m + 1) if text[i:i + m] == pattern]


class TestRabinKarp:
    def test_single_match(self):
        assert rabin_karp.trace("ABRACADABRA", "CAD")["meta"]["matches"] == [4]

    def test_overlapping_matches(self):
        assert rabin_karp.trace("AAAA", "AA")["meta"]["matches"] == [0, 1, 2]

    def test_no_match(self):
        assert rabin_karp.trace("ABCDEF", "XYZ")["meta"]["matches"] == []

    def test_whole_string(self):
        assert rabin_karp.trace("HELLO", "HELLO")["meta"]["matches"] == [0]

    def test_collisions_still_verify_characters(self):
        # A real match must pass the character check, not the hash alone.
        res = rabin_karp.trace("ABAB", "AB")
        assert res["meta"]["matches"] == [0, 2]
        _assert_envelope(res)

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        text = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 20)))
        m = rng.randint(1, len(text))
        pattern = "".join(rng.choice("ABC") for _ in range(m))
        res = rabin_karp.trace(text, pattern)
        assert res["meta"]["matches"] == _brute_find(text, pattern)
        _assert_envelope(res)


# ── MANACHER ──────────────────────────────────────────────────────────────

def _brute_longest_palindrome_len(s):
    best = 0
    n = len(s)
    for i in range(n):
        for j in range(i, n):
            sub = s[i:j + 1]
            if sub == sub[::-1]:
                best = max(best, len(sub))
    return best


class TestManacher:
    def test_odd_palindrome(self):
        res = manacher.trace("BABAD")
        assert res["meta"]["result"] == 3  # "BAB" or "ABA"
        assert res["meta"]["longest"] in ("BAB", "ABA")

    def test_even_palindrome(self):
        res = manacher.trace("CBBD")
        assert res["meta"]["result"] == 2
        assert res["meta"]["longest"] == "BB"

    def test_whole_string_palindrome(self):
        assert manacher.trace("RACECAR")["meta"]["result"] == 7

    def test_no_palindrome_beyond_one(self):
        assert manacher.trace("ABCD")["meta"]["result"] == 1

    def test_single_char(self):
        res = manacher.trace("A")
        assert res["meta"]["result"] == 1
        _assert_envelope(res)

    def test_reported_longest_is_a_palindrome_and_substring(self):
        res = manacher.trace("FORGEEKSSKEEGFOR")
        longest = res["meta"]["longest"]
        assert longest == longest[::-1], "reported string must be a palindrome"
        assert longest in "FORGEEKSSKEEGFOR", "must be a real substring"

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_brute_force(self, seed):
        rng = random.Random(seed)
        s = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 16)))
        res = manacher.trace(s)
        assert res["meta"]["result"] == _brute_longest_palindrome_len(s)
        longest = res["meta"]["longest"]
        assert longest == longest[::-1]
        assert longest in s
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_three_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"z_function", "rabin_karp", "manacher"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "z_function", "text": "AABXAAB"},
        {"algorithm": "rabin_karp", "text": "ABRACADABRA,ABRA"},
        {"algorithm": "manacher", "text": "BABAD"},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "z_function"}, "requires 'text'"),
        ({"algorithm": "z_function", "text": "A B!"}, "letters or digits"),
        ({"algorithm": "manacher"}, "requires 'text'"),
        ({"algorithm": "rabin_karp", "text": "ABC"}, "comma-separated"),
        ({"algorithm": "rabin_karp", "text": "AB,ABCD"}, "longer than the text"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id", ["z_function", "rabin_karp", "manacher"])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
