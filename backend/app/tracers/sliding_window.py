MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float], k: int):
    arr = list(array)
    n = len(arr)
    k = int(k)
    steps = []
    counts = {"additions": 0, "windows": 0}

    def add(note, window=None, s=None, best=None, best_window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"window": window, "sum": s, "best": best,
                           "best_window": best_window, "counts": dict(counts)},
            "highlight": {"index": window[1] if window else None},
            "note": note,
        })

    add(f"Find the size-{k} window with the biggest sum. The trick: never "
        f"re-add the whole window — drop one value, add one value.")

    cur = sum(arr[:k])
    counts["additions"] += k
    counts["windows"] += 1
    best = cur
    best_window = [0, k - 1]
    add(f"First window [0..{k - 1}] sums to {_fmt(cur)} — the best so far.",
        [0, k - 1], cur, best, list(best_window))

    for i in range(k, n):
        out_v, in_v = arr[i - k], arr[i]
        cur = cur - out_v + in_v
        counts["additions"] += 1
        counts["windows"] += 1
        window = [i - k + 1, i]
        if cur > best:
            best = cur
            best_window = list(window)
            add(f"Slide: drop {_fmt(out_v)}, add {_fmt(in_v)} — sum {_fmt(cur)}. "
                f"New best!", window, cur, best, list(best_window))
        else:
            add(f"Slide: drop {_fmt(out_v)}, add {_fmt(in_v)} — sum {_fmt(cur)}. "
                f"Best stays {_fmt(best)}.", window, cur, best, list(best_window))

    naive = (n - k + 1) * k
    add(f"Done — best window [{best_window[0]}..{best_window[1]}] sums to "
        f"{_fmt(best)}. {counts['additions']} additions instead of the naive "
        f"{naive} — that's O(n) vs O(n·k).",
        None, cur, best, list(best_window))
    return _result(arr, k, steps)


def _result(arr, k, steps):
    return {
        "meta": {"algorithm": "sliding_window", "view": "array",
                 "language": "python", "k": k},
        "array": arr,
        "steps": steps,
    }
