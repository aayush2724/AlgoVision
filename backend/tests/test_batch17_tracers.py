"""Batch 17 (Tier C, greedy) — Huffman coding: the greedy optimal-prefix-code
build on the shared tree view.

Checked against the two invariants that define a correct Huffman code:
  * it is prefix-free (no code is a prefix of another), and
  * total packed bits are minimal — never worse than a flat fixed-length code,
    and more-frequent symbols get codes no longer than rarer ones.
"""

import math
from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import huffman

client = TestClient(app)


def _codes(text):
    return huffman.trace(text)["meta"]["codes"]


def _roots(tree):
    child = set()
    for nd in tree:
        for c in (nd["left"], nd["right"]):
            if c is not None:
                child.add(c)
    return [nd["id"] for nd in tree if nd["id"] not in child]


class TestHuffmanTracer:
    def test_prefix_free(self):
        codes = list(_codes("ABRACADABRA").values())
        for a in codes:
            for b in codes:
                if a is not b:
                    assert not a.startswith(b), f"{a} has prefix {b}"

    def test_every_symbol_gets_a_code(self):
        text = "MISSISSIPPI"
        codes = _codes(text)
        assert set(codes) == set(text)

    def test_more_frequent_is_never_longer(self):
        text = "ABRACADABRA"
        freq = Counter(text)
        codes = _codes(text)
        for x in freq:
            for y in freq:
                if freq[x] > freq[y]:
                    assert len(codes[x]) <= len(codes[y])

    def test_beats_or_ties_fixed_length(self):
        text = "ABRACADABRA"
        r = huffman.trace(text)
        n_distinct = len(set(text))
        fixed = len(text) * max(1, math.ceil(math.log2(n_distinct)))
        assert r["meta"]["huffman_bits"] <= fixed
        assert r["meta"]["fixed_bits"] == fixed

    def test_huffman_bits_match_codes(self):
        text = "ABRACADABRA"
        r = huffman.trace(text)
        freq = Counter(text)
        codes = r["meta"]["codes"]
        assert r["meta"]["huffman_bits"] == sum(freq[c] * len(codes[c]) for c in freq)

    def test_forest_converges_to_one_tree(self):
        r = huffman.trace("ABRACADABRA")
        # First step: every distinct char is its own root.
        assert len(_roots(r["steps"][0]["structures"]["tree"])) == len(set("ABRACADABRA"))
        # Last step: a single tree.
        assert len(_roots(r["steps"][-1]["structures"]["tree"])) == 1

    def test_tree_nodes_carry_render_fields(self):
        node = huffman.trace("ABAB")["steps"][-1]["structures"]["tree"][0]
        assert {"id", "value", "depth", "x", "left", "right"} <= set(node)

    def test_two_distinct_minimum_works(self):
        codes = _codes("AAAB")
        assert set(codes) == {"A", "B"}
        assert codes["A"] != codes["B"]


class TestEndpoints:
    def test_is_listed(self):
        ids = {a["id"] for a in
               client.get("/api/trace/algorithms").json()["algorithms"]}
        assert "huffman" in ids

    def test_endpoint_returns_a_trace(self):
        res = client.post("/api/trace",
                          json={"algorithm": "huffman", "text": "ABRACADABRA"})
        assert res.status_code == 200, res.text
        body = res.json()
        assert body["steps"]
        assert body["meta"]["algorithm"] == "huffman"
        assert body["meta"]["codes"]

    def test_rejects_single_distinct_char(self):
        res = client.post("/api/trace",
                          json={"algorithm": "huffman", "text": "AAAA"})
        assert res.status_code == 400

    def test_rejects_missing_text(self):
        res = client.post("/api/trace", json={"algorithm": "huffman"})
        assert res.status_code == 400

    def test_rejects_too_long(self):
        res = client.post("/api/trace",
                          json={"algorithm": "huffman", "text": "A" * 25 + "B"})
        assert res.status_code == 400

    def test_detect_resolves_id(self):
        body = client.post("/api/detect",
                           json={"code": "", "problem": "huffman"}).json()
        assert body["algorithm"] == "huffman"
        assert body["realworld"]["scene"]
        assert body["realworld"]["title"]
