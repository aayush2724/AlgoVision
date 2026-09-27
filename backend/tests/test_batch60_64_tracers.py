"""Batches 60–64 — linked lists (list view), hard binary searches, recursion &
backtracking, and greedy/stack leftovers. Each tracer is checked against a
direct or brute-force reference on random input.
"""

import itertools
import random

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    bs_hard as BS, greedy_stack as GS, ll_more as LL, recursion_more as RM,
)

client = TestClient(app)
R = random.Random(60)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))
rand = lambda n, lo, hi: [R.randint(lo, hi) for _ in range(n)]


def walk(out):
    """Follow `next` from the final step's head pointer (list view)."""
    s = out["steps"][-1]["structures"]
    ptr = dict(s["pointers"])
    j, seen = ptr.get("head"), []
    while j is not None and len(seen) <= len(s["values"]):
        seen.append(s["values"][j])
        j = s["next"][j]
    return seen


class TestLinkedListBasics:
    def test_head_ops_length_search(self):
        for _ in range(30):
            a = rand(R.randint(1, 9), -9, 9)
            x = R.randint(-9, 9)
            out = LL.run("ll_insert_head", csv(a), x)
            assert res(out) == [x] + a == walk(out)
            out = LL.run("dll_insert_head", csv(a), x)
            assert res(out) == [x] + a
            prev = out["steps"][-1]["structures"]["prev_links"]
            assert prev[0] is None and prev[1] == 0
            assert res(LL.run("ll_delete_head", csv(a))) == a[1:]
            out = LL.run("dll_delete_head", csv(a))
            assert res(out) == a[1:]
            if len(a) > 1:
                assert out["steps"][-1]["structures"]["prev_links"][1] is None
            assert res(LL.run("ll_length", csv(a))) == len(a)
            assert res(LL.run("ll_search", csv(a), x)) == (a.index(x) if x in a else -1)

    def test_insert_step_redraws_values(self):
        out = LL.run("ll_insert_head", "1,2,3", 9)
        assert out["steps"][0]["structures"]["values"] == [1, 2, 3]
        assert out["steps"][-1]["structures"]["values"] == [9, 1, 2, 3]

    def test_dll_pairs_and_dedupe(self):
        for _ in range(30):
            a = sorted(rand(R.randint(1, 10), 0, 9))
            t = R.randint(0, 18)
            want = []
            l, r = 0, len(a) - 1
            while l < r:                     # the standard two-pointer answer
                s = a[l] + a[r]
                if s == t:
                    want.append([a[l], a[r]])
                    l, r = l + 1, r - 1
                elif s < t:
                    l += 1
                else:
                    r -= 1
            assert res(LL.run("dll_pairs_sum", csv(a), t)) == want
            if len(set(a)) == len(a):
                assert sorted(map(tuple, want)) == sorted(
                    (x, y) for x, y in itertools.combinations(a, 2) if x + y == t)
            assert res(LL.run("dll_remove_duplicates", csv(a))) == sorted(set(a))


class TestLinkedListMedium:
    def test_reverse_sort_group(self):
        for _ in range(30):
            a = rand(R.randint(1, 10), -20, 20)
            out = LL.run("ll_reverse_recursive", csv(a))
            assert res(out) == a[::-1] == walk(out)
            out = LL.run("sort_list", csv(a))
            assert res(out) == sorted(a) == walk(out)
            b = rand(len(a), 0, 2)
            out = LL.run("sort_012_list", csv(b))
            assert res(out) == sorted(b) == walk(out)
            k = R.randint(1, len(a))
            full = len(a) // k * k
            want = [v for i in range(0, full, k) for v in a[i:i + k][::-1]] + a[full:]
            assert res(LL.run("reverse_k_group", csv(a), k)) == want

    def test_loop_length(self):
        for _ in range(30):
            n = R.randint(1, 10)
            to = R.randint(-1, n - 1)
            assert res(LL.run("loop_length", csv(range(n)), to)) == (n - to if to >= 0 else 0)

    def test_y_intersection(self):
        for _ in range(40):
            a, b, c = (rand(R.randint(0, 4), 0, 9) for _ in range(3))
            if not a and not c or not b and not c:
                continue
            out = res(LL.run("y_intersection", f"{csv(a)} | {csv(b)} | {csv(c)}"))
            assert out == (c[0] if c else None)


class TestHardBinarySearch:
    def test_rotated_ii(self):
        for _ in range(60):
            a = sorted(rand(R.randint(1, 12), 0, 5))
            k = R.randint(0, len(a) - 1)
            a = a[k:] + a[:k]
            t = R.randint(0, 6)
            assert res(BS.run("search_rotated_ii", csv(a), t)) == (t in a)

    def test_two_sorted(self):
        for _ in range(60):
            a, b = sorted(rand(R.randint(0, 8), -20, 20)), sorted(rand(R.randint(0, 8), -20, 20))
            if not a and not b:
                continue
            m = sorted(a + b)
            n = len(m)
            med = m[n // 2] if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
            assert res(BS.run("median_two_sorted", f"{csv(a)} | {csv(b)}")) == med
            k = R.randint(1, n)
            assert res(BS.run("kth_two_sorted", f"{csv(a)} | {csv(b)}", k)) == m[k - 1]

    def test_gas_station(self):
        for _ in range(30):
            a = sorted(R.sample(range(0, 60), R.randint(2, 8)))
            k = R.randint(1, 10)
            gaps = [a[i + 1] - a[i] for i in range(len(a) - 1)]
            parts = [1] * len(gaps)
            for _ in range(k):               # exact greedy: split the biggest piece
                i = max(range(len(gaps)), key=lambda j: gaps[j] / parts[j])
                parts[i] += 1
            best = max(g / p for g, p in zip(gaps, parts))
            assert abs(res(BS.run("gas_station", csv(a), k)) - best) < 1e-3

    def test_peak_and_median(self):
        for _ in range(40):
            r, c = R.randint(1, 5), R.randint(1, 5)
            vals = R.sample(range(1, 99), r * c)
            g = [vals[i * c:(i + 1) * c] for i in range(r)]
            pr, pc = res(BS.run("peak_element_ii", "/".join(csv(row) for row in g)))
            nb = [g[pr + dr][pc + dc] for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
                  if 0 <= pr + dr < r and 0 <= pc + dc < c]
            assert all(g[pr][pc] > v for v in nb)
            m = [sorted(rand(R.choice([1, 3, 5]), 0, 30))]
            m += [sorted(rand(len(m[0]), 0, 30)) for _ in range(R.choice([0, 2, 4]))]
            flat = sorted(v for row in m for v in row)
            assert res(BS.run("matrix_median", "/".join(csv(row) for row in m))) == \
                flat[len(flat) // 2]


class TestRecursion:
    def test_prints_and_sorts(self):
        for n in range(1, 11):
            assert res(RM.run("print_1_to_n", str(n))) == list(range(1, n + 1))
            assert res(RM.run("print_n_to_1", str(n))) == list(range(n, 0, -1))
        for _ in range(30):
            a = rand(R.randint(1, 10), -50, 50)
            assert res(RM.run("recursive_bubble_sort", csv(a))) == sorted(a)
            assert res(RM.run("recursive_insertion_sort", csv(a))) == sorted(a)
            s = a[:8]
            assert res(RM.run("sort_stack", csv(s))) == sorted(s)
            assert res(RM.run("reverse_stack", csv(s))) == s[::-1]

    def test_good_numbers(self):
        mod = 10 ** 9 + 7
        for n in list(range(1, 8)) + [50, 10 ** 15]:
            want = pow(5, (n + 1) // 2, mod) * pow(4, n // 2, mod) % mod
            assert res(RM.run("count_good_numbers", str(n))) == want
        for n in range(1, 5):                # brute force over every n-digit string
            brute = sum(all(int(d) % 2 == 0 if i % 2 == 0 else d in "2357"
                            for i, d in enumerate(str(x).zfill(n))) for x in range(10 ** n))
            assert res(RM.run("count_good_numbers", str(n))) == brute

    def test_atoi(self):
        def ref(s):
            s = s.lstrip(" ")
            sign = -1 if s[:1] == "-" else 1
            if s[:1] in ("+", "-"):
                s = s[1:]
            d = ""
            for ch in s:
                if not ch.isdigit():
                    break
                d += ch
            return max(-2 ** 31, min(2 ** 31 - 1, sign * int(d or 0)))
        for s in ["42", "   -42", "4193 with", "words 987", "-91283472332", "+1", "  +0 12",
                  "99999999999", "-", " ", "00012a"]:
            assert res(RM.run("recursive_atoi", s)) == ref(s), s

    def test_word_break(self):
        for _ in range(40):
            words = ["".join(R.choice("ab") for _ in range(R.randint(1, 3)))
                     for _ in range(R.randint(1, 4))]
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))

            def can(i):
                return i == len(s) or any(s.startswith(w, i) and can(i + len(w)) for w in words)
            assert res(RM.run("word_break", f"{s} | {','.join(words)}")) == can(0)

    def test_m_coloring(self):
        for _ in range(30):
            n = R.randint(2, 6)
            edges = sorted({tuple(sorted(R.sample(range(n), 2))) for _ in range(R.randint(1, 8))})
            m = R.randint(1, 4)
            nodes = max(max(e) for e in edges) + 1
            brute = any(all(c[u] != c[v] for u, v in edges)
                        for c in itertools.product(range(m), repeat=nodes))
            out = RM.run("m_coloring", ",".join(f"{u}-{v}" for u, v in edges), m)
            assert res(out) == brute
            if brute:
                col = out["meta"]["coloring"]
                assert all(col[u] != col[v] and 1 <= col[u] <= m for u, v in edges)

    def test_sudoku(self):
        full = [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
        for _ in range(20):
            g = [[v if R.random() < 0.4 else 0 for v in row] for row in full]
            out = res(RM.run("sudoku_solver", "/".join(csv(r) for r in g)))
            assert out is not None
            assert all(sorted(r) == [1, 2, 3, 4] for r in out)
            assert all(sorted(col) == [1, 2, 3, 4] for col in zip(*out))
            assert all(out[r][c] == g[r][c] for r in range(4) for c in range(4) if g[r][c])
        classic = ("530070000/600195000/098000060/800060003/400803001/"
                   "700020006/060000280/000419005/000080079")
        assert res(RM.run("sudoku_solver", classic))[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]

    def test_add_operators(self):
        for _ in range(30):
            s = "".join(R.choice("0123456789") for _ in range(R.randint(1, 4)))
            t = R.randint(-20, 40)
            want = []
            for ops in itertools.product(["", "+", "-", "*"], repeat=len(s) - 1):
                expr = s[0] + "".join(o + d for o, d in zip(ops, s[1:]))
                parts = expr.replace("+", " ").replace("-", " ").replace("*", " ").split()
                if any(len(p) > 1 and p[0] == "0" for p in parts):
                    continue
                if eval(expr) == t:
                    want.append(expr)
            assert sorted(res(RM.run("expression_add_operators", s, t))) == sorted(want)


class TestGreedyStack:
    def test_paren_star(self):
        for _ in range(60):
            s = "".join(R.choice("()*") for _ in range(R.randint(1, 8)))
            brute = False
            for choice in itertools.product(["(", ")", ""], repeat=s.count("*")):
                it = iter(choice)
                t = "".join(next(it) if c == "*" else c for c in s)
                bal = 0
                for c in t:
                    bal += 1 if c == "(" else -1
                    if bal < 0:
                        break
                if bal == 0:
                    brute = True
                    break
            assert res(GS.run("valid_paren_star", s)) == brute, s

    def test_sjf_lru(self):
        for _ in range(30):
            b = rand(R.randint(1, 10), 1, 20)
            s = sorted(b)
            waits = sum(sum(s[:i]) for i in range(len(s)))
            assert res(GS.run("shortest_job_first", csv(b))) == round(waits / len(b), 2)
            pages = rand(R.randint(1, 14), 0, 6)
            cap = R.randint(1, 4)
            cache, faults = [], 0
            for p in pages:
                if p in cache:
                    cache.remove(p)
                else:
                    faults += 1
                    if len(cache) == cap:
                        cache.pop(0)
                cache.append(p)
            assert res(GS.run("lru_page_faults", csv(pages), cap)) == faults

    def test_intervals(self):
        for _ in range(40):
            pts = sorted(R.sample(range(0, 40), 2 * R.randint(1, 5)))
            ivs = [[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)]
            s = R.randint(0, 40)
            e = R.randint(s, 45)
            merged = []
            for x, y in sorted(ivs + [[s, e]]):
                if merged and x <= merged[-1][1]:
                    merged[-1][1] = max(merged[-1][1], y)
                else:
                    merged.append([x, y])
            text = ",".join(f"{x}-{y}" for x, y in ivs)
            assert res(GS.run("insert_interval", f"{text} | {s}-{e}")) == merged
            raw = []
            for _ in range(R.randint(1, 7)):
                x = R.randint(0, 15)
                raw.append([x, x + R.randint(1, 6)])
            best = max(k for k in range(len(raw) + 1) for keep in itertools.combinations(raw, k)
                       if all(p[1] <= q[0] or q[1] <= p[0]
                              for p, q in itertools.combinations(keep, 2)))
            assert res(GS.run("non_overlapping_intervals",
                              ",".join(f"{x}-{y}" for x, y in raw))) == len(raw) - best

    def test_counts_and_ranges(self):
        for _ in range(40):
            a = rand(R.randint(1, 10), -20, 20)
            assert res(GS.run("greater_to_right", csv(a))) == \
                [sum(a[j] > a[i] for j in range(i + 1, len(a))) for i in range(len(a))]
            assert res(GS.run("sum_subarray_ranges", csv(a))) == \
                sum(max(a[i:j]) - min(a[i:j]) for i in range(len(a))
                    for j in range(i + 1, len(a) + 1))

    def test_celebrity(self):
        for _ in range(40):
            n = R.randint(1, 6)
            m = [[0 if i == j else R.randint(0, 1) for j in range(n)] for i in range(n)]
            if R.random() < 0.5:
                c = R.randrange(n)
                for i in range(n):
                    if i != c:
                        m[i][c], m[c][i] = 1, 0
            want = next((c for c in range(n)
                         if all(m[c][j] == 0 for j in range(n) if j != c)
                         and all(m[i][c] == 1 for i in range(n) if i != c)), -1)
            assert res(GS.run("celebrity", "/".join(csv(r) for r in m))) == want


class TestWiring:
    def test_every_id_through_api(self):
        samples = {
            "ll_delete_head": "1,2", "ll_length": "1,2", "dll_delete_head": "1,2",
            "dll_remove_duplicates": "1,1,2", "ll_reverse_recursive": "1,2,3",
            "sort_012_list": "2,0,1", "sort_list": "3,1,2", "y_intersection": "1 | 2 | 3",
            "median_two_sorted": "1,3 | 2", "peak_element_ii": "1,2/3,4",
            "matrix_median": "1,2,3", "print_1_to_n": "3", "print_n_to_1": "3",
            "recursive_bubble_sort": "3,1,2", "recursive_insertion_sort": "3,1,2",
            "count_good_numbers": "4", "sort_stack": "3,1,2", "reverse_stack": "1,2,3",
            "recursive_atoi": " -42", "word_break": "ab | a,b",
            "sudoku_solver": "1,0,0,0/0,0,3,0/0,4,0,0/0,0,0,2",
            "valid_paren_star": "(*)", "shortest_job_first": "3,1,2",
            "insert_interval": "1-3,6-9 | 2-5", "non_overlapping_intervals": "1-2,1-3",
            "greater_to_right": "3,1,2", "sum_subarray_ranges": "1,2,3",
            "celebrity": "0,1/0,0"}
        with_target = {
            "ll_insert_head": ("1,2", 0), "ll_search": ("1,2", 2), "dll_insert_head": ("1,2", 0),
            "dll_pairs_sum": ("1,2,3", 4), "loop_length": ("1,2,3", 0),
            "reverse_k_group": ("1,2,3", 2), "search_rotated_ii": ("2,0,1", 1),
            "kth_two_sorted": ("1,3 | 2", 2), "gas_station": ("1,5", 1),
            "m_coloring": ("0-1", 2), "expression_add_operators": ("123", 6),
            "lru_page_faults": ("1,2,1", 2)}
        every = set(LL.TITLES) | set(BS.TITLES) | set(RM.TITLES) | set(GS.TITLES)
        assert set(samples) | set(with_target) == every
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["meta"]["view"] == ("list" if algo in LL.TITLES else "grid")
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        for algo in every:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "dll_pairs_sum", "text": "3,1", "target": 4},
                  {"algorithm": "sort_012_list", "text": "0,3"},
                  {"algorithm": "loop_length", "text": "1,2", "target": 5},
                  {"algorithm": "reverse_k_group", "text": "1,2", "target": 0},
                  {"algorithm": "y_intersection", "text": "1,2 | 3"},
                  {"algorithm": "median_two_sorted", "text": "3,1 | 2"},
                  {"algorithm": "peak_element_ii", "text": "1,1/2,3"},
                  {"algorithm": "matrix_median", "text": "1,2/3,4"},
                  {"algorithm": "gas_station", "text": "5,1", "target": 1},
                  {"algorithm": "print_1_to_n", "text": "11"},
                  {"algorithm": "word_break", "text": "abc"},
                  {"algorithm": "m_coloring", "text": "0-0", "target": 2},
                  {"algorithm": "sudoku_solver", "text": "1,1,0,0/0,0,0,0/0,0,0,0/0,0,0,0"},
                  {"algorithm": "expression_add_operators", "text": "123456", "target": 1},
                  {"algorithm": "valid_paren_star", "text": "(a)"},
                  {"algorithm": "insert_interval", "text": "1-5,3-7 | 2-3"},
                  {"algorithm": "celebrity", "text": "0,1,0/0,0,0"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
