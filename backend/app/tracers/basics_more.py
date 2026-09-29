"""Beginner-module basics the 2026 sheet added (Beginner Problems), on the
`grid` view. Numbers are split into digit cells; arrays are one cell per
value; frequency problems show a value row over a count row.

* count_odd_digits / largest_digit — peel digits with % 10 and // 10.
* perfect_number — sum the proper divisors; equal to n means perfect.
* lcm — Euclid for the gcd, then a·b / gcd.
* array_sum / count_odd_array — one pass, a running total.
* second_highest_freq / sum_high_low_freq — tally, then read the counts.
* reverse_string — two pointers swap inward.
* set_rightmost_unset_bit — n | (n + 1) flips the lowest 0 bit.
"""

from collections import Counter

from app.tracers.grid_common import Grid

TITLES = {
    "count_odd_digits": "Count Odd Digits in a Number",
    "largest_digit": "Largest Digit in a Number",
    "perfect_number": "Check for a Perfect Number",
    "lcm": "LCM of Two Numbers",
    "array_sum": "Sum of Array Elements",
    "count_odd_array": "Count Odd Numbers in an Array",
    "second_highest_freq": "Second Highest Occurring Element",
    "sum_high_low_freq": "Sum of Highest and Lowest Frequency",
    "reverse_string": "Reverse a String (Two Pointers)",
    "set_rightmost_unset_bit": "Set the Rightmost Unset Bit",
}
BITS = 8


def _int(text, lo, hi):
    try:
        v = int((text or "").strip())
    except ValueError:
        raise ValueError("Give a whole number.") from None
    if not (lo <= v <= hi):
        raise ValueError(f"Keep it between {lo} and {hi}.")
    return v


def _nums(text, n_max=12, v_max=255):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n_max) or any(abs(v) > v_max for v in a):
        raise ValueError(f"Give 1–{n_max} numbers within ±{v_max}.")
    return a


def run(algo, text, target=None):
    if algo in ("count_odd_digits", "largest_digit"):
        return globals()["_" + algo](_int(text, 0, 99_999_999))
    if algo == "perfect_number":
        return _perfect_number(_int(text, 1, 10_000))
    if algo == "set_rightmost_unset_bit":
        return _set_rightmost_unset_bit(_int(text, 0, 254))
    if algo == "lcm":
        parts = [p for p in (text or "").replace(" ", "").split(",") if p]
        if len(parts) != 2:
            raise ValueError("Give two numbers, e.g. 12,18.")
        a, b = (_int(p, 1, 9_999) for p in parts)
        return _lcm(a, b)
    if algo == "reverse_string":
        s = (text or "").strip()
        if not (1 <= len(s) <= 16):
            raise ValueError("Give 1–16 characters.")
        return _reverse_string(s)
    return globals()["_" + algo](_nums(text))


def _digits(n):
    d = [int(c) for c in str(n)]
    G = Grid(1, len(d))
    G.grid = [d[:]]
    return G, d


def _count_odd_digits(n):
    G, d = _digits(n)
    G.counts = {"odd": 0}
    G.add("Peel the last digit with n % 10, test it, then drop it with n // 10.")
    x, i = n, len(d) - 1
    done = []
    while True:
        dig = x % 10
        if dig % 2 == 1:
            G.counts["odd"] += 1
            done.append((0, i))
        G.add(f"Digit {dig} is {'odd' if dig % 2 else 'even'} → count {G.counts['odd']}.",
              0, i, path=done, match=dig % 2 == 1)
        x //= 10
        i -= 1
        if x == 0:
            break
    G.add(f"{G.counts['odd']} odd digit(s).", path=done)
    return G.result("count_odd_digits", G.counts["odd"], ["digit"])


def _largest_digit(n):
    G, d = _digits(n)
    G.counts = {"largest": -1}
    G.add("Peel digits one at a time, keeping the biggest seen so far.")
    x, i, best, where = n, len(d) - 1, -1, None
    while True:
        dig = x % 10
        if dig > best:
            best, where = dig, i
            G.counts["largest"] = best
            G.add(f"{dig} beats {'' if best == dig else best} the best so far → largest = {dig}.",
                  0, i, path=[(0, where)])
        else:
            G.add(f"{dig} ≤ {best}, keep {best}.", 0, i, path=[(0, where)], match=False)
        x //= 10
        i -= 1
        if x == 0:
            break
    G.add(f"Largest digit: {best}.", path=[(0, where)])
    return G.result("largest_digit", best, ["digit"])


def _perfect_number(n):
    divs = [d for d in range(1, n // 2 + 1) if n % d == 0] or [0]
    if n == 1:
        divs = [0]
    G = Grid(1, len(divs))
    G.grid = [divs[:]]
    G.counts = {"sum": 0}
    G.add(f"A number is perfect when its proper divisors (excluding {n}) add up to it. "
          f"Try every d ≤ n/2.")
    done = []
    for i, d in enumerate(divs):
        if d == 0:
            break
        G.counts["sum"] += d
        done.append((0, i))
        G.add(f"{n} % {d} = 0 → add {d}. Sum {G.counts['sum']}.", 0, i, path=done)
    ok = G.counts["sum"] == n
    G.add(f"Sum {G.counts['sum']} {'==' if ok else '!='} {n} → {'perfect' if ok else 'not perfect'}.",
          path=done, match=ok)
    return G.result("perfect_number", ok, ["divisor"])


def _lcm(a, b):
    rows = []
    x, y = a, b
    while y:
        rows.append([x, y, x % y])
        x, y = y, x % y
    g = x
    G = Grid(len(rows) + 1, 3)
    G.grid = [[None, None, None] for _ in range(len(rows) + 1)]
    G.counts = {"gcd": 0, "lcm": 0}
    G.add(f"lcm(a, b) = a·b / gcd(a, b). First run Euclid on {a} and {b}.")
    for i, (p, q, r) in enumerate(rows):
        G.grid[i] = [p, q, r]
        G.add(f"gcd({p}, {q}) → {p} mod {q} = {r}.", i, 2, deps=[(i, 0), (i, 1)])
    G.counts["gcd"] = g
    l = a * b // g
    G.counts["lcm"] = l
    G.grid[-1] = [a * b, g, l]
    G.add(f"gcd = {g}. lcm = {a}·{b} / {g} = {l}.", len(rows), 2,
          deps=[(len(rows), 0), (len(rows), 1)], path=[(len(rows), 2)])
    return G.result("lcm", l, [f"step {i + 1}" for i in range(len(rows))] + ["lcm"],
                    ["a", "b", "a mod b"])


def _array_sum(a):
    G = Grid(1, len(a))
    G.grid = [a[:]]
    G.counts = {"sum": 0}
    G.add("Start a running total at 0 and add every element once.")
    done = []
    for i, v in enumerate(a):
        G.counts["sum"] += v
        done.append((0, i))
        G.add(f"+ {v} → {G.counts['sum']}.", 0, i, path=done)
    G.add(f"Sum = {G.counts['sum']}.", path=done)
    return G.result("array_sum", G.counts["sum"], ["value"])


def _count_odd_array(a):
    G = Grid(1, len(a))
    G.grid = [a[:]]
    G.counts = {"odd": 0}
    G.add("Test each element: odd when x % 2 != 0 (works for negatives too).")
    done = []
    for i, v in enumerate(a):
        odd = v % 2 != 0
        if odd:
            G.counts["odd"] += 1
            done.append((0, i))
        G.add(f"{v} is {'odd' if odd else 'even'} → {G.counts['odd']}.", 0, i,
              path=done, match=odd)
    G.add(f"{G.counts['odd']} odd number(s).", path=done)
    return G.result("count_odd_array", G.counts["odd"], ["value"])


def _tally(a, algo):
    keys = list(dict.fromkeys(a))            # first-seen order
    G = Grid(2, len(keys))
    G.grid = [keys[:], [0] * len(keys)]
    G.counts = {"tallied": 0}
    G.add("Tally: one column per distinct value, its count underneath.")
    for v in a:
        c = keys.index(v)
        G.grid[1][c] += 1
        G.counts["tallied"] += 1
        G.add(f"Saw {v} → count {G.grid[1][c]}.", 1, c, deps=[(0, c)])
    return G, keys


def _second_highest_freq(a):
    G, keys = _tally(a, "second_highest_freq")
    freq = Counter(a)
    top = max(freq.values())
    rest = [f for f in freq.values() if f < top]
    if not rest:
        G.add(f"Every value occurs {top} times — there is no second highest frequency.",
              path=[(1, c) for c in range(len(keys))], match=False)
        return G.result("second_highest_freq", -1, ["value", "count"])
    second = max(rest)
    ans = next(v for v in keys if freq[v] == second)
    G.add(f"Highest frequency is {top}; the highest below it is {second}.",
          path=[(1, keys.index(v)) for v in keys if freq[v] == top])
    G.add(f"{ans} occurs {second} times — the second highest occurring element.",
          0, keys.index(ans), path=[(0, keys.index(ans)), (1, keys.index(ans))])
    return G.result("second_highest_freq", ans, ["value", "count"])


def _sum_high_low_freq(a):
    G, keys = _tally(a, "sum_high_low_freq")
    freq = Counter(a)
    hi, lo = max(freq.values()), min(freq.values())
    hc = [keys.index(v) for v in keys if freq[v] == hi]
    lc = [keys.index(v) for v in keys if freq[v] == lo]
    G.add(f"Highest frequency {hi} (value {keys[hc[0]]}).", 1, hc[0], path=[(1, c) for c in hc])
    G.add(f"Lowest frequency {lo} (value {keys[lc[0]]}).", 1, lc[0], path=[(1, c) for c in hc + lc])
    G.add(f"{hi} + {lo} = {hi + lo}.", path=[(1, c) for c in hc + lc])
    return G.result("sum_high_low_freq", hi + lo, ["value", "count"])


def _reverse_string(s):
    chars = list(s)
    G = Grid(1, len(chars))
    G.grid = [chars[:]]
    G.counts = {"swaps": 0}
    G.add("Two pointers: l at the front, r at the back. Swap and walk inward.")
    l, r = 0, len(chars) - 1
    done = []
    while l < r:
        chars[l], chars[r] = chars[r], chars[l]
        G.grid = [chars[:]]
        G.counts["swaps"] += 1
        done += [(0, l), (0, r)]
        G.add(f"Swap '{chars[r]}' and '{chars[l]}' → {''.join(chars)}.", 0, l,
              deps=[(0, r)], path=done)
        l, r = l + 1, r - 1
    G.add(f"Pointers met — reversed: {''.join(chars)}.", path=[(0, i) for i in range(len(chars))])
    return G.result("reverse_string", "".join(chars), ["char"])


def _bits(n):
    return [(n >> (BITS - 1 - c)) & 1 for c in range(BITS)]


def _set_rightmost_unset_bit(n):
    G = Grid(2, BITS)
    G.grid = [_bits(n), [None] * BITS]
    G.counts = {"result": n}
    labels = [f"b{BITS - 1 - c}" for c in range(BITS)]
    G.add(f"{n} in binary. The rightmost 0 bit is the one to set.")
    if n & (n + 1) == 0:
        G.grid[1] = _bits(n)
        G.add(f"Every bit is already 1 — {n} stays {n}.", path=[(0, c) for c in range(BITS)])
        return G.result("set_rightmost_unset_bit", n, ["n", "n | (n+1)"], labels)
    pos = 0
    while (n >> pos) & 1:
        pos += 1
    c = BITS - 1 - pos
    G.add(f"Scanning from the right, bit {pos} is the first 0.", 0, c, match=False)
    m = n + 1
    G.grid[1] = _bits(m)
    G.add(f"n + 1 = {m}: adding one carries through the trailing 1s and lands exactly on that bit.",
          1, c, deps=[(0, c)])
    r = n | m
    G.grid[1] = _bits(r)
    G.counts["result"] = r
    G.add(f"n | (n + 1) = {r}: the original bits plus that one 0 turned into 1.", 1, c,
          path=[(1, c)])
    return G.result("set_rightmost_unset_bit", r, ["n", "n | (n+1)"], labels)
