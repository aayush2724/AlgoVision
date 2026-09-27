"""Batches 55–59 — interval DP & subset tables, array scans, hashing/prefix
sums, matrix & merge problems, and Step 1 basics / Step 8 bit tricks. Each
tracer is checked against a brute-force reference on random input.
"""

import functools
import itertools
import math
import random
from collections import Counter

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import arrays_more as A, basics as B, dp_interval as D

client = TestClient(app)
R = random.Random(55)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))
rand = lambda n, lo, hi: [R.randint(lo, hi) for _ in range(n)]
subarrays = lambda a: [a[i:j] for i in range(len(a)) for j in range(i + 1, len(a) + 1)]


def xor_all(vals):
    return functools.reduce(lambda x, y: x ^ y, vals, 0)


class TestIntervalDP:
    def test_cut_stick(self):
        def brute(lo, hi, cuts):
            inside = [c for c in cuts if lo < c < hi]
            return min((hi - lo + brute(lo, c, inside) + brute(c, hi, inside)
                        for c in inside), default=0)
        for _ in range(30):
            n = R.randint(2, 20)
            cuts = R.sample(range(1, n), R.randint(1, min(5, n - 1)))
            assert res(D.run("cut_stick", f"{n} | {csv(cuts)}")) == brute(0, n, cuts)

    def test_burst_balloons(self):
        def brute(a):
            if not a:
                return 0
            return max((a[i - 1] if i else 1) * a[i] * (a[i + 1] if i + 1 < len(a) else 1)
                       + brute(a[:i] + a[i + 1:]) for i in range(len(a)))
        for _ in range(30):
            a = rand(R.randint(1, 6), 0, 9)
            assert res(D.run("burst_balloons", csv(a))) == brute(a)

    def test_boolean_evaluation(self):
        ops = {"&": lambda x, y: x and y, "|": lambda x, y: x or y, "^": lambda x, y: x != y}

        def values(s):
            if len(s) == 1:
                return [s == "T"]
            return [ops[s[k]](x, y) for k in range(1, len(s), 2)
                    for x in values(s[:k]) for y in values(s[k + 1:])]
        for _ in range(30):
            n = R.randint(1, 6)
            s = "".join(R.choice("TF") + (R.choice("&|^") if i < n - 1 else "")
                        for i in range(n))
            assert res(D.run("boolean_evaluation", s)) == sum(values(s)), s

    def test_palindrome_partition_ii(self):
        def brute(s):
            if s == s[::-1]:
                return 0
            return min(1 + brute(s[i:]) for i in range(1, len(s)) if s[:i] == s[:i][::-1])
        for _ in range(30):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))
            assert res(D.run("palindrome_partition_ii", s)) == brute(s), s

    def test_partition_array_max_sum(self):
        @functools.lru_cache(None)
        def brute(a, k):
            if not a:
                return 0
            return max(max(a[:j]) * j + brute(a[j:], k) for j in range(1, min(k, len(a)) + 1))
        for _ in range(30):
            a = rand(R.randint(1, 10), 0, 99)
            k = R.randint(1, len(a))
            assert res(D.run("partition_array_max_sum", csv(a), k)) == brute(tuple(a), k)

    def test_subset_family(self):
        for _ in range(40):
            a = rand(R.randint(1, 6), 0, 4)
            total = sum(a)
            masks = list(itertools.product((0, 1), repeat=len(a)))
            sums = [sum(x for x, m in zip(a, ms) if m) for ms in masks]
            assert res(D.run("min_subset_diff", csv(a))) == min(abs(total - 2 * s) for s in sums)
            d = R.randint(0, total)
            assert res(D.run("count_partitions_diff", csv(a), d)) == \
                sum(1 for s in sums if (total - s) - s == d)
            t = R.randint(-total, total)
            assert res(D.run("target_sum", csv(a), t)) == \
                sum(1 for s in sums if s - (total - s) == t)

    def test_max_rectangle(self):
        for _ in range(30):
            r, c = R.randint(1, 6), R.randint(1, 6)
            g = [rand(c, 0, 1) for _ in range(r)]
            best = max((r2 - r1 + 1) * (c2 - c1 + 1)
                       for r1 in range(r) for r2 in range(r1, r)
                       for c1 in range(c) for c2 in range(c1, c)
                       if all(g[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
                       ) if any(map(any, g)) else 0
            text = "/".join(csv(row) for row in g)
            assert res(D.run("max_rectangle_ones", text)) == best


class TestArrayScans:
    def test_simple_scans(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), -50, 50)
            assert res(A.run("largest_element", csv(a))) == max(a)
            assert res(A.run("check_sorted", csv(a))) == (a == sorted(a))
            assert res(A.run("check_sorted", csv(sorted(a)))) is True
            x = R.choice(a + [99])
            assert res(A.run("linear_search", csv(a), x)) == (a.index(x) if x in a else -1)
            b = rand(len(a), 0, 1)
            longest = max((len(s) for s in subarrays(b) if all(v == 1 for v in s)), default=0)
            assert res(A.run("max_consecutive_ones", csv(b))) == longest
            assert res(A.run("max_product_subarray", csv(a[:8]))) == \
                max(math.prod(s) for s in subarrays(a[:8]))

    def test_two_sorted(self):
        for _ in range(40):
            a, b = sorted(rand(R.randint(1, 8), 0, 9)), sorted(rand(R.randint(1, 8), 0, 9))
            text = f"{csv(a)} | {csv(b)}"
            assert res(A.run("union_sorted", text)) == sorted(set(a) | set(b))
            assert res(A.run("intersection_sorted", text)) == sorted((Counter(a) & Counter(b)).elements())
            assert res(A.run("merge_no_space", text)) == [sorted(a + b)[:len(a)], sorted(a + b)[len(a):]]

    def test_missing_and_sign(self):
        for _ in range(30):
            n = R.randint(1, 11)
            m = R.randint(0, n)
            a = [v for v in range(n + 1) if v != m]
            R.shuffle(a)
            assert res(A.run("missing_number", csv(a))) == m
            pos, neg = rand(3, 1, 9), rand(3, -9, -1)
            a = pos + neg
            R.shuffle(a)
            out = res(A.run("rearrange_by_sign", csv(a)))
            assert out[0::2] == [v for v in a if v > 0] and out[1::2] == [v for v in a if v < 0]


class TestHashingPrefix:
    def test_prefix_family(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), -5, 5)
            k = R.randint(-5, 5)
            subs = subarrays(a)
            assert res(A.run("longest_sum_k_any", csv(a), k)) == \
                max((len(s) for s in subs if sum(s) == k), default=0)
            assert res(A.run("count_sum_k", csv(a), k)) == sum(sum(s) == k for s in subs)
            assert res(A.run("largest_zero_sum", csv(a))) == \
                max((len(s) for s in subs if sum(s) == 0), default=0)
            b = rand(len(a), 0, 7)
            kx = R.randint(0, 7)
            assert res(A.run("count_xor_k", csv(b), kx)) == \
                sum(xor_all(s) == kx for s in subarrays(b))

    def test_consecutive_and_majority(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), 0, 15)
            s = set(a)
            best = max(next(L for L in itertools.count(1) if v + L not in s) for v in s)
            assert res(A.run("longest_consecutive", csv(a))) == best
            b = rand(R.randint(1, 12), 0, 3)
            assert res(A.run("majority_n3", csv(b))) == \
                sorted(v for v, c in Counter(b).items() if c > len(b) // 3)

    def test_repeating_missing(self):
        for _ in range(30):
            n = R.randint(2, 12)
            rep, mis = R.sample(range(1, n + 1), 2)
            a = [rep if v == mis else v for v in range(1, n + 1)]
            R.shuffle(a)
            assert res(A.run("repeating_missing", csv(a))) == [rep, mis]

    def test_k_sum(self):
        for _ in range(30):
            a = rand(R.randint(3, 10), -5, 5)
            three = sorted({tuple(sorted(c)) for c in itertools.combinations(a, 3) if sum(c) == 0})
            assert sorted(map(tuple, res(A.run("three_sum", csv(a))))) == three
            t = R.randint(-5, 5)
            four = sorted({tuple(sorted(c)) for c in itertools.combinations(a, 4) if sum(c) == t})
            assert sorted(map(tuple, res(A.run("four_sum", csv(a), t)))) == four


class TestMatrixMerge:
    def test_matrix(self):
        for _ in range(30):
            r, c = R.randint(1, 6), R.randint(1, 6)
            g = [rand(c, 0, 3) for _ in range(r)]
            text = "/".join(csv(row) for row in g)
            zr = {i for i in range(r) if 0 in g[i]}
            zc = {j for j in range(c) if any(g[i][j] == 0 for i in range(r))}
            assert res(A.run("set_matrix_zeros", text)) == \
                [[0 if i in zr or j in zc else g[i][j] for j in range(c)] for i in range(r)]
            spiral, m = [], [row[:] for row in g]
            while m:
                spiral += m.pop(0)
                m = [list(x) for x in zip(*m)][::-1]
            assert res(A.run("spiral_order", text)) == spiral
            sq = [rand(r, 0, 9) for _ in range(r)]
            assert res(A.run("rotate_matrix", "/".join(csv(row) for row in sq))) == \
                [list(x) for x in zip(*sq[::-1])]

    def test_pascal(self):
        for n in range(1, 9):
            assert res(A.run("pascal_triangle", "", n)) == \
                [[math.comb(i, j) for j in range(i + 1)] for i in range(n)]

    def test_merge_counts(self):
        for _ in range(40):
            a = rand(R.randint(1, 12), -20, 20)
            pairs = list(itertools.combinations(range(len(a)), 2))
            assert res(A.run("count_inversions", csv(a))) == sum(a[i] > a[j] for i, j in pairs)
            assert res(A.run("reverse_pairs", csv(a))) == sum(a[i] > 2 * a[j] for i, j in pairs)


class TestBasicsBits:
    def test_number_basics(self):
        for n in [0, 7, 10, 121, 153, 370, 9474, 12321, 1200] + rand(20, 0, 99999):
            s = str(n)
            assert res(B.run("count_digits", s)) == len(s)
            assert res(B.run("reverse_number", s)) == int(s[::-1])
            assert res(B.run("palindrome_number", s)) == (s == s[::-1])
            assert res(B.run("armstrong_number", s)) == (sum(int(d) ** len(s) for d in s) == n)
        for n in range(1, 200):
            assert res(B.run("print_divisors", str(n))) == [d for d in range(1, n + 1) if n % d == 0]
            assert res(B.run("check_prime", str(n))) == (n > 1 and all(n % d for d in range(2, n)))
        for n in range(13):
            assert res(B.run("factorial", str(n))) == math.factorial(n)
        assert res(B.run("sum_first_n", "100")) == 5050

    def test_array_string_basics(self):
        for _ in range(30):
            a = rand(R.randint(1, 12), -9, 9)
            assert res(B.run("reverse_array", csv(a))) == a[::-1]
            out = res(B.run("frequency_count", csv(a)))
            c = Counter(a)
            assert out["counts"] == {str(k): v for k, v in c.items()}
            assert c[out["highest"]] == max(c.values()) and c[out["lowest"]] == min(c.values())
        for s, want in [("racecar", True), ("A man, a plan", False), ("Madam", True),
                        ("ab", False), ("x", True), ("Was it a cat", False)]:
            assert res(B.run("palindrome_string", s)) == want, s

    def test_bits(self):
        for _ in range(40):
            n, i = R.randint(0, 255), R.randint(0, 7)
            assert res(B.run("check_ith_bit", str(n), i)) == bool(n >> i & 1)
            assert res(B.run("check_odd", str(n))) == (n % 2 == 1)
            a, b = R.randint(0, 255), R.randint(1, 255)
            assert res(B.run("swap_xor", f"{a}, {b}")) == [b, a]
            assert res(B.run("divide_bits", f"{a}, {b}")) == a // b
            lo = R.randint(0, 999)
            hi = R.randint(lo, 999)
            assert res(B.run("xor_range", f"{lo}, {hi}")) == xor_all(range(lo, hi + 1))
            assert res(B.run("xor_range", str(hi))) == xor_all(range(1, hi + 1))

    def test_single_number_iii(self):
        for _ in range(30):
            vals = R.sample(range(0, 60), R.randint(2, 6))
            x, y = vals[:2]
            a = [x, y] + [v for v in vals[2:] for _ in range(2)]
            R.shuffle(a)
            assert res(B.run("single_number_iii", csv(a))) == sorted([x, y])


class TestWiring:
    def test_every_id_through_api(self):
        samples = {"cut_stick": "7 | 1,3,4,5", "burst_balloons": "3,1,5,8",
                   "boolean_evaluation": "T|F&T^F", "palindrome_partition_ii": "aab",
                   "min_subset_diff": "1,6,11,5", "max_rectangle_ones": "1,0/1,1",
                   "largest_element": "3,9", "check_sorted": "1,2", "union_sorted": "1,2 | 2,3",
                   "intersection_sorted": "1,2 | 2,3", "missing_number": "0,2",
                   "max_consecutive_ones": "1,1,0", "rearrange_by_sign": "1,-1",
                   "max_product_subarray": "2,-3", "largest_zero_sum": "1,-1",
                   "longest_consecutive": "3,1,2", "majority_n3": "1,1,2", "repeating_missing": "1,1",
                   "three_sum": "-1,0,1", "set_matrix_zeros": "1,0/1,1", "rotate_matrix": "1,2/3,4",
                   "spiral_order": "1,2/3,4", "merge_no_space": "1,4 | 2,3",
                   "count_inversions": "3,1,2", "reverse_pairs": "5,1", "count_digits": "123",
                   "reverse_number": "123", "palindrome_number": "121", "armstrong_number": "153",
                   "print_divisors": "12", "check_prime": "7", "factorial": "5", "sum_first_n": "10",
                   "reverse_array": "1,2,3", "palindrome_string": "abba",
                   "frequency_count": "1,1,2", "check_odd": "3", "swap_xor": "1, 2",
                   "divide_bits": "7, 2", "xor_range": "3, 9", "single_number_iii": "1,2,1,3"}
        with_target = {"partition_array_max_sum": ("1,15,7", 2), "count_partitions_diff": ("5,2,6,4", 3),
                       "target_sum": ("1,1,1", 1), "linear_search": ("4,7", 7),
                       "longest_sum_k_any": ("1,2", 3), "count_sum_k": ("1,2", 3),
                       "count_xor_k": ("4,2", 6), "four_sum": ("1,0,-1,0", 0),
                       "pascal_triangle": ("rows", 4), "check_ith_bit": ("13", 2)}
        every = set(D.TITLES) | set(A.TITLES) | set(B.TITLES)
        assert set(samples) | set(with_target) == every
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["meta"]["view"] == "grid"
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        for algo in every:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "cut_stick", "text": "5 | 5"},
                  {"algorithm": "boolean_evaluation", "text": "T&"},
                  {"algorithm": "rotate_matrix", "text": "1,2,3/4,5,6"},
                  {"algorithm": "union_sorted", "text": "3,1 | 2"},
                  {"algorithm": "missing_number", "text": "0,0,1"},
                  {"algorithm": "repeating_missing", "text": "1,2,3"},
                  {"algorithm": "rearrange_by_sign", "text": "1,2,-1"},
                  {"algorithm": "linear_search", "text": "1,2"},
                  {"algorithm": "pascal_triangle", "text": "x", "target": 9},
                  {"algorithm": "check_prime", "text": "10000"},
                  {"algorithm": "divide_bits", "text": "7, 0"},
                  {"algorithm": "check_ith_bit", "text": "5", "target": 8},
                  {"algorithm": "single_number_iii", "text": "1,1,2"},
                  {"algorithm": "xor_range", "text": "9, 3"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
