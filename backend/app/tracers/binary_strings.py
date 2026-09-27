"""Binary Strings Without Consecutive 1s — a recursion tree with one rule.

Grow the string a bit at a time: '0' can always follow, '1' only if the last
bit isn't already '1'. The forbidden branch is never built, so every leaf is a
valid string. The number of leaves follows the Fibonacci numbers (n = 1, 2, 3,
4 → 2, 3, 5, 8), which is exactly why this problem shows up next to them.

Uses the `tree` view through RecTree: '0' branches left, '1' branches right;
finished strings glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_N = 4


def trace(n: int):
    n = int(n)
    t = RecTree()
    counts = {"calls": 0, "pruned": 0, "results": 0}
    out: list = []

    t.event(None, f"Build every {n}-bit string with no two 1s in a row. '0' is "
                  f"always allowed; '1' only after a '0' (or at the start).",
            counts)

    def rec(s, parent, side):
        counts["calls"] += 1
        nid = t.node(s or "·", parent, side)
        if len(s) == n:
            counts["results"] += 1
            out.append(s)
            t.event(nid, f"{s} has {n} bits and no '11' — keep it.", counts,
                    good=True)
            return
        if s.endswith("1"):
            counts["pruned"] += 1
            t.event(nid, f"'{s}' ends in 1 — only '0' may follow; the '1' "
                         f"branch is pruned.", counts)
        else:
            t.event(nid, f"'{s or '(empty)'}' — both '0' and '1' may follow.",
                    counts)
        rec(s + "0", nid, "left")
        if not s.endswith("1"):
            rec(s + "1", nid, "right")

    rec("", None, "left")
    t.event(None, f"{counts['results']} valid strings: {', '.join(out)}. "
                  f"{counts['pruned']} branch(es) pruned. The counts grow like "
                  f"Fibonacci.", counts)
    return {
        "meta": {"algorithm": "binary_strings", "view": "tree",
                 "language": "python", "result": out},
        "steps": t.steps(),
    }
