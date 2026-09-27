"""Number theory for competitive programming (batch 75) on the `grid` view.

* extended_gcd — Euclid downwards (a, b) → (b, a mod b); on the way back
  up, x = y', y = x' − ⌊a/b⌋·y' gives a·x + b·y = gcd.
* mod_inverse — a⁻¹ mod m exists iff gcd(a, m) = 1; it is the x of the
  extended Euclid.
* ncr_mod — nCr mod p (p prime = 1e9+7): n! / (r!(n−r)!) with the division
  done as multiplication by inverses (Fermat: x⁻¹ = x^(p−2)).
* euler_totient — φ(n) = n · Π(1 − 1/p) over the distinct primes of n.
* spf_sieve — sieve the SMALLEST prime factor of every number up to n; then
  factorising x is just repeated division by spf[x].
* crt — Chinese Remainder: merge x ≡ r1 (mod m1) and x ≡ r2 (mod m2) into
  one congruence mod lcm(m1, m2), one pair at a time.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "extended_gcd": "Extended Euclidean Algorithm",
    "mod_inverse": "Modular Multiplicative Inverse",
    "ncr_mod": "nCr mod p (Fermat Inverse)",
    "euler_totient": "Euler's Totient Function",
    "spf_sieve": "Smallest Prime Factor Sieve",
    "crt": "Chinese Remainder Theorem",
}
P = 10 ** 9 + 7
EXT_COLS = ["a", "b", "⌊a/b⌋", "x", "y"]


def _pair(text, lo, hi, what):
    try:
        a, b = (int(x) for x in (text or "").replace(" ", "").split(","))
    except ValueError:
        raise ValueError(f"Give two numbers: {what}.") from None
    if not (lo <= a <= hi and lo <= b <= hi):
        raise ValueError(f"Keep both within {lo}–{hi}.")
    return a, b


def _one(text, lo, hi):
    try:
        n = int((text or "").strip())
    except ValueError:
        raise ValueError(f"Give a whole number {lo}–{hi}.") from None
    if not (lo <= n <= hi):
        raise ValueError(f"Give a whole number {lo}–{hi}.")
    return n


def run(algo, text, target=None):
    if algo == "extended_gcd":
        a, b = _pair(text, 0, 9999, "a, b")
        if a == b == 0:
            raise ValueError("gcd(0, 0) is undefined.")
        return _ext(a, b)
    if algo == "mod_inverse":
        a, m = _pair(text, 1, 9999, "a, m")
        if m < 2:
            raise ValueError("m must be at least 2.")
        return _ext(a, m, m)
    if algo == "ncr_mod":
        n, r = _pair(text, 0, 20, "n, r")
        if r > n:
            raise ValueError("Need r ≤ n.")
        return _ncr(n, r)
    if algo == "euler_totient":
        return _phi(_one(text, 1, 10 ** 9))
    if algo == "spf_sieve":
        n = _one(text, 2, 60)
        if target is None or target != int(target) or not (2 <= target <= n):
            raise ValueError(f"x to factorise must be 2–{n}.")
        return _spf(n, int(target))
    pairs = []
    for part in [p.strip() for p in (text or "").split(",") if p.strip()]:
        try:
            r, m = (int(v) for v in part.split())
        except ValueError:
            raise ValueError("Give congruences 'r m', e.g. 2 3, 3 5, 2 7.") from None
        if not (2 <= m <= 99 and 0 <= r < m):
            raise ValueError("Each modulus 2–99, with 0 ≤ r < m.")
        pairs.append((r, m))
    if not (2 <= len(pairs) <= 4):
        raise ValueError("Give 2–4 congruences.")
    return _crt(pairs)


def _egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = _egcd(b, a % b)
    return g, y, x - (a // b) * y


def _ext(a, b, m=None):
    """Extended Euclid as a table; with m set, finish as a modular inverse."""
    rows = []
    x, y = a, b
    while True:
        rows.append([x, y, x // y if y else None, None, None])
        if y == 0:
            break
        x, y = y, x % y
    G = Grid(len(rows), 5)
    G.counts = {"divisions": len(rows) - 1}
    G.grid = [r[:] for r in rows]
    G.add("Go down like Euclid: (a, b) → (b, a mod b) until b = 0. Then climb "
          "back up keeping a·x + b·y = gcd.", 0, 0,
          path=[(i, 0) for i in range(len(rows))])
    last = len(rows) - 1
    G.grid[last][3], G.grid[last][4] = 1, 0
    G.add(f"Bottom: b = 0, so gcd = {rows[last][0]} = {rows[last][0]}·1 + 0·0 → "
          f"x = 1, y = 0.", last, 3)
    xs, ys = 1, 0
    for i in range(last - 1, -1, -1):
        xs, ys = ys, xs - rows[i][2] * ys
        G.grid[i][3], G.grid[i][4] = xs, ys
        G.add(f"Row {i}: x = y below = {xs}, y = x below − ⌊{rows[i][0]}/{rows[i][1]}⌋"
              f"·y below = {ys}. Check: {rows[i][0]}·{xs} + {rows[i][1]}·{ys} = "
              f"{rows[i][0] * xs + rows[i][1] * ys}.", i, 3, [(i + 1, 3), (i + 1, 4)])
    g = rows[last][0]
    if m is None:
        G.add(f"gcd({a}, {b}) = {g} = {a}·{xs} + {b}·{ys}.", 0, 3,
              path=[(0, 3), (0, 4)])
        return G.result("extended_gcd", [g, xs, ys], None, EXT_COLS)
    if g != 1:
        G.add(f"gcd({a}, {m}) = {g} ≠ 1 — {a} has no inverse mod {m} (−1).",
              match=False)
        return G.result("mod_inverse", -1, None, EXT_COLS)
    inv = xs % m
    G.add(f"{a}·{xs} + {m}·{ys} = 1, so {a}·{xs} ≡ 1 (mod {m}). Inverse = {xs} mod "
          f"{m} = {inv}. Check: {a}·{inv} mod {m} = {a * inv % m}.", 0, 3,
          path=[(0, 3)])
    return G.result("mod_inverse", inv, None, EXT_COLS)


def _ncr(n, r):
    G = Grid(2, n + 1)
    G.grid[0] = list(range(n + 1))
    G.counts = {"multiplications": 0}
    fact = [1] * (n + 1)
    G.grid[1][0] = 1
    G.add("nCr = n! / (r!·(n−r)!). Modulo a prime p we can't divide, but we can "
          "multiply by an inverse: x⁻¹ = x^(p−2) mod p (Fermat). First the "
          "factorials mod p.", 1, 0)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % P
        G.grid[1][i] = fact[i]
        G.counts["multiplications"] += 1
        G.add(f"{i}! = {i - 1}!·{i} = {fact[i]} (mod p).", 1, i, [(1, i - 1)])
    den = fact[r] * fact[n - r] % P
    inv = pow(den, P - 2, P)
    G.counts["multiplications"] += 60
    res = fact[n] * inv % P
    G.add(f"Denominator {r}!·{n - r}! = {den}; its inverse by fast power "
          f"{den}^(p−2) mod p = {inv} (about 60 squarings).", 1, r,
          [(1, r), (1, n - r)])
    G.add(f"{n}C{r} = {fact[n]} · {inv} mod p = {res}.", 1, n, path=[(1, n)])
    return G.result("ncr_mod", res, ["i", "i! mod p"])


def _phi(n):
    primes, x, p = [], n, 2
    while p * p <= x:
        if x % p == 0:
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            primes.append((p, e))
        p += 1
    if x > 1:
        primes.append((x, 1))
    G = Grid(max(1, len(primes)), 3)
    G.counts = {"trial_divisions": p - 2}
    cols = ["prime", "exponent", "φ so far"]
    G.add(f"φ({n}) counts 1..{n} coprime to {n}. Factor n by trial division up "
          f"to √n; each distinct prime p removes the multiples of p: φ ← φ·(1 − 1/p).")
    if not primes:
        G.add("n = 1: φ(1) = 1.")
        return G.result("euler_totient", 1, None, cols)
    phi = n
    for i, (p, e) in enumerate(primes):
        phi = phi // p * (p - 1)
        G.grid[i] = [p, e, phi]
        G.add(f"Prime {p} (appears {e}×): φ = φ / {p} · {p - 1} = {phi}.", i, 2)
    G.add(f"φ({n}) = {phi}.", path=[(len(primes) - 1, 2)])
    return G.result("euler_totient", phi, [f"p{i + 1}" for i in range(len(primes))], cols)


def _spf(n, x):
    nums = list(range(2, n + 1))
    spf = {v: 0 for v in nums}
    G = Grid(2, len(nums))
    G.grid[0] = nums[:]
    G.counts = {"marks": 0}
    G.add(f"spf[v] = smallest prime dividing v. Sweep i = 2, 3, …; if i is still "
          f"unmarked it is prime, and it becomes the spf of every unmarked "
          f"multiple from i² on.")
    for i in nums:
        if spf[i]:
            continue
        spf[i] = i
        marked = [i]
        for j in range(i * i, n + 1, i):
            if not spf[j]:
                spf[j] = i
                marked.append(j)
                G.counts["marks"] += 1
        G.grid[1] = [spf[v] or None for v in nums]
        G.add(f"{i} is prime: spf[{i}] = {i}"
              + (f", and it marks {marked[1:]}." if len(marked) > 1 else "."),
              1, i - 2, [], [(1, v - 2) for v in marked])
    fac, v = [], x
    while v > 1:
        fac.append(spf[v])
        G.add(f"Factorise {x}: spf[{v}] = {spf[v]} → divide → {v // spf[v]}.",
              1, v - 2, [(0, v - 2)])
        v //= spf[v]
    G.add(f"{x} = {' × '.join(map(str, fac))} — O(log x) per query after the sieve.",
          path=[(0, x - 2)])
    return G.result("spf_sieve", fac, ["n", "spf"])


def _crt(pairs):
    G = Grid(len(pairs), 3)
    G.grid = [[r, m, None] for r, m in pairs]
    G.counts = {"merges": 0}
    cols = ["r", "m", "merged"]
    G.add("Merge the congruences one at a time. x ≡ r1 (mod m1) means x = r1 + "
          "m1·t; plug into x ≡ r2 (mod m2) and solve for t with the extended "
          "Euclid. The merged modulus is lcm(m1, m2).")
    r, m = pairs[0]
    G.grid[0][2] = f"{r} mod {m}"
    for i in range(1, len(pairs)):
        r2, m2 = pairs[i]
        g, p, _ = _egcd(m, m2)
        if (r2 - r) % g:
            G.add(f"x ≡ {r} (mod {m}) and x ≡ {r2} (mod {m2}) disagree mod gcd = {g} "
                  f"— no solution (−1).", i, None, match=False)
            return G.result("crt", -1, None, cols)
        lcm = m // g * m2
        t = (r2 - r) // g * p % (m2 // g)
        r = (r + m * t) % lcm
        m = lcm
        G.counts["merges"] += 1
        G.grid[i][2] = f"{r} mod {m}"
        G.add(f"Merge with x ≡ {r2} (mod {m2}): t = {t}, so x ≡ {r} (mod {m}).",
              i, 2, [(i - 1, 2)])
    G.add(f"Smallest non-negative solution x = {r} (unique mod {m}).",
          path=[(len(pairs) - 1, 2)])
    return G.result("crt", [r, m], None, cols)
