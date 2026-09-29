"""Basic Recursion (Beginner Problems) on the `grid` view: one row per call,
so the table grows downward as calls nest and fills its "returns" column as
they unwind. Reading the table top to bottom is the call stack; bottom to
top is the unwinding.

* sum_array_rec — sum(i) = a[i] + sum(i + 1); base sum(n) = 0.
* sum_digits_rec — f(n) = n % 10 + f(n // 10); base f(0) = 0.
* factorial_rec — f(n) = n · f(n − 1); base f(0) = 1.
* prime_rec — divisible(n, d): d·d > n → prime; n % d == 0 → not.
* sorted_rec — sorted(i): a[i] ≤ a[i + 1] and sorted(i + 1).
* reverse_array_rec / reverse_string_rec — swap(l, r) then recurse inward.
* palindrome_rec — s[l] == s[r] and check(l + 1, r − 1).
"""

from app.tracers.grid_common import Grid

TITLES = {
    "sum_array_rec": "Sum of Array Elements (Recursive)",
    "sum_digits_rec": "Sum of Digits (Recursive)",
    "factorial_rec": "Factorial (Recursive)",
    "prime_rec": "Check for a Prime Number (Recursive)",
    "sorted_rec": "Check if an Array is Sorted (Recursive)",
    "reverse_array_rec": "Reverse an Array (Recursive)",
    "reverse_string_rec": "Reverse a String (Recursive)",
    "palindrome_rec": "Check if a String is a Palindrome (Recursive)",
}
COLS = ["call", "work", "returns"]


def _int(text, lo, hi):
    try:
        v = int((text or "").strip())
    except ValueError:
        raise ValueError("Give a whole number.") from None
    if not (lo <= v <= hi):
        raise ValueError(f"Keep it between {lo} and {hi}.")
    return v


def _nums(text):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= 10) or any(abs(v) > 99 for v in a):
        raise ValueError("Give 1–10 numbers within ±99.")
    return a


def _word(text):
    s = (text or "").strip()
    if not (1 <= len(s) <= 12) or " " in s:
        raise ValueError("Give one word of 1–12 characters.")
    return s


def run(algo, text, target=None):
    if algo == "sum_digits_rec":
        return _sum_digits_rec(_int(text, 0, 99_999_999))
    if algo == "factorial_rec":
        return _factorial_rec(_int(text, 0, 10))
    if algo == "prime_rec":
        return _prime_rec(_int(text, 2, 9_999))
    if algo in ("reverse_string_rec", "palindrome_rec"):
        return globals()["_" + algo](_word(text))
    return globals()["_" + algo](_nums(text))


class Calls:
    """A growing call table: push a call (new row), later fill its return."""

    def __init__(self, depth_max):
        self.G = Grid(depth_max, 3)
        self.G.grid = [[None] * 3 for _ in range(depth_max)]
        self.G.counts = {"calls": 0, "depth": 0}
        self.n = 0

    def call(self, label, work, note):
        r = self.n
        self.n += 1
        self.G.grid[r][0], self.G.grid[r][1] = label, work
        self.G.counts["calls"] += 1
        self.G.counts["depth"] = max(self.G.counts["depth"], self.n)
        self.G.add(note, r, 0, deps=[(r, 1)])
        return r

    def ret(self, r, value, note, ok=True):
        self.G.grid[r][2] = value
        self.G.add(note, r, 2, deps=[(r, 1)], path=[(i, 2) for i in range(r, self.n)],
                   match=ok)

    def result(self, algo, res):
        self.G.grid = self.G.grid[:self.n]
        return self.G.result(algo, res, [f"depth {i}" for i in range(self.n)], COLS)


def _sum_array_rec(a):
    n = len(a)
    C = Calls(n + 1)
    C.G.add(f"sum(i) adds a[i] to the sum of everything after it. Array {a}.")
    rows = []
    for i in range(n):
        rows.append(C.call(f"sum({i})", f"a[{i}]={a[i]} + sum({i + 1})",
                           f"sum({i}) needs sum({i + 1}) first — call deeper."))
    base = C.call(f"sum({n})", "base case", f"i = {n} is past the end: return 0.")
    C.ret(base, 0, "Base case returns 0. Now unwind.")
    total = 0
    for i in range(n - 1, -1, -1):
        total += a[i]
        C.ret(rows[i], total, f"sum({i}) = {a[i]} + {total - a[i]} = {total}.")
    return C.result("sum_array_rec", total)


def _sum_digits_rec(n):
    C = Calls(len(str(n)) + 1)
    C.G.add(f"f(n) = n % 10 + f(n // 10), until n is 0.")
    rows, x = [], n
    while x:
        rows.append((x, C.call(f"f({x})", f"{x % 10} + f({x // 10})",
                               f"Peel {x % 10}; recurse on {x // 10}.")))
        x //= 10
    base = C.call("f(0)", "base case", "n = 0: no digits left, return 0.")
    C.ret(base, 0, "Base case returns 0. Unwind.")
    total = 0
    for x, r in reversed(rows):
        total += x % 10
        C.ret(r, total, f"f({x}) = {x % 10} + {total - x % 10} = {total}.")
    return C.result("sum_digits_rec", total)


def _factorial_rec(n):
    C = Calls(n + 1)
    C.G.add("f(n) = n · f(n − 1), with f(0) = 1.")
    rows = [C.call(f"f({k})", f"{k} · f({k - 1})", f"f({k}) waits for f({k - 1}).")
            for k in range(n, 0, -1)]
    base = C.call("f(0)", "base case", "f(0) = 1 by definition.")
    C.ret(base, 1, "Base case returns 1. Unwind.")
    val = 1
    for k, r in zip(range(1, n + 1), reversed(rows)):
        val *= k
        C.ret(r, val, f"f({k}) = {k} · {val // k} = {val}.")
    return C.result("factorial_rec", val)


def _prime_rec(n):
    C = Calls(int(n ** 0.5) + 3)
    C.G.add(f"isPrime({n}, d) tries divisor d; stop when d·d > {n}.")
    d, rows = 2, []
    while True:
        if d * d > n:
            r = C.call(f"p({n}, {d})", f"{d}² > {n}", f"d = {d}: d² = {d * d} > {n} — no divisor left to try.")
            rows.append(r)
            C.ret(r, True, "Base case: nothing up to √n divided it → prime.")
            for rr in reversed(rows[:-1]):
                C.ret(rr, True, "Pass the verdict back up.")
            return C.result("prime_rec", True)
        r = C.call(f"p({n}, {d})", f"{n} % {d} = {n % d}",
                   f"Does {d} divide {n}? {n} % {d} = {n % d}.")
        rows.append(r)
        if n % d == 0:
            C.ret(r, False, f"{d} divides {n} → not prime.", ok=False)
            for rr in reversed(rows[:-1]):
                C.ret(rr, False, "Pass the verdict back up.", ok=False)
            return C.result("prime_rec", False)
        d += 1


def _sorted_rec(a):
    n = len(a)
    C = Calls(n)
    C.G.add(f"sorted(i) checks a[i] ≤ a[i + 1], then asks sorted(i + 1). Array {a}.")
    rows = []
    for i in range(n - 1):
        r = C.call(f"sorted({i})", f"{a[i]} ≤ {a[i + 1]}?",
                   f"Compare a[{i}]={a[i]} with a[{i + 1}]={a[i + 1]}.")
        rows.append(r)
        if a[i] > a[i + 1]:
            C.ret(r, False, f"{a[i]} > {a[i + 1]} — out of order, return false.", ok=False)
            for rr in reversed(rows[:-1]):
                C.ret(rr, False, "false propagates up.", ok=False)
            return C.result("sorted_rec", False)
    base = C.call(f"sorted({n - 1})", "base case", "One element left — trivially sorted.")
    C.ret(base, True, "Base case returns true. Unwind.")
    for rr in reversed(rows):
        C.ret(rr, True, "Its pair was in order and the rest is sorted → true.")
    return C.result("sorted_rec", True)


def _reverse_seq(seq, algo):
    n = len(seq)
    cur = list(seq)
    G = Grid((n // 2) + 2, n)
    G.grid = [cur[:]] + [[None] * n for _ in range(n // 2 + 1)]
    G.counts = {"swaps": 0}
    G.add("Each call swaps the outer pair, then recurses on the inside. Row = one call.")
    l, r, row = 0, n - 1, 1
    while l < r:
        cur[l], cur[r] = cur[r], cur[l]
        G.grid[row] = cur[:]
        G.counts["swaps"] += 1
        G.add(f"rev({l}, {r}): swap positions {l} and {r}, then call rev({l + 1}, {r - 1}).",
              row, l, deps=[(row, r)], path=[(row, c) for c in range(l + 1)] + [(row, c) for c in range(r, n)])
        l, r, row = l + 1, r - 1, row + 1
    G.grid[row] = cur[:]
    G.add(f"rev({l}, {r}): pointers met — base case. Result {''.join(map(str, cur)) if algo == 'reverse_string_rec' else cur}.",
          row, None, path=[(row, c) for c in range(n)])
    G.grid = G.grid[:row + 1]
    res = "".join(cur) if algo == "reverse_string_rec" else cur
    return G.result(algo, res, ["input"] + [f"call {i}" for i in range(1, row + 1)])


def _reverse_array_rec(a):
    return _reverse_seq(a, "reverse_array_rec")


def _reverse_string_rec(s):
    return _reverse_seq(list(s), "reverse_string_rec")


def _palindrome_rec(s):
    n = len(s)
    C = Calls(n // 2 + 1)
    C.G.add(f"check(l, r): the ends must match, then check(l + 1, r − 1). Word '{s}'.")
    l, r, rows = 0, n - 1, []
    while l < r:
        row = C.call(f"check({l}, {r})", f"'{s[l]}' == '{s[r]}'?",
                     f"Compare s[{l}]='{s[l]}' with s[{r}]='{s[r]}'.")
        rows.append(row)
        if s[l] != s[r]:
            C.ret(row, False, f"'{s[l]}' ≠ '{s[r]}' → not a palindrome.", ok=False)
            for rr in reversed(rows[:-1]):
                C.ret(rr, False, "false propagates up.", ok=False)
            return C.result("palindrome_rec", False)
        l, r = l + 1, r - 1
    base = C.call(f"check({l}, {r})", "base case", "l ≥ r: nothing left to compare → true.")
    C.ret(base, True, "Base case returns true. Unwind.")
    for rr in reversed(rows):
        C.ret(rr, True, "Ends matched and the inside is a palindrome → true.")
    return C.result("palindrome_rec", True)
