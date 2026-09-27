"""Basics (Step 1) and bit tricks (Step 8) on the `grid` view.

Numbers are split into digit cells so each step shows which digit is being
handled; bit problems show a number's 8 bits (most significant on the left).
"""

import math
from collections import Counter

from app.tracers.grid_common import Grid

TITLES = {
    "count_digits": "Count Digits of a Number",
    "reverse_number": "Reverse a Number",
    "palindrome_number": "Palindrome Number",
    "armstrong_number": "Armstrong Number",
    "print_divisors": "Print All Divisors",
    "check_prime": "Check for a Prime Number",
    "factorial": "Factorial of a Number",
    "sum_first_n": "Sum of the First N Numbers",
    "reverse_array": "Reverse an Array (Two Pointers)",
    "palindrome_string": "Check if a String is a Palindrome",
    "frequency_count": "Count Frequencies / Highest Occurring Element",
    "check_ith_bit": "Check if the i-th Bit is Set",
    "check_odd": "Check if a Number is Odd (Bitwise)",
    "swap_xor": "Swap Two Numbers With XOR",
    "divide_bits": "Divide Without * or /",
    "xor_range": "XOR of Numbers in a Range",
    "single_number_iii": "Single Number III (Two Uniques)",
}
BITS = 8
BIT_COLS = [f"b{7 - c}" for c in range(BITS)]


def _int(text, lo, hi):
    try:
        v = int((text or "").strip())
    except ValueError:
        raise ValueError("Give a whole number.") from None
    if not (lo <= v <= hi):
        raise ValueError(f"Keep it between {lo} and {hi}.")
    return v


def run(algo, text, target=None):
    if algo in ("reverse_array", "frequency_count", "single_number_iii"):
        try:
            a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
        except ValueError:
            raise ValueError("Numbers only, separated by commas.") from None
        if not (1 <= len(a) <= 12) or any(abs(v) > 255 for v in a):
            raise ValueError("Give 1–12 numbers within ±255.")
        if algo == "single_number_iii":
            c = Counter(a)
            if list(c.values()).count(1) != 2 or any(v not in (1, 2) for v in c.values()):
                raise ValueError("Every value twice except exactly two that appear once.")
        return globals()["_" + algo](a)
    if algo == "palindrome_string":
        if not (1 <= len(text or "") <= 16):
            raise ValueError("Give 1–16 characters.")
        return _palindrome_string(text)
    if algo == "xor_range":
        try:
            parts = [int(p) for p in (text or "").replace(" ", "").split(",")]
        except ValueError:
            raise ValueError("Give N, or L, R — e.g. 3, 9.") from None
        l, r = (1, parts[0]) if len(parts) == 1 else parts if len(parts) == 2 else (-1, -1)
        if not (0 <= l <= r <= 999):
            raise ValueError("Give N, or L ≤ R, within 0–999.")
        return _xor_range(l, r)
    if algo in ("swap_xor", "divide_bits"):
        try:
            a, b = (int(p) for p in (text or "").replace(" ", "").split(","))
        except ValueError:
            raise ValueError("Give two whole numbers, e.g. 13, 4.") from None
        if not (0 <= a <= 255 and 0 <= b <= 255) or (algo == "divide_bits" and b == 0):
            raise ValueError("Use 0–255 (and a non-zero divisor).")
        return (_swap_xor if algo == "swap_xor" else _divide_bits)(a, b)
    if algo == "check_ith_bit":
        n = _int(text, 0, 255)
        if target is None or target != int(target) or not (0 <= target < BITS):
            raise ValueError("i must be 0–7.")
        return _check_ith_bit(n, int(target))
    hi = {"factorial": 12, "sum_first_n": 1000, "check_odd": 255,
          "print_divisors": 999, "check_prime": 9999}.get(algo, 99999999)
    lo = 1 if algo == "print_divisors" else 0
    return globals()["_" + algo](_int(text, lo, hi))


def _digits(n):
    G = Grid(1, len(str(n)))
    G.grid[0] = list(str(n))
    return G


def _count_digits(n):
    G = _digits(n)
    G.counts = {"divisions": 0}
    x, c = n, 0
    G.add("Keep dividing by 10; each division removes one digit.")
    while True:
        c += 1
        G.counts["divisions"] += 1
        x //= 10
        G.add(f"Drop a digit → {x}. Count {c}.", 0, len(str(n)) - c)
        if x == 0:
            break
    return G.result("count_digits", c, ["digit"])


def _reverse_number(n):
    G = _digits(n)
    G.counts = {"steps": 0}
    x, rev, i = n, 0, len(str(n)) - 1
    G.add("Peel the last digit (n % 10) and push it onto the reversed number.")
    while True:
        rev = rev * 10 + x % 10
        G.counts["steps"] += 1
        G.add(f"Take {x % 10} → reversed {rev}.", 0, i)
        x //= 10
        i -= 1
        if x == 0:
            break
    return G.result("reverse_number", rev, ["digit"])


def _palindrome_number(n):
    out = _reverse_number(n)
    rev = out["meta"]["result"]
    out["meta"]["algorithm"] = "palindrome_number"
    out["meta"]["result"] = rev == n
    out["steps"].append({**out["steps"][-1], "i": len(out["steps"]),
                         "note": f"Reversed {rev} {'equals' if rev == n else 'differs from'} "
                                 f"{n} — {'a palindrome' if rev == n else 'not a palindrome'}."})
    return out


def _armstrong_number(n):
    G = _digits(n)
    k = len(str(n))
    G.counts = {"powers": 0}
    total = 0
    G.add(f"{n} has {k} digits: add each digit raised to the power {k}.")
    for i, d in enumerate(str(n)):
        total += int(d) ** k
        G.counts["powers"] += 1
        G.add(f"{d}^{k} = {int(d) ** k}; running sum {total}.", 0, i)
    G.add(f"{total} {'=' if total == n else '≠'} {n} — "
          f"{'an Armstrong number' if total == n else 'not Armstrong'}.")
    return G.result("armstrong_number", total == n, ["digit"])


def _print_divisors(n):
    r = math.isqrt(n)
    G = Grid(1, r)
    G.grid[0] = list(range(1, r + 1))
    G.counts = {"checks": 0}
    divs = set()
    G.add(f"Divisors come in pairs (i, {n}/i), so only check i up to √{n} = {r}.")
    for i in range(1, r + 1):
        G.counts["checks"] += 1
        if n % i == 0:
            divs |= {i, n // i}
            G.add(f"{i} divides {n}: record {i} and {n // i}.", 0, i - 1)
        else:
            G.add(f"{i} doesn't divide {n}.", 0, i - 1, match=False)
    res = sorted(divs)
    G.add(f"Divisors: {res}.", path=[(0, i - 1) for i in range(1, r + 1) if n % i == 0])
    return G.result("print_divisors", res, ["i"])


def _check_prime(n):
    r = math.isqrt(n)
    G = Grid(1, max(r - 1, 1))
    G.grid[0] = list(range(2, r + 1)) or ["—"]
    G.counts = {"checks": 0}
    G.add(f"A factor of {n} would have a partner, so trial-divide only up to "
          f"√{n} = {r}.")
    if n < 2:
        G.add(f"{n} is not prime (primes start at 2).", match=False)
        return G.result("check_prime", False, ["divisor"])
    for i in range(2, r + 1):
        G.counts["checks"] += 1
        if n % i == 0:
            G.add(f"{i} divides {n} — not prime.", 0, i - 2, match=False)
            return G.result("check_prime", False, ["divisor"])
        G.add(f"{i} doesn't divide {n}.", 0, i - 2)
    G.add(f"No divisor up to √{n} — {n} is prime.")
    return G.result("check_prime", True, ["divisor"])


def _factorial(n):
    G = Grid(2, max(n, 1))
    G.grid[0] = list(range(1, n + 1)) or [0]
    G.counts = {"multiplications": 0}
    f = 1
    G.add(f"{n}! multiplies 1 × 2 × … × {n} (0! = 1).")
    for i in range(1, n + 1):
        f *= i
        G.grid[1][i - 1] = f
        G.counts["multiplications"] += 1
        G.add(f"× {i} → {f}.", 1, i - 1)
    return G.result("factorial", f, ["i", "product"])


def _sum_first_n(n):
    G = Grid(1, 2)
    G.grid[0] = [n, n * (n + 1) // 2]
    G.counts = {"operations": 1}
    G.add(f"Pair the first and last numbers: 1 + {n}, 2 + {n - 1}, … — each pair "
          f"makes {n + 1}, so the sum is n(n + 1)/2 = {n * (n + 1) // 2}. "
          f"(Recursion would add them one by one.)", 0, 1)
    return G.result("sum_first_n", n * (n + 1) // 2, ["n → sum"])


def _reverse_array(a):
    G = Grid(1, len(a))
    G.grid[0] = list(a)
    G.counts = {"swaps": 0}
    arr = list(a)
    l, r = 0, len(a) - 1
    G.add("Swap the two ends and move both pointers inward.")
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        G.grid[0] = arr[:]
        G.counts["swaps"] += 1
        G.add(f"Swap positions {l} and {r}.", 0, l, [(0, r)])
        l, r = l + 1, r - 1
    G.add(f"Reversed: {arr}.", path=[(0, j) for j in range(len(arr))])
    return G.result("reverse_array", arr, ["array"])


def _palindrome_string(s):
    clean = [c.lower() for c in s if c.isalnum()]
    G = Grid(1, max(len(clean), 1))
    G.grid[0] = clean or [""]
    G.counts = {"comparisons": 0}
    G.add("Ignore case and non-letters; compare the outer pair, then recurse on "
          "the inside.")
    l, r = 0, len(clean) - 1
    while l < r:
        G.counts["comparisons"] += 1
        if clean[l] != clean[r]:
            G.add(f"'{clean[l]}' ≠ '{clean[r]}' — not a palindrome.", 0, l, [(0, r)],
                  match=False)
            return G.result("palindrome_string", False, ["char"])
        G.add(f"'{clean[l]}' = '{clean[r]}'.", 0, l, [(0, r)])
        l, r = l + 1, r - 1
    G.add("Every mirrored pair matched — a palindrome.",
          path=[(0, j) for j in range(len(clean))])
    return G.result("palindrome_string", True, ["char"])


def _frequency_count(a):
    cnt = Counter(a)
    vals = sorted(cnt)
    G = Grid(2, len(vals))
    G.grid[0] = vals[:]
    G.counts = {"distinct": len(vals)}
    seen = Counter()
    G.add("One pass with a hash map from value to count.")
    for v in a:
        seen[v] += 1
        G.grid[1][vals.index(v)] = seen[v]
        G.add(f"{v} → count {seen[v]}.", 1, vals.index(v))
    hi = max(vals, key=lambda v: (cnt[v], -v))
    lo = min(vals, key=lambda v: (cnt[v], v))
    G.add(f"Highest occurring: {hi} ({cnt[hi]}×); lowest: {lo} ({cnt[lo]}×).",
          path=[(1, vals.index(hi))])
    return G.result("frequency_count", {"counts": {str(k): v for k, v in cnt.items()},
                                        "highest": hi, "lowest": lo}, ["value", "count"])


def _bits(n):
    return [int(b) for b in format(n & 0xFF, "08b")]


def _check_ith_bit(n, i):
    G = Grid(3, BITS)
    G.grid = [_bits(n), _bits(1 << i), _bits(n & (1 << i))]
    G.counts = {"operations": 1}
    on = bool(n & (1 << i))
    G.add(f"Shift 1 left by {i} to make a mask with only bit {i} set; AND it with "
          f"{n}. Non-zero means the bit is set: {'yes' if on else 'no'}.",
          2, BITS - 1 - i, [(0, BITS - 1 - i), (1, BITS - 1 - i)], match=on)
    return G.result("check_ith_bit", on, [str(n), f"1<<{i}", "AND"], BIT_COLS)


def _check_odd(n):
    G = Grid(3, BITS)
    G.grid = [_bits(n), _bits(1), _bits(n & 1)]
    G.counts = {"operations": 1}
    G.add(f"The lowest bit decides parity: {n} & 1 = {n & 1} — "
          f"{'odd' if n & 1 else 'even'}.", 2, BITS - 1, [(0, BITS - 1)],
          match=bool(n & 1))
    return G.result("check_odd", bool(n & 1), [str(n), "1", "AND"], BIT_COLS)


def _swap_xor(a, b):
    G = Grid(2, BITS)
    G.counts = {"xors": 0}
    G.grid = [_bits(a), _bits(b)]
    G.add(f"Swap {a} and {b} with three XORs and no temporary.")
    for what in ("a ^= b", "b ^= a", "a ^= b"):
        if what == "b ^= a":
            b ^= a
        else:
            a ^= b
        G.counts["xors"] += 1
        G.grid = [_bits(a), _bits(b)]
        G.add(f"{what} → a = {a}, b = {b}.", 0 if what.startswith("a") else 1, None)
    return G.result("swap_xor", [a, b], ["a", "b"], BIT_COLS)


def _divide_bits(a, b):
    G = Grid(2, BITS)
    G.grid[0] = _bits(a)
    G.grid[1] = _bits(0)
    G.counts = {"subtractions": 0}
    q, rem = 0, a
    G.add(f"Divide {a} by {b} with shifts: for each power of two from high to "
          f"low, if b·2^k still fits in what remains, subtract it and set bit k "
          f"of the quotient.")
    for k in range(BITS - 1, -1, -1):
        if (b << k) <= rem:
            rem -= b << k
            q |= 1 << k
            G.counts["subtractions"] += 1
            G.grid[1] = _bits(q)
            G.add(f"{b}·2^{k} = {b << k} fits — subtract (remainder {rem}), set "
                  f"quotient bit {k}.", 1, BITS - 1 - k)
    G.add(f"{a} ÷ {b} = {q} remainder {rem}.")
    return G.result("divide_bits", q, [str(a), "quotient"], BIT_COLS)


def _f(n):
    return [n, 1, n + 1, 0][n % 4]


def _xor_range(l, r):
    G = Grid(2, 4)
    G.grid = [[r, 1, r + 1, 0], [l - 1, 1, l, 0]] if l > 0 else [[r, 1, r + 1, 0], [0] * 4]
    G.counts = {"operations": 3}
    G.add("XOR of 1..n repeats with period 4: it is n, 1, n+1, 0 when n % 4 is "
          "0, 1, 2, 3 — no loop needed.")
    G.add(f"f({r}): {r} % 4 = {r % 4} → {_f(r)}.", 0, r % 4)
    if l <= 1:
        G.add(f"The range starts at {l}, so the answer is just f({r}) = {_f(r)}.")
        return G.result("xor_range", _f(r), [f"f({r})", "—"], ["0", "1", "2", "3"])
    G.add(f"f({l - 1}): {l - 1} % 4 = {(l - 1) % 4} → {_f(l - 1)}.", 1, (l - 1) % 4)
    res = _f(r) ^ _f(l - 1)
    G.add(f"XOR of {l}..{r} = f({r}) ^ f({l - 1}) = {_f(r)} ^ {_f(l - 1)} = {res} "
          f"(1..{l - 1} cancels out).")
    return G.result("xor_range", res, [f"f({r})", f"f({l - 1})"], ["0", "1", "2", "3"])


def _single_number_iii(a):
    x = 0
    for v in a:
        x ^= v
    low = x & -x
    G = Grid(1, len(a))
    G.grid[0] = list(a)
    G.counts = {"xors": len(a)}
    G.add(f"XOR of everything = {x} = (first unique) ^ (second unique). Its "
          f"lowest set bit ({low}) differs between them, so split the array by "
          f"that bit and XOR each group.")
    g1 = g2 = 0
    for i, v in enumerate(a):
        if v & low:
            g1 ^= v
        else:
            g2 ^= v
        G.add(f"{v} goes to group {'A' if v & low else 'B'}.", 0, i, match=bool(v & low))
    res = sorted([g1, g2])
    G.add(f"The two numbers that appear once: {res}.",
          path=[(0, j) for j, v in enumerate(a) if v in res])
    return G.result("single_number_iii", res, ["array"])
