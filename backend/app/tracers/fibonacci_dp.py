MAX_N = 18


def trace(n: int):
    n = int(n)
    memo: dict = {}
    steps = []
    call_stack: list = []
    counts = {"calls": 0, "cache_hits": 0, "computes": 0}

    def add(note, computing=None, cache_hit=False):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                # JSON object keys are strings — the frontend renders cells 0..n
                "table": {str(k): memo.get(k) for k in range(n + 1)},
                "computing": computing,
                "cache_hit": cache_hit,
                "stack": list(call_stack),
                "counts": dict(counts),
            },
            "highlight": {"index": computing},
            "note": note,
        })

    add(f"Compute fib({n}) — the vault starts empty.")

    def fib(k):
        counts["calls"] += 1
        if k in memo:
            counts["cache_hits"] += 1
            add(
                f"fib({k}) is already in the vault: {memo[k]}. No recomputation needed.",
                computing=k, cache_hit=True,
            )
            return memo[k]
        call_stack.append(k)
        if k <= 1:
            memo[k] = k
            counts["computes"] += 1
            add(f"Base case: fib({k}) = {k}. Stored in the vault.", computing=k)
            call_stack.pop()
            return k
        add(f"fib({k}) unknown — need fib({k - 1}) and fib({k - 2}) first.", computing=k)
        v = fib(k - 1) + fib(k - 2)
        memo[k] = v
        counts["computes"] += 1
        call_stack.pop()
        add(f"fib({k}) = fib({k - 1}) + fib({k - 2}) = {v}. Stored in the vault.", computing=k)
        return v

    result = fib(n)
    add(
        f"Vault complete — fib({n}) = {result}. {counts['cache_hits']} cache hits "
        f"saved {counts['cache_hits']} recomputations.",
    )

    return {
        "meta": {
            "algorithm": "fibonacci_dp",
            "view": "table",
            "language": "python",
            "n": n,
            "result": result,
        },
        "steps": steps,
    }
