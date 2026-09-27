"""Interval DP and the subset-difference family (Step 16).

Interval DP — a cell (i, j) answers "the best for the stretch i..j", filled by
increasing length so every smaller stretch is already known:
* cut_stick — the first cut in i..j costs the current stick length; then the
  two halves are independent.
* burst_balloons — choose the LAST balloon k to burst in i..j: it pays
  a[i−1]·a[k]·a[j+1], its neighbours outside the range.
* boolean_evaluation — for operands i..j, count the ways to be True / False by
  splitting at every operator.

Front partitions (one row):
* palindrome_partition_ii — pieces[i] = 1 + min pieces after a palindromic
  s[i..j]; cuts = pieces − 1.
* partition_array_max_sum — best[i] = max over the next ≤ k items of
  (their max × count) + best after them.

Subset tables:
* min_subset_diff — mark every reachable subset sum; the answer is the
  smallest |total − 2s|.
* count_partitions_diff / target_sum — both are "count subsets summing to
  (total − d) / 2".
* max_rectangle_ones — each row turns the matrix into a histogram of column
  heights; the largest rectangle is the best over all rows.
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "cut_stick": "Minimum Cost to Cut a Stick",
    "burst_balloons": "Burst Balloons",
    "boolean_evaluation": "Evaluate Boolean Expression to True",
    "palindrome_partition_ii": "Palindrome Partitioning II (Min Cuts)",
    "partition_array_max_sum": "Partition Array for Maximum Sum",
    "min_subset_diff": "Partition Into Two Subsets With Minimum Difference",
    "count_partitions_diff": "Count Partitions With Given Difference",
    "target_sum": "Target Sum",
    "max_rectangle_ones": "Maximal Rectangle of 1s",
}


def _nums(text, lo, hi, n=8):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(not (lo <= v <= hi) for v in a):
        raise ValueError(f"Give 1–{n} whole numbers, each {lo}–{hi}.")
    return a


def run(algo, text, target=None):
    if algo == "cut_stick":
        if "|" not in (text or ""):
            raise ValueError("Give 'length | cuts', e.g. 7 | 1,3,4,5.")
        head, cuts = text.split("|", 1)
        try:
            n = int(head.strip())
        except ValueError:
            raise ValueError("The stick length must be a whole number.") from None
        c = _nums(cuts, 1, 99, 6)
        if not (2 <= n <= 99) or any(x >= n for x in c) or len(set(c)) != len(c):
            raise ValueError("Length 2–99; distinct cuts strictly inside the stick.")
        return _cut(n, sorted(c))
    if algo == "burst_balloons":
        return _burst(_nums(text, 0, 9, 6))
    if algo == "boolean_evaluation":
        s = (text or "").replace(" ", "").upper()
        if not (1 <= len(s) <= 11) or len(s) % 2 == 0 or \
                any(c not in "TF" for c in s[::2]) or any(c not in "&|^" for c in s[1::2]):
            raise ValueError("Alternate T/F with & | ^, e.g. T|F&T^F (up to 6 operands).")
        return _boolean(s)
    if algo == "palindrome_partition_ii":
        s = (text or "").replace(" ", "").lower()
        if not (1 <= len(s) <= 10) or not s.isalnum():
            raise ValueError("Give 1–10 letters/digits.")
        return _pal_cuts(s)
    if algo == "partition_array_max_sum":
        a = _nums(text, 0, 99, 10)
        if target is None or target != int(target) or not (1 <= target <= len(a)):
            raise ValueError(f"k must be 1–{len(a)}.")
        return _part_max(a, int(target))
    if algo == "max_rectangle_ones":
        g = parse_matrix(text, max_side=6)
        if any(v not in (0, 1) for r in g for v in r):
            raise ValueError("Cells must be 0 or 1.")
        return _max_rect(g)
    a = _nums(text, 0, 12, 6)
    if sum(a) > 24:
        raise ValueError("Keep the total at most 24 so the table fits.")
    if algo == "min_subset_diff":
        return _min_diff(a)
    if target is None or target != int(target) or abs(target) > 24:
        raise ValueError("Give the difference / target (−24 to 24).")
    return _count_diff(algo, a, int(target))


def _interval_deps(i, j):
    """Cells a range i..j reads (0-based grid coordinates for 1-based i, j)."""
    return [(i - 1, k - 2) for k in range(i + 1, j + 1)] + \
           [(k, j - 1) for k in range(i, j)]


def _cut(n, cuts):
    pts = [0] + cuts + [n]
    c = len(cuts)
    G = Grid(c, c)
    G.counts = {"cells": 0}
    dp = [[0] * (c + 2) for _ in range(c + 2)]
    G.add(f"Cuts {cuts} on a stick of {n}. Cell (i, j) = cheapest way to make "
          f"cuts i..j; the first cut made costs the current piece's length. "
          f"Fill short ranges first.")
    for length in range(1, c + 1):
        for i in range(1, c - length + 2):
            j = i + length - 1
            best, arg = None, None
            for k in range(i, j + 1):
                v = pts[j + 1] - pts[i - 1] + dp[i][k - 1] + dp[k + 1][j]
                if best is None or v < best:
                    best, arg = v, k
            dp[i][j] = best
            G.grid[i - 1][j - 1] = best
            G.counts["cells"] += 1
            G.add(f"Cuts {i}..{j} on the piece {pts[i - 1]}..{pts[j + 1]} "
                  f"(length {pts[j + 1] - pts[i - 1]}): cheapest is cutting at "
                  f"{pts[arg]} first → {best}.", i - 1, j - 1, _interval_deps(i, j))
    G.add(f"Minimum total cost: {dp[1][c]}.", path=[(0, c - 1)])
    return G.result("cut_stick", dp[1][c], [f"from {x}" for x in cuts],
                    [f"to {x}" for x in cuts])


def _burst(a):
    n = len(a)
    b = [1] + a + [1]
    G = Grid(n, n)
    G.counts = {"cells": 0}
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    G.add("Think of the LAST balloon k to burst in i..j: at that moment its "
          "neighbours are the balloons just outside the range, so it pays "
          "b[i−1]·b[k]·b[j+1] plus the best of the two sides.")
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            best, arg = -1, None
            for k in range(i, j + 1):
                v = b[i - 1] * b[k] * b[j + 1] + dp[i][k - 1] + dp[k + 1][j]
                if v > best:
                    best, arg = v, k
            dp[i][j] = best
            G.grid[i - 1][j - 1] = best
            G.counts["cells"] += 1
            G.add(f"Balloons {i}..{j}: bursting {b[arg]} last pays "
                  f"{b[i - 1]}·{b[arg]}·{b[j + 1]} + both sides → {best}.",
                  i - 1, j - 1, _interval_deps(i, j))
    G.add(f"Maximum coins: {dp[1][n]}.", path=[(0, n - 1)])
    return G.result("burst_balloons", dp[1][n], [str(v) for v in a], [str(v) for v in a])


def _boolean(s):
    ops = s[::2]
    n = len(ops)
    T = [[0] * n for _ in range(n)]
    F = [[0] * n for _ in range(n)]
    G = Grid(n, n)
    G.counts = {"cells": 0}
    G.add("Cell (i, j) counts the ways operands i..j can be parenthesised to "
          "give True (t) and False (f). Split at every operator between them "
          "and combine the halves' counts.")
    for i in range(n):
        T[i][i], F[i][i] = int(ops[i] == "T"), int(ops[i] == "F")
        G.grid[i][i] = f"t{T[i][i]} f{F[i][i]}"
        G.add(f"Operand {i} is {ops[i]}.", i, i)
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                op = s[2 * k + 1]
                lt, lf, rt, rf = T[i][k], F[i][k], T[k + 1][j], F[k + 1][j]
                if op == "&":
                    t, f = lt * rt, lf * rf + lt * rf + lf * rt
                elif op == "|":
                    t, f = lt * rt + lt * rf + lf * rt, lf * rf
                else:
                    t, f = lt * rf + lf * rt, lt * rt + lf * rf
                T[i][j] += t
                F[i][j] += f
            G.grid[i][j] = f"t{T[i][j]} f{F[i][j]}"
            G.counts["cells"] += 1
            G.add(f"Operands {i}..{j}: {T[i][j]} way(s) True, {F[i][j]} False.",
                  i, j, [(i, k) for k in range(i, j)] + [(k + 1, j) for k in range(i, j)])
    G.add(f"The whole expression is True in {T[0][n - 1]} way(s).", path=[(0, n - 1)])
    return G.result("boolean_evaluation", T[0][n - 1], [f"from {c}" for c in ops],
                    [f"to {c}" for c in ops])


def _pal_cuts(s):
    n = len(s)
    G = Grid(2, n + 1)
    G.grid[0] = list(s) + ["∅"]
    G.grid[1][n] = 0
    G.counts = {"checks": 0}
    best = [0] * (n + 1)
    G.add("pieces[i] = fewest palindromic pieces for s[i..]: try every first "
          "piece s[i..j] that reads the same both ways. Cuts = pieces − 1.", 1, n)
    for i in range(n - 1, -1, -1):
        cand = []
        for j in range(i, n):
            G.counts["checks"] += 1
            if s[i:j + 1] == s[i:j + 1][::-1]:
                cand.append((1 + best[j + 1], j))
        best[i], j = min(cand)
        G.grid[1][i] = best[i]
        G.add(f"From {i}: best first piece '{s[i:j + 1]}' then {best[j + 1]} "
              f"more → {best[i]} piece(s).", 1, i, [(1, jj + 1) for _, jj in cand])
    G.add(f"Minimum cuts: {best[0] - 1}.", path=[(1, 0)])
    return G.result("palindrome_partition_ii", best[0] - 1, ["char", "pieces"])


def _part_max(a, k):
    n = len(a)
    G = Grid(2, n + 1)
    G.grid[0] = a[:] + ["∅"]
    G.grid[1][n] = 0
    G.counts = {"checks": 0}
    best = [0] * (n + 1)
    G.add(f"best[i] = the most we can make from a[i..]: the next group takes "
          f"1..{k} items, all become the group's max.", 1, n)
    for i in range(n - 1, -1, -1):
        m, bv, bl = 0, -1, 0
        for ln in range(1, min(k, n - i) + 1):
            G.counts["checks"] += 1
            m = max(m, a[i + ln - 1])
            v = m * ln + best[i + ln]
            if v > bv:
                bv, bl = v, ln
        best[i] = bv
        G.grid[1][i] = bv
        G.add(f"From {i}: a group of {bl} (max {max(a[i:i + bl])}) + best after "
              f"→ {bv}.", 1, i, [(1, i + ln) for ln in range(1, min(k, n - i) + 1)])
    G.add(f"Maximum sum: {best[0]}.", path=[(1, 0)])
    return G.result("partition_array_max_sum", best[0], ["value", "best"])


def _subset_rows(a, total, count, intro):
    n = len(a)
    G = Grid(n + 1, total + 1)
    dp = [[0] * (total + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for s in range(total + 1):
        G.grid[0][s] = dp[0][s] if count else ("✓" if dp[0][s] else "·")
    G.add(intro + " Row 0 is the empty set.", 0, 0)
    for i in range(1, n + 1):
        w = a[i - 1]
        for s in range(total + 1):
            dp[i][s] = dp[i - 1][s] + (dp[i - 1][s - w] if s >= w else 0)
            if not count:
                dp[i][s] = int(dp[i][s] > 0)
            G.grid[i][s] = dp[i][s] if count else ("✓" if dp[i][s] else "·")
        G.add(f"Row {i} adds {w}: each sum is reachable without it (above) or "
              f"with it ({w} to the left, above).", i, None)
    return G, dp


def _min_diff(a):
    total = sum(a)
    G, dp = _subset_rows(a, total, False,
                         f"Split {a} into two groups with sums s and {total} − s. "
                         f"Mark every reachable subset sum, then pick s nearest "
                         f"{total}/2.")
    best = min(abs(total - 2 * s) for s in range(total + 1) if dp[len(a)][s])
    s = next(s for s in range(total // 2, -1, -1) if dp[len(a)][s])
    G.add(f"Closest reachable sum to {total}/2 is {s}: difference "
          f"|{total} − 2·{s}| = {best}.", path=[(len(a), s)])
    return G.result("min_subset_diff", best, ["∅"] + [str(v) for v in a],
                    [str(x) for x in range(total + 1)])


def _count_diff(algo, a, d):
    total = sum(a)
    if (total - d) < 0 or (total - d) % 2:
        G = Grid(1, 1)
        G.add(f"(total − d) = {total - d} must be a non-negative even number — "
              f"no split works. Answer 0.", match=False)
        return G.result(algo, 0, ["-"], ["-"])
    goal = (total - d) // 2
    what = ("two groups whose sums differ by " if algo == "count_partitions_diff"
            else "+/− signs giving ")
    G, dp = _subset_rows(a, goal, True,
                         f"Count {what}{d}: if one side sums to s, the other is "
                         f"{total} − s, so s = ({total} − {d}) / 2 = {goal}. "
                         f"Count subsets summing to {goal}.")
    res = dp[len(a)][goal]
    G.add(f"{res} way(s).", path=[(len(a), goal)])
    return G.result(algo, res, ["∅"] + [str(v) for v in a],
                    [str(x) for x in range(goal + 1)])


def _max_rect(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.counts = {"rows": 0}
    h = [0] * C
    best, cells = 0, []
    G.add("Treat each row as the floor of a histogram: a column's height is how "
          "many 1s stand directly above it (reset by a 0). Largest rectangle in "
          "each histogram, best over all rows.")
    for r in range(R):
        h = [h[c] + 1 if g[r][c] else 0 for c in range(C)]
        G.grid[r] = h[:]
        stack, row_best, span = [], 0, None
        for i in range(C + 1):
            cur = h[i] if i < C else 0
            while stack and h[stack[-1]] >= cur:
                top = stack.pop()
                left = stack[-1] + 1 if stack else 0
                area = h[top] * (i - left)
                if area > row_best:
                    row_best, span = area, (left, i - 1, h[top])
            stack.append(i)
        G.counts["rows"] += 1
        if row_best > best:
            best = row_best
            cells = [(rr, c) for c in range(span[0], span[1] + 1)
                     for rr in range(r - span[2] + 1, r + 1)]
        G.add(f"Row {r} heights {h}: largest rectangle here {row_best}. Best "
              f"{best}.", r, None, [(r, c) for c in range(C)], cells)
    G.add(f"Largest rectangle of 1s: {best}.", path=cells)
    return G.result("max_rectangle_ones", best)
