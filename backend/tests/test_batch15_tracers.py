"""Batch 15 — anagram check and the number-theory trio (GCD/Euclid, fast
exponentiation, prime factorisation), all on the grid view.

Each tracer is checked against an independent brute-force implementation
rather than against itself, so a shared misunderstanding cannot pass.
"""

import math
import random

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    anagram, fast_exponentiation, gcd_euclid, prime_factorisation,
)

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


def _assert_rectangular(res):
    for s in res["steps"]:
        grid = s["structures"]["grid"]
        assert len({len(row) for row in grid}) <= 1, "ragged grid"


# ── ANAGRAM ───────────────────────────────────────────────────────────────

class TestAnagram:
    def test_true(self):
        assert anagram.trace("LISTEN", "SILENT")["meta"]["result"] is True

    def test_false_same_length(self):
        assert anagram.trace("RAT", "CAR")["meta"]["result"] is False

    def test_false_different_length(self):
        assert anagram.trace("AB", "ABC")["meta"]["result"] is False

    def test_repeated_letters(self):
        assert anagram.trace("AABB", "BABA")["meta"]["result"] is True
        assert anagram.trace("AAB", "ABB")["meta"]["result"] is False

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_sorted_compare(self, seed):
        rng = random.Random(seed)
        a = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 8)))
        b = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 8)))
        res = anagram.trace(a, b)
        assert res["meta"]["result"] == (sorted(a) == sorted(b))
        _assert_envelope(res)
        _assert_rectangular(res)


# ── GCD (EUCLID) ──────────────────────────────────────────────────────────

class TestGcdEuclid:
    def test_classic(self):
        assert gcd_euclid.trace(48, 36)["meta"]["result"] == 12

    def test_coprime(self):
        assert gcd_euclid.trace(17, 5)["meta"]["result"] == 1

    def test_one_divides_other(self):
        assert gcd_euclid.trace(100, 25)["meta"]["result"] == 25

    def test_zero(self):
        assert gcd_euclid.trace(0, 7)["meta"]["result"] == 7
        assert gcd_euclid.trace(7, 0)["meta"]["result"] == 7

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_math_gcd(self, seed):
        rng = random.Random(seed)
        a, b = rng.randint(0, 5000), rng.randint(1, 5000)
        res = gcd_euclid.trace(a, b)
        assert res["meta"]["result"] == math.gcd(a, b)
        _assert_envelope(res)


# ── FAST EXPONENTIATION ───────────────────────────────────────────────────

class TestFastExponentiation:
    def test_classic(self):
        assert fast_exponentiation.trace(3, 13)["meta"]["result"] == 3 ** 13

    def test_exponent_zero(self):
        assert fast_exponentiation.trace(7, 0)["meta"]["result"] == 1

    def test_exponent_one(self):
        assert fast_exponentiation.trace(5, 1)["meta"]["result"] == 5

    def test_base_one(self):
        assert fast_exponentiation.trace(1, 20)["meta"]["result"] == 1

    @pytest.mark.parametrize("seed", range(30))
    def test_matches_builtin_pow(self, seed):
        rng = random.Random(seed)
        base, exp = rng.randint(1, 12), rng.randint(0, 20)
        res = fast_exponentiation.trace(base, exp)
        assert res["meta"]["result"] == base ** exp
        _assert_envelope(res)


# ── PRIME FACTORISATION ───────────────────────────────────────────────────

def _is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True


class TestPrimeFactorisation:
    def test_classic(self):
        assert prime_factorisation.trace(360)["meta"]["factors"] == [2, 2, 2, 3, 3, 5]

    def test_prime_input(self):
        assert prime_factorisation.trace(97)["meta"]["factors"] == [97]

    def test_power_of_two(self):
        assert prime_factorisation.trace(64)["meta"]["factors"] == [2, 2, 2, 2, 2, 2]

    def test_two(self):
        assert prime_factorisation.trace(2)["meta"]["factors"] == [2]

    @pytest.mark.parametrize("seed", range(30))
    def test_factors_are_prime_and_multiply_back(self, seed):
        rng = random.Random(seed)
        n = rng.randint(2, 9999)
        res = prime_factorisation.trace(n)
        factors = res["meta"]["factors"]
        assert all(_is_prime(f) for f in factors), "every factor must be prime"
        assert math.prod(factors) == n, "factors must multiply back to n"
        assert factors == sorted(factors), "factors come out ascending"
        _assert_envelope(res)


# ── ENDPOINT WIRING ───────────────────────────────────────────────────────

class TestEndpoints:
    def test_all_four_are_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"anagram", "gcd_euclid", "fast_exponentiation",
                "prime_factorisation"} <= ids

    @pytest.mark.parametrize("payload", [
        {"algorithm": "anagram", "text": "LISTEN,SILENT"},
        {"algorithm": "gcd_euclid", "array": [48, 36]},
        {"algorithm": "fast_exponentiation", "array": [3, 13]},
        {"algorithm": "prime_factorisation", "target": 360},
    ])
    def test_endpoint_returns_a_trace(self, payload):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"], "endpoint returned no steps"
        assert body["meta"]["algorithm"] == payload["algorithm"]

    @pytest.mark.parametrize("payload,fragment", [
        ({"algorithm": "anagram"}, "requires 'text'"),
        ({"algorithm": "anagram", "text": "ONE"}, "two words"),
        ({"algorithm": "gcd_euclid", "array": [0, 0]}, "undefined"),
        ({"algorithm": "fast_exponentiation", "array": [3]}, "two numbers"),
        ({"algorithm": "prime_factorisation", "target": 1}, "from 2 to"),
    ])
    def test_bad_input_is_rejected_with_a_useful_message(self, payload, fragment):
        res = client.post("/api/trace", json=payload)
        assert res.status_code == 400
        assert fragment.lower() in res.json()["detail"].lower()

    @pytest.mark.parametrize("algo_id", ["anagram", "gcd_euclid",
                                         "fast_exponentiation", "prime_factorisation"])
    def test_detect_resolves_an_exact_id_to_itself(self, algo_id):
        body = client.post("/api/detect",
                           json={"code": "", "problem": algo_id}).json()
        assert body["algorithm"] == algo_id
        assert body["realworld"]["scene"], "every algorithm needs a scene"
        assert body["realworld"]["title"]
