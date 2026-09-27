"""Greedy (Step 12) and stack (Step 9) leftovers on the `grid` view.

* valid_paren_star — track the range [lo, hi] of possible open counts: '('
  raises both, ')' lowers both, '*' widens the range; hi < 0 fails; valid if
  lo reaches 0 at the end.
* shortest_job_first — run the shortest burst first; each job waits for the
  sum of the bursts before it.
* lru_page_faults — a cache of `capacity` pages ordered by last use; a miss
  evicts the least-recently-used page.
* insert_interval — copy intervals ending before the new one, merge every
  overlapping one into it, copy the rest.
* non_overlapping_intervals — sort by end; keep an interval if it starts at
  or after the last kept end, otherwise remove it.
* greater_to_right — for each index, count later elements that are bigger.
* sum_subarray_ranges — Σ(max − min) over all subarrays = Σ a[i]·(times a[i]
  is the max) − Σ a[i]·(times it is the min); a monotonic stack finds each
  element's reach to the left and right.
* celebrity — eliminate with two pointers (if A knows B, A isn't the
  celebrity; else B isn't), then verify the survivor.
"""

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "valid_paren_star": "Valid Parenthesis String (with *)",
    "shortest_job_first": "Shortest Job First (SJF) Scheduling",
    "lru_page_faults": "LRU Page Replacement (Page Faults)",
    "insert_interval": "Insert Interval",
    "non_overlapping_intervals": "Non-overlapping Intervals",
    "greater_to_right": "Number of Greater Elements to the Right",
    "sum_subarray_ranges": "Sum of Subarray Ranges",
    "celebrity": "The Celebrity Problem",
}


def _nums(text, n=12, lo=-999):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(not (lo <= v <= 999) for v in a):
        raise ValueError(f"Give 1–{n} numbers within {lo}..999.")
    return a


def _intervals(text, n=8):
    out = []
    for p in [p for p in (text or "").replace(" ", "").split(",") if p]:
        try:
            s, e = (int(x) for x in p.split("-"))
        except ValueError:
            raise ValueError("Give intervals like 1-3,6-9.") from None
        if not (0 <= s <= e <= 99):
            raise ValueError("Each interval is start-end with 0 ≤ start ≤ end ≤ 99.")
        out.append([s, e])
    if not (1 <= len(out) <= n):
        raise ValueError(f"Give 1–{n} intervals.")
    return out


def run(algo, text, target=None):
    if algo == "valid_paren_star":
        s = (text or "").replace(" ", "")
        if not (1 <= len(s) <= 16) or any(c not in "()*" for c in s):
            raise ValueError("Use only ( ) and *, up to 16 characters.")
        return _paren_star(s)
    if algo == "shortest_job_first":
        return _sjf(_nums(text, 10, 1))
    if algo == "lru_page_faults":
        a = _nums(text, 14, 0)
        if target is None or target != int(target) or not (1 <= target <= 6):
            raise ValueError("Capacity must be 1–6.")
        return _lru(a, int(target))
    if algo == "insert_interval":
        if "|" not in (text or ""):
            raise ValueError("Give 'intervals | new', e.g. 1-3,6-9 | 2-5.")
        left, new = text.split("|", 1)
        ivs = _intervals(left)
        if ivs != sorted(ivs) or any(ivs[i][1] >= ivs[i + 1][0] for i in range(len(ivs) - 1)):
            raise ValueError("The intervals must be sorted and non-overlapping.")
        return _insert(ivs, _intervals(new, 1)[0])
    if algo == "non_overlapping_intervals":
        return _non_overlap(_intervals(text, 10))
    if algo == "greater_to_right":
        return _greater(_nums(text, 10))
    if algo == "sum_subarray_ranges":
        return _ranges(_nums(text, 10))
    if algo == "celebrity":
        g = parse_matrix(text, max_side=6)
        if len(g[0]) != len(g) or any(v not in (0, 1) for r in g for v in r):
            raise ValueError("Give a square 0/1 'knows' matrix.")
        return _celebrity(g)
    raise ValueError("Unknown algorithm.")


def _paren_star(s):
    G = Grid(3, len(s))
    G.grid[0] = list(s)
    G.counts = {"chars": 0}
    lo = hi = 0
    G.add("We don't know what each '*' is, so track the RANGE of possible open "
          "counts [lo, hi]. lo never goes below 0 (we'd pick a different '*' "
          "meaning); hi < 0 means too many ')'.")
    for i, c in enumerate(s):
        G.counts["chars"] += 1
        if c == "(":
            lo, hi, why = lo + 1, hi + 1, "'(' opens one more"
        elif c == ")":
            lo, hi, why = lo - 1, hi - 1, "')' closes one"
        else:
            lo, hi, why = lo - 1, hi + 1, "'*' could be ')', empty or '('"
        if hi < 0:
            G.grid[1][i], G.grid[2][i] = max(lo, 0), hi
            G.add(f"{why}: hi = {hi} < 0 — more ')' than any reading can open. "
                  f"Invalid.", 2, i, match=False)
            return G.result("valid_paren_star", False, ["char", "lo", "hi"])
        lo = max(lo, 0)
        G.grid[1][i], G.grid[2][i] = lo, hi
        G.add(f"{why} → [lo, hi] = [{lo}, {hi}].", 1, i)
    ok = lo == 0
    G.add(f"End with lo = {lo}: " + ("some reading closes every '(' — valid." if ok
                                     else "at least one '(' is never closed — invalid."),
          1, len(s) - 1, match=ok)
    return G.result("valid_paren_star", ok, ["char", "lo", "hi"])


def _sjf(bursts):
    order = sorted(range(len(bursts)), key=lambda i: (bursts[i], i))
    n = len(bursts)
    G = Grid(3, n)
    G.grid[0] = [f"P{i}" for i in order]
    G.grid[1] = [bursts[i] for i in order]
    G.counts = {"total_wait": 0}
    G.add("All jobs are ready at time 0. Running the shortest first keeps the "
          "most jobs from waiting behind a long one: sort by burst time.")
    t = 0
    for k, i in enumerate(order):
        G.grid[2][k] = t
        G.counts["total_wait"] += t
        G.add(f"P{i} (burst {bursts[i]}) starts at time {t} — it waited {t}.", 2, k,
              [(1, j) for j in range(k)])
        t += bursts[i]
    avg = round(G.counts["total_wait"] / n, 2)
    G.add(f"Total wait {G.counts['total_wait']} over {n} job(s) — average {avg:g}.",
          path=[(2, j) for j in range(n)])
    return G.result("shortest_job_first", avg, ["job", "burst", "waits"])


def _lru(pages, cap):
    n = len(pages)
    G = Grid(1 + cap, n)
    G.grid[0] = list(pages)
    G.counts = {"faults": 0, "hits": 0}
    cache = []                       # least recent first
    G.add(f"A cache with {cap} frame(s). Hit: the page moves to 'most recent'. "
          f"Miss (fault): load it; if full, evict the LEAST recently used page.")
    for i, p in enumerate(pages):
        if p in cache:
            cache.remove(p)
            cache.append(p)
            G.counts["hits"] += 1
            note, hit = f"Page {p} is cached — hit; it becomes most recent.", True
        else:
            G.counts["faults"] += 1
            ev = cache.pop(0) if len(cache) == cap else None
            cache.append(p)
            note = f"Page {p} is missing — fault" + (
                f"; evict {ev} (least recent)." if ev is not None else ".")
            hit = False
        for r in range(cap):
            G.grid[1 + r][i] = cache[len(cache) - 1 - r] if r < len(cache) else None
        G.add(note, 0, i, [(1 + r, i) for r in range(len(cache))], match=hit)
    G.add(f"{G.counts['faults']} page fault(s), {G.counts['hits']} hit(s).")
    return G.result("lru_page_faults", G.counts["faults"],
                    ["page"] + [f"#{r + 1} recent" for r in range(cap)])


def _fmt(ivs, width):
    return [f"{s}-{e}" for s, e in ivs] + [None] * (width - len(ivs))


def _insert(ivs, nw):
    w = len(ivs) + 1
    G = Grid(2, w)
    G.grid[0] = _fmt(ivs, w)
    G.counts = {"merged": 0}
    out = []
    s, e = nw
    G.add(f"Insert {s}-{e}: copy intervals that end before it starts, absorb "
          f"every interval that overlaps it, then copy the rest.")

    def show(note, col, ok=True):
        G.grid[1] = _fmt(out, w)
        G.add(note, 0 if col is not None else 1, col if col is not None else len(out) - 1,
              match=ok, path=[(1, j) for j in range(len(out))])

    i = 0
    while i < len(ivs) and ivs[i][1] < s:
        out.append(ivs[i])
        show(f"{ivs[i][0]}-{ivs[i][1]} ends before {s} — copy it.", i)
        i += 1
    while i < len(ivs) and ivs[i][0] <= e:
        s, e = min(s, ivs[i][0]), max(e, ivs[i][1])
        G.counts["merged"] += 1
        show(f"{ivs[i][0]}-{ivs[i][1]} overlaps — the new interval grows to "
             f"{s}-{e}.", i, False)
        i += 1
    out.append([s, e])
    show(f"Place the merged interval {s}-{e}.", None)
    while i < len(ivs):
        out.append(ivs[i])
        show(f"{ivs[i][0]}-{ivs[i][1]} starts after — copy it.", i)
        i += 1
    G.add(f"Result: {out}.", path=[(1, j) for j in range(len(out))])
    return G.result("insert_interval", out, ["intervals", "result"])


def _non_overlap(ivs):
    order = sorted(ivs, key=lambda x: (x[1], x[0]))
    G = Grid(1, len(order))
    G.grid[0] = _fmt(order, len(order))
    G.counts = {"removed": 0}
    G.add("Keep as many intervals as possible = remove as few as possible. Sort "
          "by end time: the interval that ends earliest leaves the most room.")
    last, kept = None, []
    for i, (s, e) in enumerate(order):
        if last is None or s >= last:
            G.add(f"{s}-{e} starts at/after {'nothing' if last is None else last}"
                  f" — keep it.", 0, i, path=[(0, j) for j in kept + [i]])
            last = e
            kept.append(i)
        else:
            G.counts["removed"] += 1
            G.add(f"{s}-{e} starts before {last} — overlaps, remove it.", 0, i,
                  match=False, path=[(0, j) for j in kept])
    G.add(f"Remove {G.counts['removed']} interval(s).", path=[(0, j) for j in kept])
    return G.result("non_overlapping_intervals", G.counts["removed"], ["by end"])


def _greater(a):
    n = len(a)
    G = Grid(2, n)
    G.grid[0] = list(a)
    G.counts = {"comparisons": 0}
    res = []
    G.add("For each index (each query), scan everything to its right and count "
          "the values bigger than it.")
    for i in range(n):
        bigger = [j for j in range(i + 1, n) if a[j] > a[i]]
        G.counts["comparisons"] += n - i - 1
        res.append(len(bigger))
        G.grid[1][i] = len(bigger)
        G.add(f"Index {i} ({a[i]}): {len(bigger)} bigger value(s) to the right.", 1, i,
              [(0, j) for j in bigger])
    G.add(f"Counts: {res}.", path=[(1, j) for j in range(n)])
    return G.result("greater_to_right", res, ["value", "greater →"])


def _reach(a, as_max):
    """For each i: how many subarrays have a[i] as their max (or min). Ties go
    to the leftmost index (strict on the left, non-strict on the right)."""
    n = len(a)
    beats = (lambda x, y: x > y) if as_max else (lambda x, y: x < y)
    left, right, st = [0] * n, [0] * n, []
    for i in range(n):
        while st and not beats(a[st[-1]], a[i]):
            st.pop()
        left[i] = i - (st[-1] if st else -1)
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):
        while st and beats(a[i], a[st[-1]]):
            st.pop()
        right[i] = (st[-1] if st else n) - i
        st.append(i)
    return [lft * rgt for lft, rgt in zip(left, right)]


def _ranges(a):
    n = len(a)
    G = Grid(3, n)
    G.grid[0] = list(a)
    G.counts = {"stack_passes": 4}
    G.add("Σ (max − min) over all subarrays = Σ a[i]·(#subarrays where a[i] is "
          "the max) − Σ a[i]·(#subarrays where it's the min). A monotonic stack "
          "finds how far each value reaches left and right.")
    mx = _reach(a, True)
    for i in range(n):
        G.grid[1][i] = mx[i]
        G.add(f"{a[i]} is the maximum of {mx[i]} subarray(s) → adds "
              f"{a[i] * mx[i]}.", 1, i)
    mn = _reach(a, False)
    for i in range(n):
        G.grid[2][i] = mn[i]
        G.add(f"{a[i]} is the minimum of {mn[i]} subarray(s) → subtracts "
              f"{a[i] * mn[i]}.", 2, i, match=False)
    plus = sum(v * c for v, c in zip(a, mx))
    minus = sum(v * c for v, c in zip(a, mn))
    G.add(f"Sum of ranges = {plus} − {minus} = {plus - minus}.")
    return G.result("sum_subarray_ranges", plus - minus, ["value", "× as max", "× as min"])


def _celebrity(m):
    n = len(m)
    G = Grid(n, n)
    G.grid = [row[:] for row in m]
    G.counts = {"questions": 0}
    G.add("m[a][b] = 1 means a knows b. A celebrity knows nobody and everybody "
          "knows them. Two pointers: if top knows bottom, top can't be the "
          "celebrity; otherwise bottom can't be.")
    top, bot = 0, n - 1
    while top < bot:
        G.counts["questions"] += 1
        if m[top][bot]:
            G.add(f"{top} knows {bot} — {top} is out.", top, bot, match=False)
            top += 1
        else:
            G.add(f"{top} doesn't know {bot} — {bot} is out.", top, bot, match=False)
            bot -= 1
    c = top
    cells = [(c, j) for j in range(n) if j != c] + [(i, c) for i in range(n) if i != c]
    G.counts["questions"] += 2 * (n - 1)
    ok = all(m[c][j] == 0 for j in range(n) if j != c) and \
        all(m[i][c] == 1 for i in range(n) if i != c)
    G.add(f"Candidate {c}: row {c} must be all 0 (knows nobody) and column {c} "
          f"all 1 (everyone knows them) → "
          f"{'celebrity!' if ok else 'fails — no celebrity.'}", c, c, cells,
          cells if ok else (), match=ok)
    return G.result("celebrity", c if ok else -1)
