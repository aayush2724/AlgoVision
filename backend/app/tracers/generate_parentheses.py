"""Generate Parentheses — backtracking where the rules prune the tree.

Build strings of n pairs one character at a time. Two rules keep every prefix
valid: add '(' only while fewer than n are open, add ')' only while it would
close something (close < open). Branches that break a rule are never made, so
the tree only contains valid prefixes and every leaf is a balanced string.
That pruning is the difference from generating all 2^(2n) strings and filtering.

Uses the `tree` view through RecTree: '(' branches left, ')' branches right;
the finished strings glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_N = 3


def trace(n: int):
    n = int(n)
    t = RecTree()
    counts = {"calls": 0, "pruned": 0, "results": 0}
    out: list = []

    t.event(None, f"Build every balanced string of {n} pair(s). Add '(' while "
                  f"open < {n}; add ')' only while close < open — so no "
                  f"invalid prefix is ever built.", counts)

    def rec(s, opened, closed, parent, side):
        counts["calls"] += 1
        nid = t.node(s or "·", parent, side)
        if len(s) == 2 * n:
            counts["results"] += 1
            out.append(s)
            t.event(nid, f"{s} uses all {n} pairs — a balanced string.",
                    counts, good=True)
            return
        blocked = []
        if opened == n:
            counts["pruned"] += 1
            blocked.append(f"no '(' — all {n} are open already")
        if closed == opened:
            counts["pruned"] += 1
            blocked.append("no ')' — nothing to close")
        t.event(nid, f"Prefix '{s or '(empty)'}' ({opened} open, {closed} "
                     f"closed)." + (f" Pruned: {'; '.join(blocked)}." if blocked
                                    else " Both moves are legal."), counts)
        if opened < n:
            rec(s + "(", opened + 1, closed, nid, "left")
        if closed < opened:
            rec(s + ")", opened, closed + 1, nid, "right")

    rec("", 0, 0, None, "left")
    t.event(None, f"{counts['results']} balanced strings: {', '.join(out)}. "
                  f"{counts['calls']} calls; {counts['pruned']} branches never "
                  f"built — versus 2^{2 * n} = {2 ** (2 * n)} raw strings.",
            counts)
    return {
        "meta": {"algorithm": "generate_parentheses", "view": "tree",
                 "language": "python", "result": out},
        "steps": t.steps(),
    }
