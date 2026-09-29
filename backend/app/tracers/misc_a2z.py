"""Three leftovers from the 2026 sheet, on the `grid` view.

* single_number_ii — every value appears three times except one: count the
  1s in each bit position; positions where count % 3 == 1 belong to the
  lonely number.
* distinct_islands — flood each island and record its shape as cell offsets
  from its first cell; two islands are the same shape when the offset lists
  match. Count distinct shapes.
* shortest_palindrome — the longest palindromic prefix is the longest border
  (KMP lps) of s + '#' + reverse(s); prepend the reversed remainder.
"""

from collections import deque

from app.tracers.grid_common import Grid, parse_matrix, DIRS4

TITLES = {
    "single_number_ii": "Single Number II (Every Other Value Thrice)",
    "distinct_islands": "Number of Distinct Islands",
    "shortest_palindrome": "Shortest Palindrome (KMP)",
}
BITS = 8


def run(algo, text, target=None):
    if algo == "distinct_islands":
        g = parse_matrix(text)
        if any(v not in (0, 1) for r in g for v in r):
            raise ValueError("Cells must be 0 or 1.")
        return _distinct(g)
    if algo == "shortest_palindrome":
        s = (text or "").strip()
        if not (1 <= len(s) <= 10) or " " in s:
            raise ValueError("Give one word of 1–10 characters.")
        return _shortest_pal(s)
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= 10) or any(not (0 <= v <= 255) for v in a):
        raise ValueError("Give 1–10 numbers from 0 to 255.")
    from collections import Counter
    c = Counter(a)
    if list(c.values()).count(1) != 1 or any(v not in (1, 3) for v in c.values()):
        raise ValueError("Every value three times except exactly one that appears once.")
    return _single_ii(a)


def _bits(n):
    return [(n >> (BITS - 1 - c)) & 1 for c in range(BITS)]


def _single_ii(a):
    n = len(a)
    G = Grid(n + 2, BITS)
    G.grid = [_bits(v) for v in a] + [[0] * BITS, [None] * BITS]
    G.counts = {"result": 0}
    labels = [str(v) for v in a] + ["count % 3", "answer"]
    cols = [f"b{BITS - 1 - c}" for c in range(BITS)]
    G.add("Write every number in binary. A value that appears 3 times adds 3 to each of "
          "its 1-bits; only the lonely value leaves a remainder when you count mod 3.")
    ans = 0
    for c in range(BITS):
        cnt = sum(G.grid[r][c] for r in range(n))
        G.grid[n][c] = cnt % 3
        deps = [(r, c) for r in range(n) if G.grid[r][c]]
        bit = cnt % 3
        if bit:
            ans |= 1 << (BITS - 1 - c)
        G.grid[n + 1][c] = bit
        G.add(f"Bit {BITS - 1 - c}: {cnt} ones → {cnt} % 3 = {bit}.", n, c, deps=deps,
              path=[(n + 1, k) for k in range(c + 1)], match=bool(bit))
    G.counts["result"] = ans
    G.add(f"Read the remainders as a number: {ans}.", path=[(n + 1, k) for k in range(BITS)])
    return G.result("single_number_ii", ans, labels, cols)


def _distinct(src):
    R, C = len(src), len(src[0])
    G = Grid(R, C)
    G.grid = [["·" if v == 0 else "1" for v in row] for row in src]
    G.counts = {"islands": 0, "distinct": 0}
    seen: set = set()
    shapes: dict = {}
    done: list = []
    G.add("Flood each island; record its shape as offsets from the first cell "
          "(row-major). Islands with identical offset lists are the same shape.")
    for r in range(R):
        for c in range(C):
            if src[r][c] != 1 or (r, c) in seen:
                continue
            G.counts["islands"] += 1
            q = deque([(r, c)])
            seen.add((r, c))
            cells = [(r, c)]
            while q:
                cr, cc = q.popleft()
                for dr, dc in DIRS4:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < R and 0 <= nc < C and src[nr][nc] == 1 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))
                        cells.append((nr, nc))
            cells.sort()
            shape = tuple((x - r, y - c) for x, y in cells)
            if shape in shapes:
                label = shapes[shape]
                G.add(f"Island at ({r}, {c}) has offsets {list(shape)} — same shape as {label}.",
                      r, c, deps=cells, path=done, match=False)
            else:
                label = chr(ord("A") + len(shapes) % 26)
                shapes[shape] = label
                G.counts["distinct"] += 1
                G.add(f"Island at ({r}, {c}) has offsets {list(shape)} — new shape {label}.",
                      r, c, deps=cells, path=done)
            for x, y in cells:
                G.grid[x][y] = label
            done += cells
            G.add(f"Stamp it {label}.", r, c, path=done)
    G.add(f"{G.counts['distinct']} distinct shape(s) among {G.counts['islands']} island(s).",
          path=done)
    return G.result("distinct_islands", G.counts["distinct"])


def _shortest_pal(s):
    rev = s[::-1]
    t = s + "#" + rev
    m = len(t)
    G = Grid(2, m)
    G.grid = [list(t), [None] * m]
    G.counts = {"lps": 0}
    G.add(f"Build t = s + '#' + reverse(s) = '{t}'. The longest border of t (a prefix that "
          f"is also a suffix) is the longest palindromic prefix of s.")
    lps = [0] * m
    G.grid[1][0] = 0
    G.add("lps[0] = 0.", 1, 0, deps=[(0, 0)])
    k = 0
    for i in range(1, m):
        while k > 0 and t[i] != t[k]:
            k = lps[k - 1]
            G.add(f"t[{i}]='{t[i]}' ≠ t[{k if k else 0}] — fall back to lps = {k}.", 1, i,
                  deps=[(0, i), (0, k)], match=False)
        if t[i] == t[k]:
            k += 1
        lps[i] = k
        G.grid[1][i] = k
        G.add(f"t[{i}]='{t[i]}' vs t[{k - 1 if k else 0}]: lps[{i}] = {k}.", 1, i,
              deps=[(0, i), (0, max(k - 1, 0))], path=[(1, j) for j in range(i + 1)])
    L = lps[-1]
    G.counts["lps"] = L
    ans = s[L:][::-1] + s
    G.add(f"Border length {L}: '{s[:L]}' is the longest palindromic prefix. Prepend the "
          f"reversed remainder '{s[L:][::-1]}' → '{ans}'.", path=[(0, j) for j in range(L)])
    return G.result("shortest_palindrome", ans, ["t", "lps"], [str(i) for i in range(m)])
