"""Combination Sum II — each candidate used at most once, no repeated answers.

Sort the candidates. Each call loops over what it may add next (position
idx onward): equal values are only tried once per level (so no duplicate
combinations), and because the list is sorted, the loop stops as soon as a
value is bigger than what remains. Reaching 0 exactly is an answer.

Uses the `tree` view through RecTree with n-ary children; nodes show the
numbers picked so far, answers glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_LEN = 6
MAX_TARGET = 15
MAX_NODES = 45


def _label(picked):
    return "".join(str(v) for v in picked) or "∅"


def trace(candidates: list, target: int):
    arr = sorted(int(v) for v in candidates)
    target = int(target)
    t = RecTree()
    counts = {"calls": 0, "answers": 0, "pruned": 0}
    out: list = []

    t.event(None, f"Sorted candidates {arr}, target {target}, each used at most "
                  f"once. A call adds one more candidate from its position "
                  f"onward; equal values once per level; stop when too big.",
            counts)

    def rec(idx, rem, picked, parent):
        counts["calls"] += 1
        nid = t.node(_label(picked), parent, side=None)
        if rem == 0:
            counts["answers"] += 1
            out.append(list(picked))
            t.event(nid, f"{' + '.join(map(str, picked))} = {target} — an "
                         f"answer.", counts, good=True)
            return
        stop = next((arr[i] for i in range(idx, len(arr)) if arr[i] > rem), None)
        if stop is not None:
            counts["pruned"] += 1
        t.event(nid, f"At {_label(picked)} with {rem} remaining: try each "
                     f"candidate from position {idx}."
                     + (f" {stop} > {rem}, and everything after it is bigger — "
                        f"the loop stops there." if stop is not None else ""),
                counts)
        for i in range(idx, len(arr)):
            if i > idx and arr[i] == arr[i - 1]:
                continue
            if arr[i] > rem:
                break
            picked.append(arr[i])
            rec(i + 1, rem - arr[i], picked, nid)
            picked.pop()

    rec(0, target, [], None)
    shown = "; ".join(" + ".join(map(str, p)) for p in out) or "none"
    t.event(None, f"{counts['answers']} combination(s): {shown}. "
                  f"{counts['calls']} calls.", counts)
    return {
        "meta": {"algorithm": "combination_sum_ii", "view": "tree",
                 "language": "python", "result": out, "nodes": t.size()},
        "steps": t.steps(),
    }
