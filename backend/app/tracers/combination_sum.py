"""Combination Sum — pick candidates (reuse allowed) that add up to a target.

At each call: take the current candidate again (left — same index, smaller
remaining target) or move past it for good (right — next index). Taking is
only tried while the candidate still fits in what remains, which prunes the
tree. A leaf with remaining 0 is an answer; running out of candidates is a
dead end. Because we never go back to an earlier index, each combination is
produced once, in non-decreasing order.

Uses the `tree` view through RecTree: nodes show the numbers picked so far
and the candidate being considered ("22→3"; ∅ for none, ✗ for a dead end);
answers glow green. The tree must stay drawable, so inputs
whose tree would exceed MAX_NODES are rejected up front (see `tree_size`).
"""

from app.tracers.recursion_tree import RecTree

MAX_CANDIDATES = 4
MAX_TARGET = 12
MAX_NODES = 45


def tree_size(cands: list, target: int) -> int:
    def rec(i, rem):
        if rem == 0 or i == len(cands):
            return 1
        size = 1 + rec(i + 1, rem)
        if cands[i] <= rem:
            size += rec(i, rem - cands[i])
        return size
    return rec(0, target)


def _label(picked):
    return "".join(str(v) for v in picked) or "∅"


def trace(candidates: list, target: int):
    cands = sorted({int(c) for c in candidates})
    target = int(target)
    t = RecTree()
    counts = {"calls": 0, "answers": 0, "dead_ends": 0}
    out: list = []

    t.event(None, f"Candidates {cands}, target {target}, each usable any number "
                  f"of times. Left = take the current candidate again; right = "
                  f"move past it for good.", counts)

    def rec(i, rem, picked, parent, side):
        counts["calls"] += 1
        # "22→3" = picked 2,2 and now considering candidate 3. Without the
        # candidate, every "move on" child would repeat its parent's label.
        if rem == 0:
            label = _label(picked)
        elif i == len(cands):
            label = _label(picked) + "✗"
        else:
            label = f"{_label(picked)}→{cands[i]}"
        nid = t.node(label, parent, side)
        if rem == 0:
            counts["answers"] += 1
            out.append(list(picked))
            t.event(nid, f"{' + '.join(map(str, picked))} = {target} — an "
                         f"answer.", counts, good=True)
            return
        if i == len(cands):
            counts["dead_ends"] += 1
            t.event(nid, f"No candidates left and {rem} still to make — dead "
                         f"end, back up.", counts)
            return
        c = cands[i]
        fits = c <= rem
        t.event(nid, f"At {_label(picked)} with {rem} remaining, candidate {c}: "
                     + ("take it again (left) or move on (right)." if fits
                        else f"{c} > {rem}, so only moving on is possible."),
                counts)
        if fits:
            picked.append(c)
            rec(i, rem - c, picked, nid, "left")
            picked.pop()
        rec(i + 1, rem, picked, nid, "right")

    rec(0, target, [], None, "left")
    shown = "; ".join(" + ".join(map(str, p)) for p in out) or "none"
    t.event(None, f"{counts['answers']} combination(s): {shown}. "
                  f"{counts['calls']} calls, {counts['dead_ends']} dead ends.",
            counts)
    return {
        "meta": {"algorithm": "combination_sum", "view": "tree",
                 "language": "python", "result": out},
        "steps": t.steps(),
    }
