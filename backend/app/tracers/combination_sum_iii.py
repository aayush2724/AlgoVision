"""Combination Sum III — choose exactly k distinct digits 1–9 summing to n.

Each call loops over the next digit it may add (bigger than the last one, so
each combination comes out once, in increasing order). A branch dies early
when the digit exceeds what remains, or when k digits are already picked.
A node with exactly k digits and nothing remaining is an answer.

Uses the `tree` view through RecTree with n-ary children; answers glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_NODES = 45


def _label(picked):
    return "".join(str(v) for v in picked) or "∅"


def trace(k: int, n: int):
    k, n = int(k), int(n)
    t = RecTree()
    counts = {"calls": 0, "answers": 0}
    out: list = []

    t.event(None, f"Pick exactly {k} different digits from 1–9 that add up to "
                  f"{n}. Each call adds a digit bigger than the last, so no "
                  f"combination repeats.", counts)

    def rec(start, rem, picked, parent):
        counts["calls"] += 1
        nid = t.node(_label(picked), parent, side=None)
        if len(picked) == k:
            if rem == 0:
                counts["answers"] += 1
                out.append(list(picked))
                t.event(nid, f"{' + '.join(map(str, picked))} = {n} with "
                             f"{k} digits — an answer.", counts, good=True)
            else:
                t.event(nid, f"{k} digits picked but {rem} still remains — "
                             f"dead end.", counts)
            return
        t.event(nid, f"At {_label(picked)} with {rem} remaining: try digits "
                     f"{start}..9, stopping once a digit exceeds {rem}.",
                counts)
        for d in range(start, 10):
            if d > rem:
                break
            picked.append(d)
            rec(d + 1, rem - d, picked, nid)
            picked.pop()

    rec(1, n, [], None)
    shown = "; ".join(" + ".join(map(str, p)) for p in out) or "none"
    t.event(None, f"{counts['answers']} combination(s): {shown}. "
                  f"{counts['calls']} calls.", counts)
    return {
        "meta": {"algorithm": "combination_sum_iii", "view": "tree",
                 "language": "python", "result": out, "nodes": t.size()},
        "steps": t.steps(),
    }
