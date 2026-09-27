"""Combinatorial game theory (batch 79) on the `grid` view.

* nim — the player to move wins iff the XOR of the pile sizes is non-zero;
  a winning move shrinks one pile so the XOR becomes 0.
* grundy_numbers — for a subtraction game (remove one of the allowed counts),
  g(n) = mex{ g(n − m) }; a position is losing iff g(n) = 0. Sprague–Grundy
  says a sum of games is decided by the XOR of their Grundy numbers.
* optimal_game — coins in a line, players take either end: dp[i][j] = the
  most the player to move can collect from a[i..j] when the opponent also
  plays perfectly (they will leave us the smaller of the two follow-ups).
"""

from app.tracers.grid_common import Grid

TITLES = {
    "nim": "Nim (XOR of Piles)",
    "grundy_numbers": "Grundy Numbers (Subtraction Game)",
    "optimal_game": "Optimal Strategy for a Coin Game",
}
BITS = 6


def _nums(text, n, lo, hi):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(not (lo <= v <= hi) for v in a):
        raise ValueError(f"Give 1–{n} numbers from {lo} to {hi}.")
    return a


def run(algo, text, target=None):
    if algo == "nim":
        return _nim(_nums(text, 6, 0, 63))
    if algo == "optimal_game":
        return _coins(_nums(text, 8, 1, 99))
    if "|" not in (text or ""):
        raise ValueError("Give 'n | allowed moves', e.g. 10 | 1,3,4.")
    n_t, m_t = text.split("|", 1)
    try:
        n = int(n_t.strip())
    except ValueError:
        raise ValueError("n must be a whole number.") from None
    moves = sorted(set(_nums(m_t, 4, 1, 9)))
    if not (1 <= n <= 20):
        raise ValueError("n from 1 to 20.")
    return _grundy(n, moves)


def _bits(v):
    return [int(b) for b in format(v, f"0{BITS}b")]


def _nim(piles):
    rows = [f"pile {i}" for i in range(len(piles))] + ["XOR"]
    cols = [str(1 << (BITS - 1 - c)) for c in range(BITS)]
    G = Grid(len(piles) + 1, BITS)
    G.grid = [_bits(p) for p in piles] + [[None] * BITS]
    G.counts = {"xors": 0}
    x = 0
    G.add("Write every pile in binary. The player to move wins exactly when the "
          "XOR of all piles (the parity of each column) is non-zero.")
    for i, p in enumerate(piles):
        x ^= p
        G.counts["xors"] += 1
        G.grid[-1] = _bits(x)
        G.add(f"XOR in pile {i} ({p}) → {x}.", len(piles), None,
              [(i, c) for c in range(BITS)])
    if x == 0:
        G.add("XOR = 0: every move makes it non-zero, and the opponent can always "
              "restore 0 — the player to move LOSES.", match=False)
        return G.result("nim", {"first_wins": False, "move": None}, rows, cols)
    i = next(k for k, p in enumerate(piles) if p ^ x < p)
    G.add(f"XOR = {x} ≠ 0 — the player to move WINS. Pick a pile with the XOR's "
          f"top bit set: pile {i} ({piles[i]}) → {piles[i] ^ x}. Now the XOR is 0.",
          i, None, [], [(i, c) for c in range(BITS)])
    return G.result("nim", {"first_wins": True, "move": [i, piles[i] ^ x]}, rows, cols)


def _grundy(n, moves):
    G = Grid(2, n + 1)
    G.grid[0] = list(range(n + 1))
    G.counts = {"mex_checks": 0}
    g = [0] * (n + 1)
    G.grid[1][0] = 0
    G.add(f"Moves: remove {moves}. g(0) = 0 — no move, the player to move loses. "
          f"g(i) = mex of the Grundy numbers reachable in one move (the smallest "
          f"non-negative number NOT among them).", 1, 0)
    for i in range(1, n + 1):
        reach = sorted({g[i - m] for m in moves if m <= i})
        mex = 0
        while mex in reach:
            mex += 1
            G.counts["mex_checks"] += 1
        g[i] = mex
        G.grid[1][i] = mex
        G.add(f"g({i}): reachable {reach or '∅'} → mex = {mex}"
              + (" (losing position)." if mex == 0 else "."), 1, i,
              [(1, i - m) for m in moves if m <= i], match=mex != 0)
    G.add(f"g({n}) = {g[n]}: the player to move {'wins' if g[n] else 'loses'}. "
          f"Losing positions: {[i for i in range(n + 1) if g[i] == 0]}.",
          path=[(1, i) for i in range(n + 1) if g[i] == 0])
    return G.result("grundy_numbers", g, ["n", "grundy"])


def _coins(a):
    n = len(a)
    G = Grid(n, n)
    G.counts = {"cells": 0}
    dp = [[0] * n for _ in range(n)]
    get = lambda i, j: dp[i][j] if i <= j else 0
    G.add("dp[i][j] = the most the player to move collects from coins i..j. "
          "Taking a[i] leaves the opponent i+1..j, who then leaves us the WORSE "
          "of dp[i+2][j] and dp[i+1][j−1] — likewise for taking a[j].")
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if i == j:
                dp[i][j] = a[i]
                note, deps = f"One coin: take {a[i]}.", []
            else:
                left = a[i] + min(get(i + 2, j), get(i + 1, j - 1))
                right = a[j] + min(get(i + 1, j - 1), get(i, j - 2))
                dp[i][j] = max(left, right)
                note = (f"Coins {i}..{j}: take left {a[i]} → {left}, or right "
                        f"{a[j]} → {right}. Best {dp[i][j]}.")
                deps = [(x, y) for x, y in ((i + 2, j), (i + 1, j - 1), (i, j - 2))
                        if x <= y]
            G.grid[i][j] = dp[i][j]
            G.counts["cells"] += 1
            G.add(note, i, j, deps)
    G.add(f"The first player can guarantee {dp[0][n - 1]} of {sum(a)} "
          f"(the opponent gets {sum(a) - dp[0][n - 1]}).", 0, n - 1, path=[(0, n - 1)])
    return G.result("optimal_game", dp[0][n - 1], list(map(str, a)), list(map(str, a)))
