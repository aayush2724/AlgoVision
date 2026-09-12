"""Sieve of Eratosthenes — find every prime up to n by crossing out.

The two details students usually miss are both visible here: multiples start
at p², not 2p, and the outer loop can stop at √n. The counters make the
saving concrete.
"""

MIN_N = 10
MAX_N = 50


def trace(n: int):
    # is_prime[i] for 0..n; index 0 and 1 are not primes.
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    if n >= 1:
        is_prime[1] = False
    steps: list = []
    counts = {"primes_found": 0, "crossings": 0, "skipped_as_done": 0}

    def shown():
        # 1 = still standing (prime), 0 = crossed out
        return [1 if is_prime[i] else 0 for i in range(n + 1)]

    def add(note, placed=None, marked=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": shown(),
                "placed": placed,
                "sorted_ranges": [[m, m] for m in (marked or [])],
                "numbers": list(range(n + 1)),
                "primes": [i for i, p in enumerate(is_prime) if p],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    limit = int(n ** 0.5)
    add(f"Every number from 0 to {n} starts as a candidate. Cross out 0 and 1 "
        f"— neither is prime. Then repeatedly take the smallest survivor and "
        f"cross out its multiples. The outer loop only needs to reach √{n} ≈ "
        f"{limit}.")

    for p in range(2, n + 1):
        if not is_prime[p]:
            continue
        counts["primes_found"] += 1
        if p > limit:
            counts["skipped_as_done"] += 1
            add(f"{p} survived every earlier crossing-out, so it is prime. "
                f"Past √{n} there is nothing left to cross: any multiple of "
                f"{p} would need a smaller factor, and those are all gone.",
                placed=p)
            continue
        add(f"{p} is still standing — it is prime. Now remove its multiples.",
            placed=p)
        marked = []
        # Start at p*p: every smaller multiple already has a smaller factor.
        for m in range(p * p, n + 1, p):
            if is_prime[m]:
                is_prime[m] = False
                counts["crossings"] += 1
                marked.append(m)
        if marked:
            add(f"Cross out {', '.join(str(m) for m in marked)} — each is "
                f"{p} times something. Starting at {p}² = {p * p} is safe "
                f"because anything smaller was already removed by a smaller "
                f"prime.", placed=p, marked=marked)
        else:
            add(f"Every multiple of {p} up to {n} was already crossed out by "
                f"a smaller prime.", placed=p)

    primes = [i for i, prime in enumerate(is_prime) if prime]
    add(f"{len(primes)} primes up to {n}: {', '.join(str(p) for p in primes)}. "
        f"Total crossings: {counts['crossings']} — testing each number for "
        f"divisibility separately would cost far more.")

    return {
        "meta": {
            "algorithm": "sieve",
            "view": "array",
            "language": "python",
            "n": n,
            "primes": primes,
        },
        "array": list(range(n + 1)),
        "steps": steps,
    }
