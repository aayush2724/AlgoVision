"""DP remainder (Step 16): the stock-trading state machines and the LIS family.

Stocks — one column per day, one row per *state* you can be in at day's end.
Each cell takes the better of "stay in this state" or "arrive from another
state today" (buying subtracts the price, selling adds it):

* stock_ii (unlimited trades): free / hold.
* stock_iii (≤ 2 trades) and stock_iv (≤ k trades): buy1, sell1, buy2, sell2 …
* stock_cooldown: hold / sold / rest — after selling you must rest a day.
* stock_fee: free / hold, and every sale pays the fee.

LIS family — one column per element:

* print_lis — length ending at i = 1 + best earlier smaller; keep the
  predecessor to print one sequence back.
* largest_divisible_subset — sort, then "smaller" becomes "divides".
* longest_string_chain — sort words by length; a word extends a chain if
  deleting one letter gives the previous word.
* longest_bitonic — increasing-into-i plus decreasing-out-of-i, minus 1.
* number_of_lis — track both the best length and how many ways reach it.

Uses the `grid` view: the cell being computed is `row`/`col`, the cells it
reads are `deps`, and the answer (or the recovered sequence) glows green.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "stock_ii": "Best Time to Buy & Sell Stock II (Unlimited)",
    "stock_iii": "Best Time to Buy & Sell Stock III (≤ 2 Trades)",
    "stock_iv": "Best Time to Buy & Sell Stock IV (≤ k Trades)",
    "stock_cooldown": "Buy & Sell Stock With Cooldown",
    "stock_fee": "Buy & Sell Stock With Transaction Fee",
    "print_lis": "Print the Longest Increasing Subsequence",
    "largest_divisible_subset": "Largest Divisible Subset",
    "longest_string_chain": "Longest String Chain",
    "longest_bitonic": "Longest Bitonic Subsequence",
    "number_of_lis": "Number of Longest Increasing Subsequences",
}
MAX_LEN = 8


def _nums(text, lo, hi):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= MAX_LEN) or any(not (lo <= v <= hi) for v in a):
        raise ValueError(f"Give 1–{MAX_LEN} whole numbers, each {lo}–{hi}.")
    return a


def run(algo, text, target=None):
    if algo.startswith("stock_"):
        prices = _nums(text, 0, 999)
        k = None
        if algo == "stock_iv":
            if target is None or target != int(target) or not (1 <= target <= 3):
                raise ValueError("k (the number of trades) must be 1–3.")
            k = int(target)
        if algo == "stock_fee":
            if target is None or target != int(target) or not (0 <= target <= 99):
                raise ValueError("The fee must be 0–99.")
            k = int(target)
        return _stocks(algo, prices, k)
    if algo == "longest_string_chain":
        words = [w for w in (text or "").replace(" ", "").lower().split(",") if w]
        if not (1 <= len(words) <= MAX_LEN) or any(not w.isalpha() or len(w) > 6
                                                   for w in words):
            raise ValueError(f"Give 1–{MAX_LEN} words of up to 6 letters.")
        return _chain(words)
    lo = 1 if algo == "largest_divisible_subset" else -999
    return _lis(algo, _nums(text, lo, 999))


def _stocks(algo, p, k):
    n = len(p)
    if algo in ("stock_ii", "stock_fee"):
        states = ["free", "hold"]
    elif algo in ("stock_iii", "stock_iv"):
        t = 2 if algo == "stock_iii" else k
        states = [x for j in range(1, t + 1) for x in (f"buy{j}", f"sell{j}")]
    else:
        states = ["hold", "sold", "rest"]
    G = Grid(len(states) + 1, n)
    G.grid[0] = p[:]
    G.counts = {"cells": 0}
    NEG = float("-inf")
    prev = {s: (0 if s in ("free", "rest") or s.startswith("sell") else NEG)
            for s in states}
    fee = k if algo == "stock_fee" else 0
    intro = {
        "stock_ii": "Unlimited trades. Each day you end either holding a share "
                    "or free (holding none).",
        "stock_iii": "At most two trades: buy1 → sell1 → buy2 → sell2. Each "
                     "state is the best profit if that is your latest action.",
        "stock_iv": f"At most {k} trade(s): buy1, sell1, …, buy{k}, sell{k}.",
        "stock_cooldown": "hold = own a share, sold = sold today, rest = free "
                          "and allowed to buy tomorrow. After selling, rest a day.",
        "stock_fee": f"Unlimited trades, but every sale costs a fee of {fee}.",
    }[algo]
    G.add(intro + " Row 0 is the price; each cell keeps the better of staying "
          "put or arriving from another state today.", 0, 0)
    for d in range(n):
        x = p[d]
        cur = dict(prev)
        for si, s in enumerate(states):
            G.counts["cells"] += 1
            if algo in ("stock_ii", "stock_fee"):
                if s == "free":
                    cur[s] = max(prev["free"], prev["hold"] + x - fee)
                    why = f"stay free, or sell at {x}" + (f" − fee {fee}" if fee else "")
                    src = ["free", "hold"]
                else:
                    cur[s] = max(prev["hold"], prev["free"] - x)
                    why, src = f"keep holding, or buy at {x}", ["hold", "free"]
            elif algo == "stock_cooldown":
                if s == "hold":
                    cur[s] = max(prev["hold"], prev["rest"] - x)
                    why, src = f"keep holding, or buy at {x} after resting", ["hold", "rest"]
                elif s == "sold":
                    cur[s] = prev["hold"] + x
                    why, src = f"sell today at {x}", ["hold"]
                else:
                    cur[s] = max(prev["rest"], prev["sold"])
                    why, src = "rest, or cool down after yesterday's sale", ["rest", "sold"]
            else:
                j = int(s[-1])
                if s.startswith("buy"):
                    before = 0 if j == 1 else cur[f"sell{j - 1}"]
                    cur[s] = max(prev[s], before - x)
                    why = (f"keep, or buy at {x}" +
                           (f" using sell{j - 1}'s profit" if j > 1 else ""))
                    src = [s] + ([f"sell{j - 1}"] if j > 1 else [])
                else:
                    cur[s] = max(prev[s], cur[f"buy{j}"] + x)
                    why, src = f"keep, or sell at {x} after buy{j}", [s, f"buy{j}"]
            G.grid[si + 1][d] = None if cur[s] == NEG else cur[s]
            deps = [(states.index(z) + 1, d - 1) for z in src] if d else []
            G.add(f"Day {d}, {s}: {why} → {cur[s] if cur[s] != NEG else '—'}.",
                  si + 1, d, deps)
        prev = cur
    ends = [s for s in states if not s.startswith(("hold", "buy"))]
    best = max(prev[s] for s in ends)
    G.add(f"Best profit: {best}.",
          path=[(states.index(s) + 1, n - 1) for s in ends if prev[s] == best])
    return G.result(algo, best, ["price"] + states, [f"d{d}" for d in range(n)])


def _lis(algo, a):
    if algo == "largest_divisible_subset":
        a = sorted(set(a))
    if algo == "longest_bitonic":
        return _bitonic(a)
    n = len(a)
    ok = ((lambda j, i: a[i] % a[j] == 0) if algo == "largest_divisible_subset"
          else (lambda j, i: a[j] < a[i]))
    rows = ["value", "length", "count" if algo == "number_of_lis" else "prev"]
    G = Grid(3, n)
    G.grid[0] = a[:]
    G.counts = {"comparisons": 0}
    L, C, P = [1] * n, [1] * n, [None] * n
    rel = "divides" if algo == "largest_divisible_subset" else "is smaller than"
    G.add(("Sorted first, so only earlier values can divide later ones. "
           if algo == "largest_divisible_subset" else "")
          + f"For each i, look back at every j that {rel} a[i]: the best chain "
          f"ending at i extends the best such j.")
    for i in range(n):
        deps = []
        for j in range(i):
            G.counts["comparisons"] += 1
            if not ok(j, i):
                continue
            deps.append((1, j))
            if L[j] + 1 > L[i]:
                L[i], C[i], P[i] = L[j] + 1, C[j], j
            elif L[j] + 1 == L[i]:
                C[i] += C[j]
        G.grid[1][i] = L[i]
        G.grid[2][i] = C[i] if algo == "number_of_lis" else ("—" if P[i] is None else P[i])
        extra = (f", reached {C[i]} way(s)" if algo == "number_of_lis"
                 else (f", after index {P[i]}" if P[i] is not None else ", starts fresh"))
        G.add(f"i={i} ({a[i]}): longest chain ending here is {L[i]}{extra}.",
              1, i, deps)
    best = max(L)
    if algo == "number_of_lis":
        res = sum(C[i] for i in range(n) if L[i] == best)
        G.add(f"LIS length {best}; adding the counts of every position with that "
              f"length gives {res} sequence(s).",
              path=[(1, i) for i in range(n) if L[i] == best])
        return G.result(algo, res, rows)
    i = L.index(best)
    seq, path = [], []
    while i is not None:
        seq.append(a[i])
        path.append((0, i))
        i = P[i]
    seq.reverse()
    G.add(f"Longest length {best}; follow the predecessors back: {seq}.", path=path)
    return G.result(algo, seq, rows)


def _bitonic(a):
    n = len(a)
    G = Grid(4, n)
    G.grid[0] = a[:]
    G.counts = {"comparisons": 0}
    up, down = [1] * n, [1] * n
    G.add("Bitonic = rises then falls. 'up' is the longest increasing run "
          "ending at i (left to right); 'down' the longest decreasing run "
          "starting at i (right to left).")
    for i in range(n):
        for j in range(i):
            G.counts["comparisons"] += 1
            if a[j] < a[i]:
                up[i] = max(up[i], up[j] + 1)
        G.grid[1][i] = up[i]
        G.add(f"up[{i}] = {up[i]}.", 1, i, [(1, j) for j in range(i) if a[j] < a[i]])
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            G.counts["comparisons"] += 1
            if a[j] < a[i]:
                down[i] = max(down[i], down[j] + 1)
        G.grid[2][i] = down[i]
        G.add(f"down[{i}] = {down[i]}.", 2, i,
              [(2, j) for j in range(i + 1, n) if a[j] < a[i]])
    for i in range(n):
        G.grid[3][i] = up[i] + down[i] - 1
        G.add(f"Peak at {i}: {up[i]} + {down[i]} − 1 = {G.grid[3][i]}.", 3, i,
              [(1, i), (2, i)])
    best = max(G.grid[3])
    G.add(f"Longest bitonic subsequence: {best}.",
          path=[(3, i) for i in range(n) if G.grid[3][i] == best])
    return G.result("longest_bitonic", best, ["value", "up", "down", "total"])


def _chain(words):
    words = sorted(dict.fromkeys(words), key=lambda w: (len(w), w))
    n = len(words)
    G = Grid(2, n)
    G.grid[0] = words[:]
    G.counts = {"checks": 0}
    L = [1] * n

    def pred(short, long):
        return len(long) == len(short) + 1 and any(
            long[:k] + long[k + 1:] == short for k in range(len(long)))

    G.add("Sort by length. A word extends a chain when deleting one of its "
          "letters gives an earlier word.")
    for i in range(n):
        deps = []
        for j in range(i):
            G.counts["checks"] += 1
            if pred(words[j], words[i]):
                deps.append((1, j))
                L[i] = max(L[i], L[j] + 1)
        G.grid[1][i] = L[i]
        G.add(f"'{words[i]}': longest chain ending here is {L[i]}.", 1, i, deps)
    best = max(L)
    G.add(f"Longest string chain: {best}.",
          path=[(1, i) for i in range(n) if L[i] == best])
    return G.result("longest_string_chain", best, ["word", "chain"])
