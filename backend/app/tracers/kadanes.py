MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    arr = list(array)
    n = len(arr)
    steps = []
    counts = {"steps": 0, "extensions": 0, "restarts": 0}

    def add(note, window=None, s=None, best=None, best_window=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"window": window, "sum": s, "best": best,
                           "best_window": best_window, "counts": dict(counts)},
            "highlight": {"index": window[1] if window else None},
            "note": note,
        })

    if not arr:
        add("An empty array has no subarray to maximize.")
        return _result(arr, steps)

    add(f"Find the contiguous run with the biggest sum. Kadane's rule at each "
        f"value: extend the current run, or cut losses and restart.")

    cur = arr[0]
    cur_start = 0
    best = cur
    best_window = [0, 0]
    counts["steps"] += 1
    add(f"Start the run at {_fmt(arr[0])} — best so far.",
        [0, 0], cur, best, list(best_window))

    for i in range(1, n):
        v = arr[i]
        counts["steps"] += 1
        if cur + v < v:
            cur = v
            cur_start = i
            counts["restarts"] += 1
            note = (f"The old run would drag {_fmt(v)} down — cut losses and "
                    f"restart here. Run sum: {_fmt(cur)}.")
        else:
            cur += v
            counts["extensions"] += 1
            note = f"Extend the run with {_fmt(v)} — run sum {_fmt(cur)}."
        window = [cur_start, i]
        if cur > best:
            best = cur
            best_window = list(window)
            note += " New best!"
        add(note, window, cur, best, list(best_window))

    add(f"Done — the best run is [{best_window[0]}..{best_window[1]}] with sum "
        f"{_fmt(best)}, found in one pass with {counts['restarts']} restart(s).",
        None, cur, best, list(best_window))
    return _result(arr, steps)


def _result(arr, steps):
    return {
        "meta": {"algorithm": "kadanes", "view": "array", "language": "python"},
        "array": arr,
        "steps": steps,
    }
