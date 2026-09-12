"""Next Greater Element — the monotonic stack pattern.

The naive answer is a nested loop, O(n²). The stack version touches each
index at most twice, so it is O(n): the trace makes that "pushed once, popped
once" accounting visible.
"""

MAX_ARRAY_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(array: list[float]):
    arr = list(array)
    n = len(arr)
    steps: list = []
    counts = {"pushes": 0, "pops": 0, "comparisons": 0}
    # result[i] = the first value to the right of i that is bigger; None = none
    result: list = [None] * n
    stack: list[int] = []

    def add(note, placed=None, resolved=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": list(arr),
                "placed": placed,
                "sorted_ranges": [[r, r] for r in resolved] if resolved else [],
                "stack": list(stack),
                "stack_values": [arr[s] for s in stack],
                "result": list(result),
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("An empty array has no elements to answer for.")
        return _result(arr, steps, result)

    add("For each value, find the first bigger value to its right. Keep a "
        "stack of indices still waiting for their answer — it stays in "
        "decreasing order, which is what makes this linear.")

    for i in range(n):
        v = arr[i]
        settled: list[int] = []
        while stack and arr[stack[-1]] < v:
            counts["comparisons"] += 1
            j = stack.pop()
            counts["pops"] += 1
            result[j] = v
            settled.append(j)
            add(f"{_fmt(v)} is bigger than the waiting {_fmt(arr[j])} at index "
                f"{j} — that one's answer is {_fmt(v)}. Pop it.",
                placed=i, resolved=list(settled))
        if stack:
            counts["comparisons"] += 1
        stack.append(i)
        counts["pushes"] += 1
        add(f"Index {i} ({_fmt(v)}) has no answer yet — push it and move on. "
            f"Waiting: {[_fmt(arr[s]) for s in stack]}.",
            placed=i, resolved=list(settled))

    if stack:
        left = ", ".join(f"{_fmt(arr[s])} (index {s})" for s in stack)
        add(f"Input exhausted — {left} never found anything bigger to the "
            f"right, so their answer is 'none'.")
    add(f"Done: {counts['pushes']} pushes and {counts['pops']} pops for {n} "
        f"values. Every index entered and left the stack at most once — that "
        f"is the O(n), versus O(n²) for the nested-loop version.")
    return _result(arr, steps, result)


def _result(arr, steps, result):
    return {
        "meta": {
            "algorithm": "next_greater_element",
            "view": "array",
            "language": "python",
            "result": result,
        },
        "array": arr,
        "steps": steps,
    }
