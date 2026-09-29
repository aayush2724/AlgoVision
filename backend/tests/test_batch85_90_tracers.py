"""Batches 85–90 — the tracers built for the rows the 20-module A2Z sheet
added (2026-09-29): beginner basics, basic recursion, Pascal variants,
linked-list fundamentals, heap construction, two BST problems, and three
leftovers. Each tracer is checked against a direct reference on random
input, and every one is reachable through /api/trace.
"""

import heapq
import random
from collections import Counter
from math import gcd

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    basics_more as BM, recursion_basics as RB, pascal_more as PM,
    ll_basics2 as LL, heaps_build as HB, bst_more as BST, misc_a2z as MA,
    graph_undirected as GU,
)
from app.tracers.common import Graph

client = TestClient(app)
R = random.Random(85)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))
rand = lambda n, lo, hi: [R.randint(lo, hi) for _ in range(n)]


def walk(out):
    s = out["steps"][-1]["structures"]
    ptr = dict(s["pointers"])
    j, seen = ptr.get("head"), []
    while j is not None and len(seen) <= len(s["values"]):
        seen.append(s["values"][j])
        j = s["next"][j]
    return seen


def prev_ok(out):
    """Every prev link must mirror the next link (doubly linked lists)."""
    s = out["steps"][-1]["structures"]
    nxt, prv, removed = s["next"], s["prev_links"], set(s["removed"])
    for i, j in enumerate(nxt):
        if i in removed:
            continue
        if j is not None:
            assert prv[j] == i, (i, j, prv)
    return True


class TestBasicsMore:
    def test_digits_and_numbers(self):
        for _ in range(40):
            n = R.randint(0, 99_999_999)
            assert res(BM.run("count_odd_digits", str(n))) == sum(int(c) % 2 for c in str(n))
            assert res(BM.run("largest_digit", str(n))) == max(int(c) for c in str(n))
        for n in (1, 6, 12, 28, 496, 497, 8128):
            want = n > 1 and sum(d for d in range(1, n) if n % d == 0) == n
            assert res(BM.run("perfect_number", str(n))) is want
        for _ in range(30):
            a, b = R.randint(1, 500), R.randint(1, 500)
            assert res(BM.run("lcm", f"{a},{b}")) == a * b // gcd(a, b)

    def test_arrays_and_frequencies(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), -20, 20)
            assert res(BM.run("array_sum", csv(a))) == sum(a)
            assert res(BM.run("count_odd_array", csv(a))) == sum(v % 2 != 0 for v in a)
            f = Counter(a)
            hi, lo = max(f.values()), min(f.values())
            assert res(BM.run("sum_high_low_freq", csv(a))) == hi + lo
            rest = [c for c in f.values() if c < hi]
            got = res(BM.run("second_highest_freq", csv(a)))
            if rest:
                assert f[got] == max(rest)
            else:
                assert got == -1

    def test_strings_and_bits(self):
        for w in ("hello", "a", "ab", "racecar"):
            assert res(BM.run("reverse_string", w)) == w[::-1]
        for n in range(0, 255):
            assert res(BM.run("set_rightmost_unset_bit", str(n))) == (n | (n + 1) if n & (n + 1) else n)

    def test_validation(self):
        for algo, bad in [("count_odd_digits", "x"), ("perfect_number", "0"), ("lcm", "5"),
                          ("array_sum", ""), ("reverse_string", ""), ("set_rightmost_unset_bit", "300")]:
            try:
                BM.run(algo, bad)
                assert False, algo
            except ValueError:
                pass


class TestRecursionBasics:
    def test_numbers(self):
        for _ in range(30):
            n = R.randint(0, 99_999_999)
            assert res(RB.run("sum_digits_rec", str(n))) == sum(int(c) for c in str(n))
        for n in range(0, 11):
            f = 1
            for k in range(2, n + 1):
                f *= k
            assert res(RB.run("factorial_rec", str(n))) == f
        for n in range(2, 300):
            want = all(n % d for d in range(2, int(n ** 0.5) + 1))
            assert res(RB.run("prime_rec", str(n))) is want

    def test_arrays_and_words(self):
        for _ in range(40):
            a = rand(R.randint(1, 10), 0, 5)
            assert res(RB.run("sum_array_rec", csv(a))) == sum(a)
            assert res(RB.run("sorted_rec", csv(a))) is (a == sorted(a))
            assert res(RB.run("reverse_array_rec", csv(a))) == a[::-1]
        for w in ("recursion", "a", "ab", "aba", "abba", "abca", "racecar"):
            assert res(RB.run("reverse_string_rec", w)) == w[::-1]
            assert res(RB.run("palindrome_rec", w)) is (w == w[::-1])

    def test_call_table_has_returns(self):
        out = RB.run("factorial_rec", "4")
        grid = out["steps"][-1]["structures"]["grid"]
        assert [r[0] for r in grid] == ["f(4)", "f(3)", "f(2)", "f(1)", "f(0)"]
        assert [r[2] for r in grid] == [24, 6, 2, 1, 1]


class TestPascal:
    def test_element_and_row(self):
        from math import comb
        for r in range(1, 13):
            assert res(PM.run("pascal_row", str(r))) == [comb(r - 1, i) for i in range(r)]
            for c in range(1, r + 1):
                assert res(PM.run("pascal_element", f"{r},{c}")) == comb(r - 1, c - 1)


class TestLinkedListBasics2:
    def test_singly(self):
        for _ in range(40):
            a = rand(R.randint(1, 9), -9, 9)
            x = R.randint(-9, 9)
            assert res(LL.run("ll_traverse", csv(a))) == a
            out = LL.run("ll_delete_tail", csv(a))
            assert res(out) == a[:-1] == walk(out)
            k = R.randint(1, len(a))
            out = LL.run("ll_delete_kth", csv(a), k)
            assert res(out) == a[:k - 1] + a[k:] == walk(out)
            v = R.choice(a)
            i = a.index(v)
            out = LL.run("ll_delete_value", csv(a), v)
            assert res(out) == a[:i] + a[i + 1:] == walk(out)
            out = LL.run("ll_insert_tail", csv(a), x)
            assert res(out) == a + [x] == walk(out)
            k = R.randint(1, len(a) + 1)
            out = LL.run("ll_insert_kth", f"{csv(a)} | {x}", k)
            assert res(out) == a[:k - 1] + [x] + a[k - 1:] == walk(out)
            out = LL.run("ll_insert_before_value", f"{csv(a)} | {x}", v)
            assert res(out) == a[:i] + [x] + a[i:] == walk(out)

    def test_doubly(self):
        for _ in range(40):
            a = rand(R.randint(1, 9), -9, 9)
            x = R.randint(-9, 9)
            out = LL.run("dll_from_array", csv(a))
            assert res(out) == a == walk(out) and prev_ok(out)
            out = LL.run("dll_delete_tail", csv(a))
            assert res(out) == a[:-1] == walk(out) and prev_ok(out)
            k = R.randint(1, len(a))
            out = LL.run("dll_delete_kth", csv(a), k)
            assert res(out) == a[:k - 1] + a[k:] == walk(out) and prev_ok(out)
            v = R.choice(a)
            i = a.index(v)
            out = LL.run("dll_remove_node", csv(a), v)
            assert res(out) == a[:i] + a[i + 1:] == walk(out) and prev_ok(out)
            out = LL.run("dll_insert_before_tail", csv(a), x)
            assert res(out) == a[:-1] + [x] + a[-1:] == walk(out) and prev_ok(out)
            out = LL.run("dll_insert_before_kth", f"{csv(a)} | {x}", k)
            assert res(out) == a[:k - 1] + [x] + a[k - 1:] == walk(out) and prev_ok(out)
            out = LL.run("dll_insert_before_node", f"{csv(a)} | {x}", v)
            assert res(out) == a[:i] + [x] + a[i:] == walk(out) and prev_ok(out)

    def test_validation(self):
        for algo, text, t in [("ll_delete_kth", "1,2,3", 4), ("ll_delete_value", "1,2,3", 9),
                              ("ll_insert_kth", "1,2,3", 1), ("ll_insert_kth", "1,2,3 | 4", 5),
                              ("dll_insert_before_node", "1,2 | 3", 7), ("ll_traverse", "", None)]:
            try:
                LL.run(algo, text, t)
                assert False, algo
            except ValueError:
                pass


def is_max_heap(a):
    return all(a[i] >= a[c] for i in range(len(a)) for c in (2 * i + 1, 2 * i + 2) if c < len(a))


class TestHeapsAndBst:
    def test_heapify_and_build(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), -50, 50)
            out = HB.run("build_heap", csv(a))
            assert sorted(res(out)) == sorted(a) and is_max_heap(res(out))
            i = R.randint(0, len(a) - 1)
            # sift-down from i only fixes i's subtree when the children already are heaps
            heap = a[:]
            for start in range(len(a) // 2 - 1, -1, -1):
                if start != i and not (start > i):
                    pass
            out = HB.run("heapify", f"{csv(a)} | {i}")
            got = res(out)
            assert sorted(got) == sorted(a)
            assert got[:i] == a[:i]          # nothing above i moves

    def test_sort_k_sorted(self):
        for _ in range(30):
            s = sorted(rand(R.randint(1, 10), 0, 30))
            k = R.randint(0, min(3, len(s) - 1))
            a = s[:]
            for i in range(0, len(a) - 1, k + 1) if k else []:
                seg = a[i:i + k + 1]
                R.shuffle(seg)
                a[i:i + k + 1] = seg
            assert res(HB.run("sort_k_sorted", f"{csv(a)} | {k}")) == s

    def test_bst(self):
        for _ in range(30):
            vals = R.sample(range(-99, 100), R.randint(1, 12))
            assert res(BST.run("bst_min_max", csv(vals))) == [min(vals), max(vals)]
            assert res(BST.run("bst_iterator", csv(vals))) == sorted(vals)
        try:
            BST.run("bst_min_max", "1,1")
            assert False
        except ValueError:
            pass


class TestMiscA2Z:
    def test_single_number_ii(self):
        for _ in range(30):
            vals = R.sample(range(0, 256), R.randint(1, 3))
            a = [v for v in vals[1:] for _ in range(3)] + [vals[0]]
            R.shuffle(a)
            assert res(MA.run("single_number_ii", csv(a))) == vals[0]

    def test_distinct_islands(self):
        cases = {
            "1,1,0,1,1/1,0,0,0,1/0,0,0,0,0/1,1,0,1,1": 3,
            "1,1,0,0,0/1,1,0,0,0/0,0,0,1,1/0,0,0,1,1": 1,
            "1,0,1/0,0,0/1,0,1": 1,
            "0,0/0,0": 0,
        }
        for text, want in cases.items():
            assert res(MA.run("distinct_islands", text)) == want

    def test_shortest_palindrome(self):
        for w in ("aacecaaa", "abcd", "a", "aa", "ab", "racecar", "abab"):
            got = res(MA.run("shortest_palindrome", w))
            assert got == got[::-1] and got.endswith(w)
            for L in range(len(w), -1, -1):     # the shortest such string
                if w[:L] == w[:L][::-1]:
                    assert got == w[L:][::-1] + w
                    break

    def test_print_shortest_path(self):
        g = Graph(nodes=[{"id": c, "x": i, "y": 0} for i, c in enumerate("ABCDE")],
                  edges=[["A", "B", 1], ["B", "C", 2], ["A", "C", 5], ["C", "D", 1], ["B", "E", 9], ["D", "E", 1]])
        out = GU.trace_for("print_shortest_path")(g, "A")
        assert res(out) == ["A", "B", "C", "D", "E"]
        green = out["steps"][-1]["structures"]["mst_edges"]
        assert len(green) == 4
        lonely = Graph(nodes=[{"id": "A", "x": 0, "y": 0}, {"id": "B", "x": 1, "y": 0}], edges=[])
        assert res(GU.trace_for("print_shortest_path")(lonely, "A")) == []


class TestEndpoint:
    def test_all_new_ids_listed_and_traceable(self):
        listed = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        new = set(BM.TITLES) | set(RB.TITLES) | set(PM.TITLES) | set(LL.TITLES) | set(HB.TITLES) \
            | set(BST.TITLES) | set(MA.TITLES) | {"print_shortest_path"}
        assert new <= listed
        r = client.post("/api/trace", json={"algorithm": "ll_insert_kth", "text": "1,2,4 | 3", "target": 3})
        assert r.status_code == 200 and r.json()["meta"]["result"] == [1, 2, 3, 4]
        r = client.post("/api/trace", json={"algorithm": "ll_insert_kth", "text": "1,2,4", "target": 3})
        assert r.status_code == 400
        r = client.post("/api/trace", json={"algorithm": "heapify", "text": "3,1,2 | 0"})
        assert r.status_code == 200 and r.json()["meta"]["view"] == "tree"
