"""Stock Span — the monotonic stack, looking backwards this time.

A day's span is how many consecutive days (ending today) the price was at or
below today's price. The nested-loop answer walks back from every day, O(n²).
The stack keeps only the days that are still "taller than everything since" —
a day that today's price beats can never block a later day either, so it is
popped for good. Each day is pushed once and popped at most once: O(n).

Reuses the `array` view: today is the highlighted cell (`placed`), and the
span it covers lights green via `sorted_ranges`. No new renderer.
"""

MAX_LEN = 16


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(prices: list):
    arr = list(prices)
    n = len(arr)
    steps: list = []
    counts = {"pushes": 0, "pops": 0}
    spans: list = [None] * n
    stack: list[int] = []

    def add(note, placed=None, span_range=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "array": arr[:],
                "placed": placed,
                "sorted_ranges": [list(span_range)] if span_range else [],
                "stack": stack[:],
                "stack_values": [arr[s] for s in stack],
                "result": spans[:],
                "counts": dict(counts),
            },
            "highlight": {"index": placed},
            "note": note,
        })

    if n == 0:
        add("No prices, no spans.")
        return _result(arr, steps, spans)

    add("For each day, count the run of consecutive days (ending today) whose "
        "price was ≤ today's. A stack remembers only the earlier days that are "
        "still taller than everything after them.")

    for i, p in enumerate(arr):
        popped = []
        while stack and arr[stack[-1]] <= p:
            j = stack.pop()
            counts["pops"] += 1
            popped.append(_fmt(arr[j]))
        if popped:
            add(f"Day {i} ({_fmt(p)}) beats {', '.join(popped)} on the stack — "
                f"pop them. They can never block a later day, since today is "
                f"at least as tall.", placed=i)
        spans[i] = i - stack[-1] if stack else i + 1
        blocker = (f"the taller day {stack[-1]} ({_fmt(arr[stack[-1]])}) stops "
                   f"it" if stack else "nothing taller came before")
        stack.append(i)
        counts["pushes"] += 1
        add(f"Span of day {i} = {spans[i]} — {blocker}. Push day {i}. "
            f"Stack: {[_fmt(arr[s]) for s in stack]}.",
            placed=i, span_range=(i - spans[i] + 1, i))

    add(f"Spans: {spans}. {counts['pushes']} pushes and {counts['pops']} pops "
        f"for {n} days — each day entered and left the stack at most once, "
        f"so O(n) instead of walking back from every day.")
    return _result(arr, steps, spans)


def _result(arr, steps, spans):
    return {
        "meta": {
            "algorithm": "stock_span",
            "view": "array",
            "language": "python",
            "result": spans,
        },
        "array": arr,
        "steps": steps,
    }
