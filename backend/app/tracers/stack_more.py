"""More monotonic-stack classics — each keeps a stack of indices whose answer
is still pending, and resolves them as soon as the current value decides it.

* next_smaller — the first smaller value to the right (mirror of next greater).
* nge_circular — next greater, but the array wraps around: sweep twice; the
  second lap only resolves, it never pushes.
* remove_k_digits — the smallest number after deleting k digits: while the
  kept digit on top is bigger than the incoming one (and deletions remain),
  delete it. Leftover deletions come off the end; leading zeros are dropped.
* sum_subarray_mins — each value is the minimum of left·right subarrays,
  where left/right are its distances to the previous smaller (strict) and
  next smaller-or-equal value. Two stack passes find both; the sum of
  value·left·right is the answer.

Reuses the `array` view: the current index is `placed`, resolved (or kept)
indices are green via `sorted_ranges`, and the span a value is minimum of is
the orange `merging` range.
"""

TITLES = {
    "next_smaller": "Next Smaller Element",
    "nge_circular": "Next Greater Element II (Circular)",
    "remove_k_digits": "Remove K Digits",
    "sum_subarray_mins": "Sum of Subarray Minimums",
}
MAX_LEN = 12


def _f(v):
    return f"{v:g}"


def validate(algo, arr, target):
    if not arr or len(arr) > MAX_LEN:
        return f"Give 1–{MAX_LEN} numbers."
    if algo == "remove_k_digits":
        if any(v != int(v) or not (0 <= v <= 9) for v in arr):
            return "Digits 0–9 only."
        if target is None or target != int(target) or not (0 <= target <= len(arr)):
            return f"K must be 0–{len(arr)}."
    if algo == "sum_subarray_mins" and any(v != int(v) or v < 0 or v > 100 for v in arr):
        return "Whole numbers 0–100."
    return None


def trace(algo, array, target=None):
    arr = list(array)
    steps: list = []
    counts = {"pushes": 0, "pops": 0}

    def add(note, placed=None, green=(), span=None):
        steps.append({"i": len(steps), "line": 0,
                      "structures": {"array": arr[:], "placed": placed,
                                     "sorted_ranges": [[j, j] for j in green],
                                     "merging": list(span) if span else None,
                                     "counts": dict(counts)},
                      "highlight": {"index": placed}, "note": note})

    n = len(arr)
    if algo in ("next_smaller", "nge_circular"):
        smaller = algo == "next_smaller"
        res = [None] * n
        stack: list = []
        resolved: list = []
        word = "smaller" if smaller else "bigger"
        add(f"For each value, find the first {word} one to its right"
            + ("." if smaller else " — wrapping around past the end.")
            + " A stack holds the indices still waiting.")
        for i in range((1 if smaller else 2) * n):
            j = i % n
            v = arr[j]
            while stack and (arr[stack[-1]] > v if smaller else arr[stack[-1]] < v):
                t = stack.pop()
                counts["pops"] += 1
                res[t] = v
                resolved.append(t)
                add(f"{_f(v)} (index {j}{', 2nd lap' if i >= n else ''}) is "
                    f"{word} than waiting {_f(arr[t])} at index {t} — that is "
                    f"its answer. Pop.", j, resolved)
            if i < n:
                stack.append(j)
                counts["pushes"] += 1
                add(f"Push index {j} ({_f(v)}). Waiting: "
                    f"{[_f(arr[s]) for s in stack]}.", j, resolved)
            elif not stack:
                break
        add(f"Answers: {[('—' if r is None else _f(r)) for r in res]} "
            f"('—' = none). Every index was pushed once and popped at most "
            f"once — O(n){'' if smaller else ', even with two laps'}.",
            None, resolved)
        result = res
    elif algo == "remove_k_digits":
        k = int(target)
        left = k
        stack: list = []
        add(f"Delete {k} digit(s) to make the smallest number. Keep a stack of "
            f"kept digits; a bigger kept digit before a smaller one should go.")
        for i, d in enumerate(arr):
            while left and stack and arr[stack[-1]] > d:
                t = stack.pop()
                counts["pops"] += 1
                left -= 1
                add(f"Digit {_f(d)} is smaller than kept {_f(arr[t])} (index "
                    f"{t}) — delete that one ({left} deletion(s) left).", i, stack)
            stack.append(i)
            counts["pushes"] += 1
            add(f"Keep digit {_f(d)} (index {i}).", i, stack)
        while left:
            t = stack.pop()
            left -= 1
            add(f"Deletions left over — drop the last kept digit ({_f(arr[t])}).",
                None, stack)
        kept = "".join(str(int(arr[j])) for j in stack)
        s = kept.lstrip("0") or "0"
        add(f"Kept digits read {kept or '(none)'}; without leading zeros that "
            f"is {s}.", None, stack)
        result = s
    else:
        prev_smaller = [-1] * n
        next_smaller = [n] * n
        stack: list = []
        add("Each value is the minimum of every subarray that stretches left "
            "until a strictly smaller value and right until a smaller-or-equal "
            "one. Pass 1 finds the previous smaller values.")
        for i, v in enumerate(arr):
            while stack and arr[stack[-1]] >= v:
                stack.pop()
                counts["pops"] += 1
            prev_smaller[i] = stack[-1] if stack else -1
            stack.append(i)
            counts["pushes"] += 1
            add(f"Previous smaller of {_f(v)} (index {i}): "
                + (f"index {prev_smaller[i]} ({_f(arr[prev_smaller[i]])})."
                   if prev_smaller[i] >= 0 else "none — it reaches the start."), i)
        stack = []
        add("Pass 2, right to left: the next smaller-or-equal values.")
        for i in range(n - 1, -1, -1):
            v = arr[i]
            while stack and arr[stack[-1]] > v:
                stack.pop()
                counts["pops"] += 1
            next_smaller[i] = stack[-1] if stack else n
            stack.append(i)
            counts["pushes"] += 1
            add(f"Next smaller-or-equal of {_f(v)} (index {i}): "
                + (f"index {next_smaller[i]} ({_f(arr[next_smaller[i]])})."
                   if next_smaller[i] < n else "none — it reaches the end."), i)
        total = 0
        done: list = []
        for i, v in enumerate(arr):
            left = i - prev_smaller[i]
            right = next_smaller[i] - i
            total += v * left * right
            done.append(i)
            add(f"{_f(v)} is the minimum of {left} × {right} = {left * right} "
                f"subarrays (indices {prev_smaller[i] + 1}..{next_smaller[i] - 1}) "
                f"→ adds {_f(v * left * right)}. Running total {_f(total)}.",
                i, done, (prev_smaller[i] + 1, next_smaller[i] - 1))
        add(f"Sum of subarray minimums: {_f(total)} — from two O(n) stack "
            f"passes instead of checking all {n * (n + 1) // 2} subarrays.",
            None, done)
        result = total
    return {"meta": {"algorithm": algo, "view": "array", "language": "python",
                     "result": result},
            "array": arr, "steps": steps}
