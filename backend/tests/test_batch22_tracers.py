"""Batch 22 — Bit manipulation: count set bits (Kernighan), power of two,
single number (XOR), minimum bit flips, power set (bitmask). Each is checked
against Python's own bit operations.
"""

from functools import reduce

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    count_set_bits, power_of_two, single_number, min_bit_flips, power_set,
)

client = TestClient(app)


class TestBitTracers:
    def test_count_set_bits(self):
        for n in (0, 1, 13, 255, 1024, 4095):
            assert count_set_bits.trace(n)["meta"]["set_bits"] == bin(n).count("1"), n

    def test_power_of_two(self):
        for n in (1, 2, 3, 16, 18, 1024, 0):
            assert power_of_two.trace(n)["meta"]["is_power_of_two"] == (n > 0 and (n & (n - 1)) == 0), n

    def test_single_number(self):
        for arr in ([4, 1, 2, 1, 2], [2, 2, 1], [7], [5, 5, 3, 3, 9]):
            assert single_number.trace(arr)["meta"]["single"] == reduce(lambda a, b: a ^ b, arr), arr

    def test_min_bit_flips(self):
        for a, b in ((10, 7), (0, 0), (255, 0), (13, 13), (1, 2)):
            assert min_bit_flips.trace(a, b)["meta"]["flips"] == bin(a ^ b).count("1"), (a, b)

    def test_power_set(self):
        for els in (["A", "B", "C"], ["X"], ["A", "B", "C", "D"]):
            assert power_set.trace(els)["meta"]["count"] == 2 ** len(els), els

    def test_bits_row_width(self):
        # numeric tracers always render a 12-bit row
        assert len(count_set_bits.trace(5)["steps"][0]["structures"]["array"]) == 12
        assert len(single_number.trace([1, 1, 2])["steps"][0]["structures"]["array"]) == 12


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"count_set_bits", "power_of_two", "single_number",
                "min_bit_flips", "power_set"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("count_set_bits", {"text": "13"}),
            ("power_of_two", {"text": "16"}),
            ("single_number", {"text": "4,1,2,1,2"}),
            ("min_bit_flips", {"text": "10 | 7"}),
            ("power_set", {"text": "A,B,C"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        assert client.post("/api/trace", json={"algorithm": "count_set_bits", "text": "abc"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "count_set_bits", "text": "99999"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "min_bit_flips", "text": "10"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "power_set", "text": "A,B,C,D,E,F"}).status_code == 400

    def test_detect_resolves(self):
        for algo in ("count_set_bits", "power_of_two", "single_number",
                     "min_bit_flips", "power_set"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
