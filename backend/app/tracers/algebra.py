"""Speed-up tricks (batch 78) on the `grid` view.

* matrix_exponentiation — [[F(n+1), F(n)], [F(n), F(n−1)]] = [[1,1],[1,0]]^n;
  square-and-multiply gives F(n) in O(log n) 2×2 multiplications.
* ternary_search — on a unimodal array (strictly up, then strictly down)
  probe m1 < m2: if a[m1] < a[m2] the peak is right of m1, else left of m2.
  Each round keeps two thirds of the range.
* meet_in_middle — count subsets with sum ≤ S: 2^n is too many, so list the
  2^(n/2) sums of each half, sort one list, and for every sum x of the other
  half binary-search how many partners stay ≤ S − x.
"""

from bisect import bisect_right

from app.tracers.grid_common import Grid

TITLES = {
    "matrix_exponentiation": "Matrix Exponentiation (Fibonacci)",
    "ternary_search": "Ternary Search (Peak of a Unimodal Array)",
    "meet_in_middle": "Meet in the Middle (Subset Sums ≤ S)",
}


def _nums(text, n):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(abs(v) > 99 for v in a):
        raise ValueError(f"Give 1–{n} numbers within ±99.")
    return a


def run(algo, text, target=None):
    if algo == "matrix_exponentiation":
        try:
            n = int((text or "").strip())
        except ValueError:
            raise ValueError("Give n (0–90).") from None
        if not (0 <= n <= 90):
            raise ValueError("Give n (0–90).")
        return _matpow(n)
    if algo == "ternary_search":
        a = _nums(text, 12)
        p = a.index(max(a))
        if any(a[i] >= a[i + 1] for i in range(p)) or \
                any(a[i] <= a[i + 1] for i in range(p, len(a) - 1)):
            raise ValueError("The array must rise strictly, then fall strictly.")
        return _ternary(a)
    a = _nums(text, 8)
    if target is None or target != int(target) or abs(target) > 999:
        raise ValueError("Give the limit S (a whole number).")
    return _mitm(a, int(target))


def _mul(x, y):
    return [[x[0][0] * y[0][0] + x[0][1] * y[1][0], x[0][0] * y[0][1] + x[0][1] * y[1][1]],
            [x[1][0] * y[0][0] + x[1][1] * y[1][0], x[1][0] * y[0][1] + x[1][1] * y[1][1]]]


def _flat(m):
    return [m[0][0], m[0][1], m[1][0], m[1][1]]


def _matpow(n):
    G = Grid(2, 5)
    G.counts = {"matrix_mults": 0}
    base, res, e = [[1, 1], [1, 0]], [[1, 0], [0, 1]], n
    G.grid = [_flat(base) + [e], _flat(res) + [None]]
    G.add(f"Q = [[1,1],[1,0]] and Qⁿ = [[F(n+1), F(n)], [F(n), F(n−1)]]. Compute "
          f"Q^{n} by square-and-multiply: look at the exponent's bits from the "
          f"lowest.", 0, 4)
    while e:
        bit = e & 1
        if bit:
            res = _mul(res, base)
            G.counts["matrix_mults"] += 1
        base = _mul(base, base)
        G.counts["matrix_mults"] += 1
        e >>= 1
        G.grid = [_flat(base) + [e], _flat(res) + [None]]
        G.add(f"Bit {bit}: " + ("multiply the result by the current power; " if bit
                                else "") + f"square the power. Exponent left {e}.",
              1 if bit else 0, None, [], [(1, c) for c in range(4)] if bit else [])
    fib = res[0][1]
    G.add(f"F({n}) = the top-right entry = {fib}, using "
          f"{G.counts['matrix_mults']} 2×2 multiplications instead of {n} additions.",
          1, 1, path=[(1, 1)])
    return G.result("matrix_exponentiation", fib, ["power", "result"],
                    ["a", "b", "c", "d", "exp"])


def _ternary(a):
    G = Grid(1, len(a))
    G.grid[0] = list(a)
    G.counts = {"probes": 0}
    lo, hi = 0, len(a) - 1
    win = lambda: [(0, j) for j in range(lo, hi + 1)]
    G.add("The values rise, then fall. Probe two points m1 < m2 that split "
          "[lo, hi] into thirds: the smaller probe can't be on the peak's side "
          "that we drop.", None, None, win())
    while hi - lo > 2:
        m1 = lo + (hi - lo) // 3
        m2 = hi - (hi - lo) // 3
        G.counts["probes"] += 2
        if a[m1] < a[m2]:
            G.add(f"a[{m1}] = {a[m1]} < a[{m2}] = {a[m2]}: still climbing at m1 — "
                  f"the peak is right of {m1}.", 0, m1, win(), [(0, m2)], match=False)
            lo = m1 + 1
        else:
            G.add(f"a[{m1}] = {a[m1]} ≥ a[{m2}] = {a[m2]}: already falling at m2 — "
                  f"the peak is left of {m2}.", 0, m2, win(), [(0, m1)], match=False)
            hi = m2 - 1
    p = max(range(lo, hi + 1), key=lambda i: a[i])
    G.add(f"At most three cells left — scan them: the peak is a[{p}] = {a[p]}.",
          0, p, win(), [(0, p)])
    return G.result("ternary_search", a[p], None, None, index=p)


def _sums(part):
    return [sum(part[i] for i in range(len(part)) if m >> i & 1)
            for m in range(1 << len(part))]


def _mitm(a, s):
    h = len(a) // 2
    left, right = a[:h], a[h:]
    ls, rs = _sums(left), sorted(_sums(right))
    w = max(len(ls), len(rs))
    G = Grid(2, w)
    G.grid = [ls + [None] * (w - len(ls)), rs + [None] * (w - len(rs))]
    G.counts = {"binary_searches": 0, "count": 0}
    G.add(f"Split {a} into {left} and {right}. Row 0: all {len(ls)} subset sums of "
          f"the left half. Row 1: all {len(rs)} of the right half, SORTED. That's "
          f"{len(ls) + len(rs)} sums instead of {1 << len(a)} subsets.")
    for i, x in enumerate(ls):
        k = bisect_right(rs, s - x)
        G.counts["binary_searches"] += 1
        G.counts["count"] += k
        G.add(f"Left sum {x}: partners must be ≤ {s} − {x} = {s - x}; binary search "
              f"finds {k} of them. Running count {G.counts['count']}.", 0, i,
              [(1, j) for j in range(k)])
    G.add(f"{G.counts['count']} subset(s) of {a} have sum ≤ {s}.")
    return G.result("meet_in_middle", G.counts["count"], ["left sums", "right sums"])
