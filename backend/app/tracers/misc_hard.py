"""Last leftovers (Steps 11, 15, 16) on the `grid` view.

* ninja_friends — two friends start in the top corners and step down one row
  at a time (column −1, 0 or +1), collecting chocolates; a shared cell
  counts once. dp over (row, col1, col2) from the bottom up; then replay the
  best choices from the top.
* max_sum_combination — sort both arrays descending; a max-heap starts
  with (0, 0); popping (i, j) offers (i+1, j) and (i, j+1), with a visited
  set so no pair is pushed twice.
* accounts_merge — union accounts that share an email (DSU keyed by the
  first account owning each email), then group emails by root.
"""

import heapq

from app.tracers.grid_common import Grid, parse_matrix

TITLES = {
    "ninja_friends": "Ninja and His Friends (Cherry Pickup II)",
    "max_sum_combination": "Maximum Sum Combinations",
    "accounts_merge": "Accounts Merge",
}


def run(algo, text, target=None):
    if algo == "ninja_friends":
        g = parse_matrix(text, max_side=5)
        if len(g[0]) < 2 or any(not (0 <= v <= 99) for r in g for v in r):
            raise ValueError("At least 2 columns; cells 0–99.")
        return _ninja(g)
    if algo == "max_sum_combination":
        if "|" not in (text or ""):
            raise ValueError("Give two arrays separated by '|', e.g. 1,4,2,3 | 2,5,1,6.")
        try:
            a, b = ([int(x) for x in p.replace(" ", "").split(",") if x]
                    for p in text.split("|", 1))
        except ValueError:
            raise ValueError("Numbers only, separated by commas.") from None
        if not (1 <= len(a) <= 6 and len(a) == len(b)) or any(abs(v) > 99 for v in a + b):
            raise ValueError("Two arrays of the same length (1–6), values within ±99.")
        if target is None or target != int(target) or not (1 <= target <= len(a) ** 2):
            raise ValueError(f"k must be 1–{len(a) ** 2}.")
        return _combos(a, b, int(target))
    return _accounts(_parse_accounts(text))


def _ninja(g):
    R, C = len(g), len(g[0])
    G = Grid(R, C)
    G.grid = [row[:] for row in g]
    G.counts = {"states": 0}
    moves = (-1, 0, 1)
    dp = [[[0] * C for _ in range(C)] for _ in range(R)]
    G.add(f"Alice starts at (0, 0), Bob at (0, {C - 1}). Each step both move "
          f"down-left, down or down-right. State = (row, Alice's column, Bob's "
          f"column): 3 × 3 = 9 move pairs per state. Solve from the last row up.")

    def nexts(a, b):
        return [(a + da, b + db) for da in moves for db in moves
                if 0 <= a + da < C and 0 <= b + db < C]

    for r in range(R - 1, -1, -1):
        for a in range(C):
            for b in range(C):
                here = g[r][a] + (g[r][b] if a != b else 0)
                dp[r][a][b] = here + (max(dp[r + 1][x][y] for x, y in nexts(a, b))
                                      if r < R - 1 else 0)
                G.counts["states"] += 1
        top = max((dp[r][a][b], a, b) for a in range(C) for b in range(C))
        G.add(f"Row {r} done: {C * C} states. Best from this row down if they "
              f"stood at columns {top[1]} and {top[2]}: {top[0]}.", r, None,
              [(r, top[1]), (r, top[2])])
    a, b = 0, C - 1
    path, total = [], dp[0][0][C - 1]
    for r in range(R):
        path += [(r, a), (r, b)]
        G.add(f"Row {r}: Alice at {a}, Bob at {b} — collect {g[r][a]}"
              + (f" + {g[r][b]}" if a != b else " (same cell, counted once)") + ".",
              r, a, [(r, b)], path)
        if r < R - 1:
            a, b = max(nexts(a, b), key=lambda p: dp[r + 1][p[0]][p[1]])
    G.add(f"Maximum chocolates: {total}.", path=path)
    return G.result("ninja_friends", total)


def _combos(a, b, k):
    A, B = sorted(a, reverse=True), sorted(b, reverse=True)
    n = len(A)
    G = Grid(2, n)
    G.grid = [A[:], B[:]]
    G.counts = {"heap_pops": 0, "pushes": 1}
    heap, seen, out = [(-(A[0] + B[0]), 0, 0)], {(0, 0)}, []
    G.add("Sort both arrays descending: A[0] + B[0] is the largest sum. The next "
          "largest is always a neighbour (i+1, j) or (i, j+1) of a pair already "
          "taken, so a max-heap of frontier pairs finds them in order.")
    while len(out) < k:
        s, i, j = heapq.heappop(heap)
        out.append(-s)
        G.counts["heap_pops"] += 1
        pushed = []
        for ni, nj in ((i + 1, j), (i, j + 1)):
            if ni < n and nj < n and (ni, nj) not in seen:
                seen.add((ni, nj))
                heapq.heappush(heap, (-(A[ni] + B[nj]), ni, nj))
                G.counts["pushes"] += 1
                pushed.append(f"({ni},{nj})")
        G.add(f"Pop A[{i}] + B[{j}] = {A[i]} + {B[j]} = {-s}. Push "
              f"{', '.join(pushed) or 'nothing new'}. Sums so far {out}.",
              0, i, [(1, j)], [(0, i), (1, j)])
    G.add(f"The {k} largest sums: {out}.")
    return G.result("max_sum_combination", out, ["A (desc)", "B (desc)"])


def _parse_accounts(text):
    accts = []
    for part in [p.strip() for p in (text or "").split(";") if p.strip()]:
        words = part.replace(",", " ").split()
        if len(words) < 2 or not words[0].isalpha() or \
                not all(w.replace("@", "").replace(".", "").isalnum() for w in words[1:]):
            raise ValueError("Each account is 'Name email email …'; accounts are "
                             "separated by ';'.")
        accts.append((words[0], list(dict.fromkeys(words[1:]))))
    if not (1 <= len(accts) <= 6) or any(len(e) > 4 for _, e in accts):
        raise ValueError("1–6 accounts with at most 4 emails each.")
    return accts


def _accounts(accts):
    n = len(accts)
    w = max(len(e) for _, e in accts)
    G = Grid(n, w + 2)
    G.grid = [[name] + emails + [None] * (w - len(emails)) + [i]
              for i, (name, emails) in enumerate(accts)]
    G.counts = {"unions": 0}
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    owner = {}
    G.add("Each account is a DSU node (last column = its root). Walk every "
          "email: the first account to own it becomes its owner; any later "
          "account with the same email is unioned with the owner.")
    for i, (_, emails) in enumerate(accts):
        for k, e in enumerate(emails):
            if e not in owner:
                owner[e] = i
                continue
            ra, rb = find(owner[e]), find(i)
            first = (owner[e], accts[owner[e]][1].index(e) + 1)
            if ra != rb:
                parent[rb] = ra
                G.counts["unions"] += 1
                for r in range(n):
                    G.grid[r][w + 1] = find(r)
                G.add(f"'{e}' also belongs to account {owner[e]} — union account "
                      f"{i}'s group into {ra}.", i, k + 1, [first])
            else:
                G.add(f"'{e}' is shared, but accounts {owner[e]} and {i} are "
                      f"already joined.", i, k + 1, [first], match=False)
    groups = {}
    for e, i in owner.items():
        groups.setdefault(find(i), set()).add(e)
    res = sorted([accts[r][0]] + sorted(es) for r, es in groups.items())
    for r in range(n):
        G.grid[r][w + 1] = find(r)
    G.add(f"Group emails by root and sort them: {res}.",
          path=[(r, w + 1) for r in range(n)])
    return G.result("accounts_merge", res, [f"acct {i}" for i in range(n)],
                    ["name"] + [f"email {k + 1}" for k in range(w)] + ["root"])
