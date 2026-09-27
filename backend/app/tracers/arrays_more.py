"""Array problems (Step 3) on the `grid` view — row 0 is the array; extra rows
show what the scan keeps (prefix sums, counts, merged output …).

Scans (batch 56): largest_element, check_sorted, linear_search,
union_sorted / intersection_sorted (two pointers), missing_number (XOR),
max_consecutive_ones, rearrange_by_sign, max_product_subarray (track the
max AND min product — a negative flips them).

Hashing / prefix (batch 57): longest_sum_k_any & count_sum_k & largest_zero_sum
(prefix-sum map), count_xor_k (prefix-XOR map), longest_consecutive (set:
only start counting at a run's first value), majority_n3 (two-candidate
Boyer-Moore + verify), repeating_missing (sum and sum-of-squares),
three_sum / four_sum (sort + two pointers, skipping duplicates).

Matrix & merge (batch 58): set_matrix_zeros (mark rows/cols, then clear),
rotate_matrix (transpose, then reverse each row), spiral_order (shrinking
bounds), pascal_triangle, merge_no_space (gap method), count_inversions and
reverse_pairs (count during merge sort).
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "largest_element": "Largest Element in an Array",
    "check_sorted": "Check if an Array is Sorted",
    "linear_search": "Linear Search",
    "union_sorted": "Union of Two Sorted Arrays",
    "intersection_sorted": "Intersection of Two Sorted Arrays",
    "missing_number": "Find the Missing Number",
    "max_consecutive_ones": "Maximum Consecutive Ones",
    "rearrange_by_sign": "Rearrange Array Elements by Sign",
    "max_product_subarray": "Maximum Product Subarray",
    "longest_sum_k_any": "Longest Subarray With Sum K (any sign)",
    "count_sum_k": "Count Subarrays With Sum K",
    "largest_zero_sum": "Largest Subarray With Sum 0",
    "count_xor_k": "Count Subarrays With XOR K",
    "longest_consecutive": "Longest Consecutive Sequence",
    "majority_n3": "Majority Elements (> n/3)",
    "repeating_missing": "Find the Repeating and Missing Numbers",
    "three_sum": "3 Sum",
    "four_sum": "4 Sum",
    "set_matrix_zeros": "Set Matrix Zeros",
    "rotate_matrix": "Rotate a Matrix by 90°",
    "spiral_order": "Spiral Traversal of a Matrix",
    "pascal_triangle": "Pascal's Triangle",
    "merge_no_space": "Merge Two Sorted Arrays Without Extra Space",
    "count_inversions": "Count Inversions",
    "reverse_pairs": "Reverse Pairs",
}
NEEDS_T = {"linear_search", "longest_sum_k_any", "count_sum_k", "count_xor_k", "four_sum"}
MATRIX = {"set_matrix_zeros", "rotate_matrix", "spiral_order"}
TWO = {"union_sorted", "intersection_sorted", "merge_no_space"}


def _nums(text, n=12):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(abs(v) > 999 for v in a):
        raise ValueError(f"Give 1–{n} whole numbers within ±999.")
    return a


def run(algo, text, target=None):
    if algo in MATRIX:
        g = parse_matrix(text, max_side=6)
        if algo == "rotate_matrix" and len(g) != len(g[0]):
            raise ValueError("Rotation needs a square matrix.")
        return {"set_matrix_zeros": _zeros, "rotate_matrix": _rotate,
                "spiral_order": _spiral}[algo](g)
    if algo == "pascal_triangle":
        if target is None or target != int(target) or not (1 <= target <= 8):
            raise ValueError("Give the number of rows (1–8).")
        return _pascal(int(target))
    if algo in TWO:
        if "|" not in (text or ""):
            raise ValueError("Give two arrays separated by '|', e.g. 1,3,5 | 2,3,4.")
        a, b = (_nums(p, 8) for p in text.split("|", 1))
        if a != sorted(a) or b != sorted(b):
            raise ValueError("Both arrays must be sorted.")
        return {"union_sorted": _union, "intersection_sorted": _inter,
                "merge_no_space": _gap}[algo](a, b)
    a = _nums(text)
    if algo in NEEDS_T and (target is None or target != int(target) or abs(target) > 9999):
        raise ValueError("Give a whole-number target within ±9999.")
    if algo == "missing_number" and (len(set(a)) != len(a) or
                                     any(not (0 <= v <= len(a)) for v in a)):
        raise ValueError(f"Give distinct numbers from 0..{len(a)} with one missing.")
    if algo == "repeating_missing" and (any(not (1 <= v <= len(a)) for v in a)
                                        or len(set(a)) != len(a) - 1):
        raise ValueError(f"Give 1..{len(a)} with exactly one value repeated (and one missing).")
    if algo == "rearrange_by_sign" and (0 in a or
                                        sum(v > 0 for v in a) != sum(v < 0 for v in a)):
        raise ValueError("Give equally many positive and negative non-zero numbers.")
    fn = globals()["_" + algo]
    return fn(a, int(target)) if algo in NEEDS_T else fn(a)


def _row(a, rows=1, labels=None):
    G = Grid(rows, len(a))
    G.grid[0] = list(a)
    G.labels = labels
    return G


def _done(G, algo, res):
    return G.result(algo, res, G.labels)


# ── scans ──────────────────────────────────────────────────────────────
def _largest_element(a):
    G = _row(a)
    G.counts = {"comparisons": 0}
    best = 0
    G.add("One pass, keeping the biggest value seen.", 0, 0, path=[(0, 0)])
    for i in range(1, len(a)):
        G.counts["comparisons"] += 1
        if a[i] > a[best]:
            best = i
        G.add(f"{a[i]} vs best {a[best]}.", 0, i, path=[(0, best)])
    G.add(f"Largest: {a[best]}.", path=[(0, best)])
    return _done(G, "largest_element", a[best])


def _check_sorted(a):
    G = _row(a)
    G.counts = {"comparisons": 0}
    G.add("Sorted means no element is smaller than the one before it.")
    for i in range(1, len(a)):
        G.counts["comparisons"] += 1
        if a[i] < a[i - 1]:
            G.add(f"{a[i]} < {a[i - 1]} — not sorted.", 0, i, [(0, i - 1)], match=False)
            return _done(G, "check_sorted", False)
        G.add(f"{a[i - 1]} ≤ {a[i]}.", 0, i, path=[(0, j) for j in range(i + 1)])
    G.add("Every neighbour pair is in order — sorted.",
          path=[(0, j) for j in range(len(a))])
    return _done(G, "check_sorted", True)


def _linear_search(a, x):
    G = _row(a)
    G.counts = {"checks": 0}
    G.add(f"Check each position in turn for {x}.")
    for i, v in enumerate(a):
        G.counts["checks"] += 1
        if v == x:
            G.add(f"Position {i} holds {x} — found.", 0, i, path=[(0, i)])
            return _done(G, "linear_search", i)
        G.add(f"Position {i} holds {v}.", 0, i, match=False)
    G.add(f"{x} is not in the array (−1).", match=False)
    return _done(G, "linear_search", -1)


def _two_rows(a, b):
    w = len(a) + len(b)
    G = Grid(3, w)
    G.grid[0] = a + [None] * (w - len(a))
    G.grid[1] = b + [None] * (w - len(b))
    G.labels = ["A", "B", "out"]
    return G


def _union(a, b):
    G = _two_rows(a, b)
    G.counts = {"steps": 0}
    i = j = 0
    out = []
    G.add("Two pointers walk both sorted arrays; take the smaller, skipping "
          "anything equal to the last value written.")
    while i < len(a) or j < len(b):
        if j >= len(b) or (i < len(a) and a[i] <= b[j]):
            v, src = a[i], (0, i)
            i += 1
        else:
            v, src = b[j], (1, j)
            j += 1
        G.counts["steps"] += 1
        if not out or out[-1] != v:
            out.append(v)
            G.grid[2][len(out) - 1] = v
            G.add(f"Take {v}.", 2, len(out) - 1, [src])
        else:
            G.add(f"{v} is already the last value written — skip.", src[0], src[1],
                  match=False)
    G.add(f"Union: {out}.", path=[(2, k) for k in range(len(out))])
    return _done(G, "union_sorted", out)


def _inter(a, b):
    G = _two_rows(a, b)
    G.counts = {"steps": 0}
    i = j = 0
    out = []
    G.add("Two pointers: advance the smaller side; equal values are common.")
    while i < len(a) and j < len(b):
        G.counts["steps"] += 1
        if a[i] == b[j]:
            out.append(a[i])
            G.grid[2][len(out) - 1] = a[i]
            G.add(f"Both have {a[i]} — keep it.", 2, len(out) - 1, [(0, i), (1, j)])
            i += 1
            j += 1
        elif a[i] < b[j]:
            G.add(f"{a[i]} < {b[j]} — advance A.", 0, i, [(1, j)], match=False)
            i += 1
        else:
            G.add(f"{b[j]} < {a[i]} — advance B.", 1, j, [(0, i)], match=False)
            j += 1
    G.add(f"Intersection: {out}.", path=[(2, k) for k in range(len(out))])
    return _done(G, "intersection_sorted", out)


def _missing_number(a):
    G = _row(a)
    G.counts = {"xors": 0}
    x = 0
    G.add(f"XOR every index 1..{len(a)} and every value: pairs cancel, the "
          f"missing number survives.")
    for i, v in enumerate(a):
        x ^= (i + 1) ^ v
        G.counts["xors"] += 1
        G.add(f"XOR in index {i + 1} and value {v} → {x}.", 0, i)
    G.add(f"Missing number: {x}.")
    return _done(G, "missing_number", x)


def _max_consecutive_ones(a):
    G = _row(a)
    G.counts = {"resets": 0}
    run = best = start = bs = 0
    G.add("Count the current run of 1s; any other value resets it.")
    for i, v in enumerate(a):
        if v == 1:
            run += 1
            if run == 1:
                start = i
            if run > best:
                best, bs = run, start
        else:
            run = 0
            G.counts["resets"] += 1
        G.add(f"Run {run}, best {best}.", 0, i,
              [(0, j) for j in range(i - run + 1, i + 1)] if run else [],
              [(0, j) for j in range(bs, bs + best)])
    G.add(f"Longest run of 1s: {best}.", path=[(0, j) for j in range(bs, bs + best)])
    return _done(G, "max_consecutive_ones", best)


def _rearrange_by_sign(a):
    G = _row(a, 2, ["input", "output"])
    G.counts = {"placed": 0}
    out = [None] * len(a)
    pos, neg = 0, 1
    G.add("Positives go to even slots, negatives to odd slots, keeping order.")
    for i, v in enumerate(a):
        k = pos if v > 0 else neg
        out[k] = v
        G.grid[1][k] = v
        if v > 0:
            pos += 2
        else:
            neg += 2
        G.counts["placed"] += 1
        G.add(f"{v} → slot {k}.", 1, k, [(0, i)])
    G.add(f"Result: {out}.", path=[(1, k) for k in range(len(a))])
    return _done(G, "rearrange_by_sign", out)


def _max_product_subarray(a):
    G = _row(a, 3, ["value", "max here", "min here"])
    G.counts = {"swaps": 0}
    hi = lo = best = a[0]
    G.grid[1][0] = G.grid[2][0] = a[0]
    G.add("Track the largest AND smallest product ending here: a negative "
          "number turns the smallest into the largest.", 1, 0)
    for i in range(1, len(a)):
        v = a[i]
        if v < 0:
            hi, lo = lo, hi
            G.counts["swaps"] += 1
        hi, lo = max(v, hi * v), min(v, lo * v)
        best = max(best, hi)
        G.grid[1][i], G.grid[2][i] = hi, lo
        G.add(f"{v}{' (negative: swap max/min)' if v < 0 else ''}: max {hi}, min "
              f"{lo}. Best {best}.", 1, i, [(1, i - 1), (2, i - 1)])
    G.add(f"Maximum product: {best}.")
    return _done(G, "max_product_subarray", best)


# ── hashing / prefix sums ──────────────────────────────────────────────
def _prefix_scan(a, k, counting, op):
    G = _row(a, 2, ["value", "prefix"])
    G.counts = {"lookups": 0}
    first, count, pre = {0: -1}, {0: 1}, 0
    best, span, total = 0, None, 0
    what = "XOR" if op == "xor" else "sum"
    G.add(f"Running prefix {what}. A subarray ending here has {what} {k} "
          f"exactly when an earlier prefix equals prefix "
          f"{'⊕' if op == 'xor' else '−'} {k}.")
    for i, v in enumerate(a):
        pre = pre ^ v if op == "xor" else pre + v
        G.grid[1][i] = pre
        need = pre ^ k if op == "xor" else pre - k
        G.counts["lookups"] += 1
        hits = count.get(need, 0)
        total += hits
        if need in first and i - first[need] > best:
            best, span = i - first[need], (first[need] + 1, i)
        first.setdefault(pre, i)
        count[pre] = count.get(pre, 0) + 1
        G.add(f"Prefix {pre}; earlier prefixes equal to {need}: {hits}. "
              + (f"Count {total}." if counting else f"Longest so far {best}."),
              1, i, path=[(0, j) for j in range(span[0], span[1] + 1)] if span else [])
    return G, best, span, total


def _span(span):
    return [(0, j) for j in range(span[0], span[1] + 1)] if span else []


def _longest_sum_k_any(a, k):
    G, best, span, _ = _prefix_scan(a, k, False, "sum")
    G.add(f"Longest subarray with sum {k}: {best}.", path=_span(span))
    return _done(G, "longest_sum_k_any", best)


def _count_sum_k(a, k):
    G, _, _, total = _prefix_scan(a, k, True, "sum")
    G.add(f"{total} subarray(s) sum to {k}.")
    return _done(G, "count_sum_k", total)


def _largest_zero_sum(a):
    G, best, span, _ = _prefix_scan(a, 0, False, "sum")
    G.add(f"Largest subarray with sum 0: {best}.", path=_span(span))
    return _done(G, "largest_zero_sum", best)


def _count_xor_k(a, k):
    G, _, _, total = _prefix_scan(a, k, True, "xor")
    G.add(f"{total} subarray(s) have XOR {k}.")
    return _done(G, "count_xor_k", total)


def _longest_consecutive(a):
    G = _row(a)
    G.counts = {"starts": 0}
    s = set(a)
    best, run_vals = 0, []
    G.add("Put everything in a set. Only start counting at a value whose "
          "predecessor is missing — the start of a run — so each run is walked once.")
    for i, v in enumerate(a):
        if v - 1 in s:
            G.add(f"{v}: {v - 1} exists, so {v} isn't a run start.", 0, i, match=False)
            continue
        G.counts["starts"] += 1
        x = v
        while x + 1 in s:
            x += 1
        ln = x - v + 1
        if ln > best:
            best, run_vals = ln, list(range(v, x + 1))
        G.add(f"{v} starts a run {v}..{x} (length {ln}). Best {best}.", 0, i,
              [(0, j) for j, w in enumerate(a) if v <= w <= x])
    G.add(f"Longest consecutive sequence: {best}.",
          path=[(0, j) for j, w in enumerate(a) if w in run_vals])
    return _done(G, "longest_consecutive", best)


def _majority_n3(a):
    G = _row(a)
    G.counts = {"votes": 0}
    c1 = c2 = None
    n1 = n2 = 0
    G.add("At most two values can appear more than n/3 times. Keep two "
          "candidates with counts; a third value cancels one vote from each.")
    for i, v in enumerate(a):
        G.counts["votes"] += 1
        if v == c1:
            n1 += 1
        elif v == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = v, 1
        elif n2 == 0:
            c2, n2 = v, 1
        else:
            n1 -= 1
            n2 -= 1
        G.add(f"{v}: candidates {c1}×{n1}, {c2}×{n2}.", 0, i)
    res = sorted(c for c in {c1, c2} if c is not None and a.count(c) > len(a) // 3)
    G.add(f"Verify by counting: {res or 'none'} appear(s) more than "
          f"{len(a)}/3 times.", path=[(0, j) for j, v in enumerate(a) if v in res])
    return _done(G, "majority_n3", res)


def _repeating_missing(a):
    G = _row(a)
    n = len(a)
    s = sum(a) - n * (n + 1) // 2                      # r − m
    q = sum(v * v for v in a) - n * (n + 1) * (2 * n + 1) // 6   # r² − m²
    rp = (q // s + s) // 2
    ms = rp - s
    G.counts = {"passes": 1}
    G.add(f"Compare with 1..{n}: the sums differ by r − m = {s}, the sums of "
          f"squares by r² − m² = {q}. So r + m = {q // s}, giving r = {rp} and "
          f"m = {ms}.", path=[(0, j) for j, v in enumerate(a) if v == rp])
    return _done(G, "repeating_missing", [rp, ms])


def _k_sum(a, target, k, algo):
    s = sorted(a)
    G = _row(s)
    G.counts = {"checks": 0}
    out = []
    G.add(f"Sort, fix the first {k - 2} value(s), then two pointers close in on "
          f"the rest. Skip equal neighbours so no answer repeats.")

    def two(lo, hi, need, fixed):
        l, r = lo, hi
        while l < r:
            G.counts["checks"] += 1
            t = s[l] + s[r]
            cells = [(0, f) for f in fixed] + [(0, l), (0, r)]
            combo = [s[f] for f in fixed] + [s[l], s[r]]
            if t == need:
                out.append(combo)
                G.add(f"{combo} sums to {target} — record it.", 0, r, cells, cells)
                l += 1
                while l < r and s[l] == s[l - 1]:
                    l += 1
            elif t < need:
                G.add(f"{combo} is too small — move the left pointer up.", 0, l,
                      cells, match=False)
                l += 1
            else:
                G.add(f"{combo} is too big — move the right pointer down.", 0, r,
                      cells, match=False)
                r -= 1

    n = len(s)
    for i in range(n):
        if i and s[i] == s[i - 1]:
            continue
        if k == 3:
            two(i + 1, n - 1, target - s[i], [i])
        else:
            for j in range(i + 1, n):
                if j > i + 1 and s[j] == s[j - 1]:
                    continue
                two(j + 1, n - 1, target - s[i] - s[j], [i, j])
    G.add(f"{len(out)} unique {'quadruplet' if k == 4 else 'triplet'}(s).")
    return _done(G, algo, out)


def _three_sum(a):
    return _k_sum(a, 0, 3, "three_sum")


def _four_sum(a, target):
    return _k_sum(a, target, 4, "four_sum")


# ── matrix & merge ─────────────────────────────────────────────────────
def _zeros(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [r[:] for r in g]
    G.counts = {"zeros": sum(v == 0 for r in g for v in r)}
    rows = {r for r in range(R) for c in range(C) if g[r][c] == 0}
    cols = {c for r in range(R) for c in range(C) if g[r][c] == 0}
    G.add(f"First mark which rows {sorted(rows)} and columns {sorted(cols)} "
          f"contain a 0 — clearing while scanning would spread fake zeros.",
          deps=[(r, c) for r in range(R) for c in range(C) if g[r][c] == 0])
    for r in range(R):
        for c in range(C):
            if (r in rows or c in cols) and G.grid[r][c] != 0:
                G.grid[r][c] = 0
                G.add(f"({r}, {c}) is in a marked row or column — set it to 0.", r, c)
    G.add("Done.", path=[(r, c) for r in range(R) for c in range(C) if G.grid[r][c] == 0])
    return G.result("set_matrix_zeros", G.grid)


def _rotate(g):
    n = len(g)
    G = Grid(n, n)
    G.grid = [r[:] for r in g]
    G.counts = {"swaps": 0}
    G.add("Rotate clockwise in place: transpose (swap across the diagonal), "
          "then reverse every row.")
    for i in range(n):
        for j in range(i + 1, n):
            G.grid[i][j], G.grid[j][i] = G.grid[j][i], G.grid[i][j]
            G.counts["swaps"] += 1
            G.add(f"Transpose: swap ({i},{j}) ↔ ({j},{i}).", i, j, [(j, i)])
    for i in range(n):
        G.grid[i].reverse()
        G.add(f"Reverse row {i}.", i, None, [(i, c) for c in range(n)])
    G.add("Rotated 90° clockwise.", path=[(r, c) for r in range(n) for c in range(n)])
    return G.result("rotate_matrix", G.grid)


def _spiral(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [r[:] for r in g]
    G.counts = {"visited": 0}
    top, bot, left, right = 0, R - 1, 0, C - 1
    out, seen = [], []

    def visit(r, c, why):
        out.append(g[r][c])
        seen.append((r, c))
        G.counts["visited"] += 1
        G.add(f"{why} {g[r][c]}.", r, c, path=seen)

    G.add("Walk the outer ring (right, down, left, up), then shrink the bounds.")
    while top <= bot and left <= right:
        for c in range(left, right + 1):
            visit(top, c, "→")
        top += 1
        for r in range(top, bot + 1):
            visit(r, right, "↓")
        right -= 1
        if top <= bot:
            for c in range(right, left - 1, -1):
                visit(bot, c, "←")
            bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1):
                visit(r, left, "↑")
            left += 1
    G.add(f"Spiral order: {out}.", path=seen)
    return G.result("spiral_order", out)


def _pascal(n):
    G = Grid(n, n)
    G.counts = {"additions": 0}
    rows = []
    G.add("Each row starts and ends with 1; every inner value is the sum of the "
          "two values above it.")
    for r in range(n):
        row = [1] * (r + 1)
        for c in range(1, r):
            row[c] = rows[r - 1][c - 1] + rows[r - 1][c]
            G.counts["additions"] += 1
        rows.append(row)
        G.grid[r][:r + 1] = row
        G.add(f"Row {r}: {row}.", r, None, [(r - 1, c) for c in range(r)] if r else [])
    G.add(f"{n} rows of Pascal's triangle.")
    return G.result("pascal_triangle", rows)


def _gap(a, b):
    n, m = len(a), len(b)
    arr = a + b
    G = Grid(1, n + m)
    G.grid[0] = arr[:]
    G.counts = {"swaps": 0}
    G.add(f"Treat both arrays as one of length {n + m} (first {n} are A). Compare "
          f"elements a 'gap' apart and swap if out of order; halve the gap "
          f"(rounding up) until it reaches 1.")
    gap = (n + m + 1) // 2
    while True:
        for i in range(0, n + m - gap):
            j = i + gap
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
                G.counts["swaps"] += 1
                G.grid[0] = arr[:]
                G.add(f"Gap {gap}: positions {i} and {j} out of order — swap.",
                      0, j, [(0, i)])
        if gap == 1:
            break
        gap = (gap + 1) // 2
    G.add(f"A = {arr[:n]}, B = {arr[n:]} — merged in place.",
          path=[(0, j) for j in range(n + m)])
    return G.result("merge_no_space", [arr[:n], arr[n:]], ["A | B"])


def _merge_count(a, algo):
    G = Grid(1, len(a))
    G.grid[0] = list(a)
    G.counts = {"count": 0}
    arr = list(a)
    rule = "a[i] > a[j]" if algo == "count_inversions" else "a[i] > 2·a[j]"
    G.add(f"Merge sort, counting pairs with i < j and {rule} while the halves "
          f"are still separate and sorted — one scan counts many pairs at once.")

    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        j, found = mid, 0
        for i in range(lo, mid):
            while j < hi and (arr[j] < arr[i] if algo == "count_inversions"
                              else 2 * arr[j] < arr[i]):
                j += 1
            found += j - mid
        G.counts["count"] += found
        arr[lo:hi] = sorted(arr[lo:hi])
        G.grid[0] = arr[:]
        G.add(f"Merge {lo}..{hi - 1}: {found} pair(s) across the halves. "
              f"Total {G.counts['count']}.", 0, lo, [(0, x) for x in range(lo, hi)])

    sort(0, len(arr))
    G.add(f"{G.counts['count']} pair(s).", path=[(0, x) for x in range(len(arr))])
    return G.result(algo, G.counts["count"], ["array"])


def _count_inversions(a):
    return _merge_count(a, "count_inversions")


def _reverse_pairs(a):
    return _merge_count(a, "reverse_pairs")
