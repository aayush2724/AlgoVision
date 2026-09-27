"""Batch 32 — expression conversions (Step 9): all six infix/postfix/prefix
directions. Checked against an independent reference: a recursive-descent
infix parser and recursive postfix/prefix readers that build an expression
tree — every conversion's output must denote the same tree as its input,
over hundreds of random expressions (including right-associative ^ chains).
"""

import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import expr_convert

client = TestClient(app)
PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}


def parse_infix(s):
    pos = 0

    def expr(min_prec):
        nonlocal pos
        left = atom()
        while pos < len(s) and s[pos] in PREC and PREC[s[pos]] >= min_prec:
            op = s[pos]
            pos += 1
            nxt = PREC[op] if op == "^" else PREC[op] + 1   # ^ right-assoc
            left = (op, left, expr(nxt))
        return left

    def atom():
        nonlocal pos
        c = s[pos]
        pos += 1
        if c == "(":
            node = expr(1)
            pos += 1  # ')'
            return node
        return c

    tree = expr(1)
    assert pos == len(s)
    return tree


def parse_postfix(s):
    st = []
    for c in s:
        if c in PREC:
            b, a = st.pop(), st.pop()
            st.append((c, a, b))
        else:
            st.append(c)
    return st.pop()


def parse_prefix(s):
    it = iter(s)

    def rec():
        c = next(it)
        return (c, rec(), rec()) if c in PREC else c
    return rec()


PARSE = {"infix": parse_infix, "postfix": parse_postfix, "prefix": parse_prefix}


def rand_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return rng.choice("ABCDEFG")
    return (rng.choice("+-*/^"), rand_tree(rng, depth - 1), rand_tree(rng, depth - 1))


def to_postfix(t):
    return t if isinstance(t, str) else to_postfix(t[1]) + to_postfix(t[2]) + t[0]


def to_prefix(t):
    return t if isinstance(t, str) else t[0] + to_prefix(t[1]) + to_prefix(t[2])


def to_infix(t, parent_prec=0, right_side=False, parent_op=None):
    """Minimal brackets: only where precedence/associativity demands them."""
    if isinstance(t, str):
        return t
    op = t[0]
    p = PREC[op]
    inner = (to_infix(t[1], p, False, op) + op + to_infix(t[2], p, True, op))
    need = (p < parent_prec
            or (p == parent_prec and parent_op != "^" and right_side)
            or (p == parent_prec and parent_op == "^" and not right_side))
    return f"({inner})" if need else inner


def _cases(n=300, seed=32):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        t = rand_tree(rng, 3)
        if not isinstance(t, str) and len(to_postfix(t)) <= 15 and len(to_infix(t)) <= 15:
            out.append(t)
    return out


class TestConversions:
    def test_reference_round_trip(self):
        for t in _cases(50):
            assert parse_infix(to_infix(t)) == t
            assert parse_postfix(to_postfix(t)) == t
            assert parse_prefix(to_prefix(t)) == t

    def test_all_six_directions(self):
        render = {"infix": to_infix, "postfix": to_postfix, "prefix": to_prefix}
        for t in _cases():
            for algo, (src, dst) in expr_convert.MODES.items():
                text = render[src](t)
                out = expr_convert.trace(text, algo)["meta"]["result"]
                assert PARSE[dst](out) == t, (algo, text, out)

    def test_textbook(self):
        cases = [
            ("infix_to_postfix", "A+B*(C^D-E)^(F+G*H)-I", "ABCD^E-FGH*+^*+I-"),
            ("infix_to_prefix", "(A-B/C)*(A/K-L)", "*-A/BC-/AKL"),
            ("infix_to_postfix", "A^B^C", "ABC^^"),
            ("postfix_to_infix", "AB-DE+F*/", "((A-B)/((D+E)*F))"),
            ("prefix_to_postfix", "/-AK-/BL*CD", "AK-BL/CD*-/"),
        ]
        for algo, src, want in cases:
            assert expr_convert.trace(src, algo)["meta"]["result"] == want

    def test_validate(self):
        assert expr_convert.validate("A+B*C", "infix") is None
        for bad in ("A+", "(A+B", "A+B)", "AB+", "+A", "A++B", "A(B)"):
            assert expr_convert.validate(bad, "infix"), bad
        assert expr_convert.validate("AB+C*", "postfix") is None
        for bad in ("A+B", "AB", "+AB", "AB+*"):
            assert expr_convert.validate(bad, "postfix"), bad
        assert expr_convert.validate("*+ABC", "prefix") is None
        assert expr_convert.validate("AB+", "prefix")


class TestEndpoints:
    def test_endpoints_ok(self):
        for algo, text in (("infix_to_postfix", "A+B*C"), ("infix_to_prefix", "A*(B+C)"),
                           ("postfix_to_infix", "AB+C*"), ("postfix_to_prefix", "AB+C*"),
                           ("prefix_to_infix", "*+ABC"), ("prefix_to_postfix", "*+ABC")):
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"][-1]["structures"]["output"]

    def test_validation(self):
        for algo, text in (("infix_to_postfix", "A+"), ("postfix_to_infix", "A+B"),
                           ("prefix_to_infix", "AB+"), ("infix_to_prefix", "A" * 16),
                           ("postfix_to_prefix", "")):
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 400, (algo, text)

    def test_detect_resolves(self):
        for algo in expr_convert.MODES:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
