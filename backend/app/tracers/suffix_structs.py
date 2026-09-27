"""Suffix array family (batch 76) on the `grid` view.

* suffix_array — prefix doubling: rank suffixes by their first 1, 2, 4, …
  characters. Suffix i's rank for 2k characters is the pair (rank of its
  first k, rank of the k starting at i + k) — both already known — so each
  round is one sort of pairs. Stops when every rank is distinct.
* lcp_kasai — LCP[i] = longest common prefix of the i-th and (i−1)-th
  suffix in sorted order. Kasai walks suffixes in TEXT order: the match
  length h drops by at most 1 from one suffix to the next, so the total
  work is O(n).
* longest_repeated_substring — the answer is the largest LCP value.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "suffix_array": "Suffix Array (Prefix Doubling)",
    "lcp_kasai": "LCP Array (Kasai)",
    "longest_repeated_substring": "Longest Repeated Substring (SA + LCP)",
}


def run(algo, text, target=None):
    s = (text or "").strip().lower()
    if not (2 <= len(s) <= 10) or not s.isalpha():
        raise ValueError("Give 2–10 letters.")
    if algo == "suffix_array":
        return _sa_trace(s)
    return _kasai(s, algo)


def _sa(s, G=None):
    n = len(s)
    rank = [ord(c) - 96 for c in s]
    k, rounds = 1, 0
    if G:
        G.grid[0] = rank[:]
        G.add("Round 0: rank every suffix by its first character (a = 1 …).", 0, None,
              [], [(0, i) for i in range(n)])
    while True:
        key = lambda i: (rank[i], rank[i + k] if i + k < n else 0)
        order = sorted(range(n), key=key)
        new = [0] * n
        for j in range(1, n):
            new[order[j]] = new[order[j - 1]] + (key(order[j]) != key(order[j - 1]))
        new = [r + 1 for r in new]
        rounds += 1
        if G:
            G.grid[rounds] = new[:]
            G.counts["rounds"] = rounds
            G.add(f"Round {rounds}: sort by the pair (rank of first {k}, rank of the "
                  f"{k} after them) → ranks for the first {2 * k} characters"
                  + (" — all distinct, done." if max(new) == n else "."),
                  rounds, None, [(rounds - 1, i) for i in range(n)],
                  [(rounds, i) for i in range(n)])
        rank = new
        if max(rank) == n:
            return order
        k *= 2


def _sa_trace(s):
    n = len(s)
    G = Grid((n - 1).bit_length() + 2, n)
    G.counts = {"rounds": 0}
    sa = _sa(s, G)
    used = G.counts["rounds"] + 1
    G.grid = G.grid[:used]
    for step in G.steps:
        step["structures"]["grid"] = step["structures"]["grid"][:used]
    G.add(f"Suffix array (start positions in sorted order): {sa} — "
          f"{', '.join(repr(s[i:]) for i in sa)}.")
    return G.result("suffix_array", sa, [f"round {r}" for r in range(used)], list(s))


def _kasai(s, algo):
    n = len(s)
    sa = _sa(s)
    pos = [0] * n
    for r, i in enumerate(sa):
        pos[i] = r
    G = Grid(n, 3)
    G.grid = [[i, s[i:], None] for i in sa]
    G.counts = {"char_compares": 0}
    G.add(f"Rows are suffixes in sorted order (suffix array {sa}). Kasai visits "
          f"them in TEXT order (0, 1, 2, …): moving from suffix i to i + 1 loses "
          f"one leading character, so the match length h drops by at most 1.")
    lcp, h = [0] * n, 0
    for i in range(n):
        if pos[i] == 0:
            h = 0
            G.grid[0][2] = 0
            G.add(f"'{s[i:]}' is first in sorted order — LCP[0] = 0 by definition; "
                  f"reset h.", 0, 2)
            continue
        j = sa[pos[i] - 1]
        start = h
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[pos[i]] = h
        G.grid[pos[i]][2] = h
        G.counts["char_compares"] += h - start + 1
        G.add(f"'{s[i:]}' vs its sorted neighbour '{s[j:]}': start comparing at "
              f"h = {start} (kept from the previous suffix), match {h}.",
              pos[i], 2, [(pos[i] - 1, 1), (pos[i], 1)])
        if h:
            h -= 1
    cols = ["start", "suffix", "LCP"]
    if algo == "lcp_kasai":
        G.add(f"LCP array: {lcp}. {G.counts['char_compares']} character comparisons "
              f"in total — linear.", path=[(r, 2) for r in range(n)])
        return G.result("lcp_kasai", lcp, None, cols)
    best = max(range(n), key=lambda r: lcp[r])
    res = s[sa[best]:sa[best] + lcp[best]]
    G.add((f"The largest LCP is {lcp[best]} (rows {best - 1} and {best}): "
           f"'{res}' appears at least twice.") if lcp[best] else
          "Every LCP is 0 — no substring repeats.",
          best, 2, [(best - 1, 1), (best, 1)] if lcp[best] else [], [(best, 2)])
    return G.result("longest_repeated_substring", res, None, cols)
