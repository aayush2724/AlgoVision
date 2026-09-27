"""Harder binary searches (Step 4) on the `grid` view.

* search_rotated_ii — rotated with duplicates: when a[lo] = a[mid] = a[hi]
  we can't tell which half is sorted, so shrink both ends by one.
* median_two_sorted / kth_two_sorted — binary-search how many elements the
  left part takes from A; the rest come from B. A cut is right when
  maxLeft(A) ≤ minRight(B) and maxLeft(B) ≤ minRight(A).
* gas_station — binary search on the answer d (a real number): stations
  needed for a gap g is ceil(g / d) − 1; find the smallest d that fits k.
* peak_element_ii — binary search on columns: take the column's maximum;
  if a neighbour to one side is bigger, a peak lies on that side.
* matrix_median — binary search on the value: count cells ≤ x (upper bound
  in every sorted row) until that count passes half.
"""

import math

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "search_rotated_ii": "Search in Rotated Sorted Array II (duplicates)",
    "median_two_sorted": "Median of Two Sorted Arrays",
    "kth_two_sorted": "K-th Element of Two Sorted Arrays",
    "gas_station": "Minimise Max Distance to Gas Station",
    "peak_element_ii": "Find a Peak Element II (matrix)",
    "matrix_median": "Median of a Row-Wise Sorted Matrix",
}
INF = float("inf")


def _nums(text, n=10):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if len(a) > n or any(abs(v) > 999 for v in a):
        raise ValueError(f"At most {n} numbers within ±999.")
    return a


def _two(text):
    if "|" not in (text or ""):
        raise ValueError("Give two sorted arrays separated by '|', e.g. 1,3,8 | 7,9,10,11.")
    a, b = (_nums(p, 8) for p in text.split("|", 1))
    if a != sorted(a) or b != sorted(b) or not (a or b):
        raise ValueError("Both arrays must be sorted, and not both empty.")
    return a, b


def run(algo, text, target=None):
    if algo in ("median_two_sorted", "kth_two_sorted"):
        a, b = _two(text)
        if algo == "median_two_sorted":
            return _median(a, b)
        if target is None or target != int(target) or not (1 <= target <= len(a) + len(b)):
            raise ValueError(f"k must be 1–{len(a) + len(b)}.")
        return _kth(a, b, int(target))
    if algo in ("peak_element_ii", "matrix_median"):
        g = parse_matrix(text, max_side=6)
        if algo == "peak_element_ii":
            R, C = len(g), len(g[0])
            if any(g[r][c] == g[r][c + 1] for r in range(R) for c in range(C - 1)) or \
                    any(g[r][c] == g[r + 1][c] for r in range(R - 1) for c in range(C)):
                raise ValueError("Neighbouring cells must differ.")
            return _peak(g)
        if any(row != sorted(row) for row in g) or len(g) * len(g[0]) % 2 == 0:
            raise ValueError("Every row sorted, and an odd number of cells.")
        return _matrix_median(g)
    if algo == "gas_station":
        a = _nums(text, 10)
        if len(a) < 2 or a != sorted(a) or len(set(a)) != len(a) or a[0] < 0:
            raise ValueError("Give 2–10 increasing, non-negative station positions.")
        if target is None or target != int(target) or not (1 <= target <= 20):
            raise ValueError("k (new stations) must be 1–20.")
        return _gas(a, int(target))
    a = _nums(text, 12)
    if not a:
        raise ValueError("Give 1–12 numbers.")
    if target is None or target != int(target):
        raise ValueError("Give a whole-number target.")
    return _rotated(a, int(target))


def _rotated(a, t):
    G = Grid(1, len(a))
    G.grid[0] = list(a)
    G.counts = {"probes": 0, "shrinks": 0}
    lo, hi = 0, len(a) - 1
    win = lambda: [(0, j) for j in range(lo, hi + 1)]
    G.add(f"Search {t}. One half of [lo, hi] is always sorted — unless a[lo] = "
          f"a[mid] = a[hi], when duplicates hide which one.", deps=win())
    while lo <= hi:
        mid = (lo + hi) // 2
        G.counts["probes"] += 1
        if a[mid] == t:
            G.add(f"a[{mid}] = {t} — found.", 0, mid, win(), [(0, mid)])
            return G.result("search_rotated_ii", True)
        if a[lo] == a[mid] == a[hi]:
            G.add(f"a[lo] = a[mid] = a[hi] = {a[mid]}: can't tell which half is "
                  f"sorted. Drop both ends.", 0, mid, win(), match=False)
            lo, hi = lo + 1, hi - 1
            G.counts["shrinks"] += 1
            continue
        if a[lo] <= a[mid]:
            inside = a[lo] <= t < a[mid]
            G.add(f"Left half {a[lo]}..{a[mid]} is sorted; {t} is "
                  f"{'inside — go left' if inside else 'not in it — go right'}.",
                  0, mid, win(), match=False)
            if inside:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            inside = a[mid] < t <= a[hi]
            G.add(f"Right half {a[mid]}..{a[hi]} is sorted; {t} is "
                  f"{'inside — go right' if inside else 'not in it — go left'}.",
                  0, mid, win(), match=False)
            if inside:
                lo = mid + 1
            else:
                hi = mid - 1
    G.add(f"The range is empty — {t} is not present.", match=False)
    return G.result("search_rotated_ii", False)


def _two_grid(a, b):
    w = max(len(a), len(b), 1)
    G = Grid(2, w)
    G.grid[0] = a + [None] * (w - len(a))
    G.grid[1] = b + [None] * (w - len(b))
    return G


def _f(v):
    return "−∞" if v == -INF else "+∞" if v == INF else v


def _partition(a, b, need, G):
    """Binary-search how many of the `need` left-part elements come from a
    (the shorter array); returns the four values around the cut."""
    lo, hi = max(0, need - len(b)), min(need, len(a))
    while True:
        ca = (lo + hi) // 2
        cb = need - ca
        l1 = a[ca - 1] if ca else -INF
        l2 = b[cb - 1] if cb else -INF
        r1 = a[ca] if ca < len(a) else INF
        r2 = b[cb] if cb < len(b) else INF
        G.counts["cuts"] += 1
        left = [(0, j) for j in range(ca)] + [(1, j) for j in range(cb)]
        if l1 <= r2 and l2 <= r1:
            G.add(f"Take {ca} from A and {cb} from B: {_f(l1)} ≤ {_f(r2)} and "
                  f"{_f(l2)} ≤ {_f(r1)} — every left value ≤ every right value. "
                  f"This is the cut.", None, None, left, left)
            return l1, l2, r1, r2
        if l1 > r2:
            G.add(f"Take {ca} from A and {cb} from B: A's left end {_f(l1)} > B's "
                  f"right start {_f(r2)} — too many from A.", None, None, left,
                  match=False)
            hi = ca - 1
        else:
            G.add(f"Take {ca} from A and {cb} from B: B's left end {_f(l2)} > A's "
                  f"right start {_f(r1)} — too few from A.", None, None, left,
                  match=False)
            lo = ca + 1


def _median(a, b):
    swap = len(a) > len(b)
    if swap:
        a, b = b, a
    G = _two_grid(a, b)
    G.counts = {"cuts": 0}
    n = len(a) + len(b)
    need = (n + 1) // 2
    G.add(f"{n} values in total: the left half holds {need}. Binary-search how "
          f"many come from the shorter array{' (swapped into row A)' if swap else ''}.")
    l1, l2, r1, r2 = _partition(a, b, need, G)
    if n % 2:
        med = max(l1, l2)
        G.add(f"Odd total — the median is the largest left value, {med}.")
    else:
        med = (max(l1, l2) + min(r1, r2)) / 2
        G.add(f"Even total — median = (max left {max(l1, l2)} + min right "
              f"{min(r1, r2)}) / 2 = {med:g}.")
    return G.result("median_two_sorted", med, ["A", "B"])


def _kth(a, b, k):
    swap = len(a) > len(b)
    if swap:
        a, b = b, a
    G = _two_grid(a, b)
    G.counts = {"cuts": 0}
    G.add(f"The {k}-th smallest is the largest value of a left part holding {k} "
          f"elements. Binary-search how many come from the shorter array.")
    l1, l2, _, _ = _partition(a, b, k, G)
    res = max(l1, l2)
    G.add(f"The {k}-th element is max({_f(l1)}, {_f(l2)}) = {res}.")
    return G.result("kth_two_sorted", res, ["A", "B"])


def _gas(a, k):
    gaps = [a[i + 1] - a[i] for i in range(len(a) - 1)]
    G = Grid(3, len(a))
    G.grid[0] = list(a)
    G.grid[1] = gaps + [None]
    G.counts = {"iterations": 0}
    need = lambda d: sum(math.ceil(g / d) - 1 for g in gaps)
    lo, hi = 0.0, float(max(gaps))
    G.add(f"The answer d is a real number between 0 and the largest gap {hi:g}. "
          f"For a guess d, gap g needs ceil(g/d) − 1 new stations. Smaller d "
          f"needs more stations — binary-search the smallest d that needs ≤ {k}.")
    while hi - lo > 1e-6:
        mid = (lo + hi) / 2
        cnt = need(mid)
        G.counts["iterations"] += 1
        if G.counts["iterations"] <= 14:
            G.grid[2] = [math.ceil(g / mid) - 1 for g in gaps] + [None]
            G.add(f"d = {mid:.4f}: needs {cnt} station(s) — "
                  f"{'fits, try smaller' if cnt <= k else 'too many, go bigger'}.",
                  2, None, [(2, j) for j in range(len(gaps))], match=cnt <= k)
        if cnt <= k:
            hi = mid
        else:
            lo = mid
    res = round(hi, 4)
    G.grid[2] = [math.ceil(g / hi) - 1 for g in gaps] + [None]
    G.add(f"… repeat until the range is tiny. Smallest max distance ≈ {res}.",
          path=[(2, j) for j in range(len(gaps))])
    return G.result("gas_station", res, ["position", "gap", "added"])


def _peak(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [row[:] for row in g]
    G.counts = {"columns_checked": 0}
    lo, hi = 0, C - 1
    G.add("Binary-search the columns. In the middle column take the maximum: it "
          "beats its upper and lower neighbours. If the left or right neighbour "
          "is bigger, climb that way — a peak must exist on that side.")
    while lo <= hi:
        mid = (lo + hi) // 2
        r = max(range(R), key=lambda i: g[i][mid])
        G.counts["columns_checked"] += 1
        left = g[r][mid - 1] if mid else -INF
        right = g[r][mid + 1] if mid + 1 < C else -INF
        col = [(i, mid) for i in range(R)]
        if g[r][mid] > left and g[r][mid] > right:
            G.add(f"Column {mid}: max {g[r][mid]} at row {r}, bigger than both side "
                  f"neighbours — a peak.", r, mid, col, [(r, mid)])
            return G.result("peak_element_ii", [r, mid])
        if left > g[r][mid]:
            G.add(f"Column {mid}: max {g[r][mid]} at row {r}, but the left "
                  f"neighbour {left} is bigger — search the left columns.", r, mid,
                  col, match=False)
            hi = mid - 1
        else:
            G.add(f"Column {mid}: max {g[r][mid]} at row {r}, but the right "
                  f"neighbour {right} is bigger — search the right columns.", r, mid,
                  col, match=False)
            lo = mid + 1
    return G.result("peak_element_ii", None)


def _matrix_median(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [row[:] for row in g]
    G.counts = {"guesses": 0}
    half = R * C // 2
    lo, hi = min(r[0] for r in g), max(r[-1] for r in g)
    G.add(f"{R * C} cells, so the median has {half} values below it. Binary-search "
          f"the VALUE between {lo} and {hi}: count cells ≤ x with an upper bound in "
          f"each sorted row.")
    while lo < hi:
        mid = (lo + hi) // 2
        small = [(r, c) for r in range(R) for c in range(C) if g[r][c] <= mid]
        G.counts["guesses"] += 1
        if len(small) <= half:
            G.add(f"x = {mid}: {len(small)} cell(s) ≤ x — not more than {half}, so "
                  f"the median is bigger.", deps=small, match=False)
            lo = mid + 1
        else:
            G.add(f"x = {mid}: {len(small)} cell(s) ≤ x — more than {half}, so the "
                  f"median is at most {mid}.", deps=small)
            hi = mid
    G.add(f"The range closed at {lo}: the median.",
          path=[(r, c) for r in range(R) for c in range(C) if g[r][c] == lo])
    return G.result("matrix_median", lo)
