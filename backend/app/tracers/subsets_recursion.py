"""Subsets by recursion — take it or leave it, drawn as the recursion tree.

For each element the recursion branches twice: include it (left) or skip it
(right). After n decisions every root-to-leaf path is one subset, so there are
exactly 2ⁿ leaves — the power set. The same tree answers the subsequence-sum
questions: with a target K, the leaves whose sum is K are the answers (count
them, or stop at the first to ask "does one exist?").

Uses the `tree` view through RecTree: each node is labelled with the elements
picked so far (∅ for none); answer leaves glow green.
"""

from app.tracers.recursion_tree import RecTree

MAX_LEN = 4


def _label(picked):
    return "".join(str(v) for v in picked) or "∅"


def trace(array: list, k: int | None = None):
    arr = [int(v) for v in array]
    t = RecTree()
    counts = {"calls": 0, "subsets": 0, "matches": 0}
    subsets: list = []
    sums: list = []

    goal = (f" A leaf is an answer when its sum is {k}." if k is not None
            else " Every leaf is one subset.")
    t.event(None, f"Build every subset of {arr}: at each element, branch "
                  f"left to take it, right to skip it.{goal}", counts)

    def rec(i, picked, parent, side):
        counts["calls"] += 1
        nid = t.node(_label(picked), parent, side)
        if i == len(arr):
            counts["subsets"] += 1
            s = sum(picked)
            subsets.append(list(picked))
            sums.append(s)
            hit = k is None or s == k
            if k is not None and hit:
                counts["matches"] += 1
            what = (f"{{{', '.join(map(str, picked))}}}" if picked else "the empty set")
            if k is None:
                note = f"All {len(arr)} decisions made — leaf: {what}, sum {s}."
            else:
                note = (f"Leaf {what}: sum {s} {'= K — an answer!' if hit else f'≠ {k}.'}")
            t.event(nid, note, counts, good=hit)
            return
        v = arr[i]
        t.event(nid, f"At {_label(picked)}: decide element {v} — take it "
                     f"(left) or skip it (right).", counts)
        picked.append(v)
        rec(i + 1, picked, nid, "left")
        picked.pop()
        rec(i + 1, picked, nid, "right")

    rec(0, [], None, "left")
    if k is None:
        t.event(None, f"{counts['subsets']} leaves = 2^{len(arr)} subsets — the "
                      f"power set. Subset sums: {sorted(sums)}.", counts)
    else:
        t.event(None, f"{counts['matches']} subsequence(s) sum to {k} "
                      f"({'so one exists' if counts['matches'] else 'none exists'}). "
                      f"The tree has 2^{len(arr)} leaves — exponential, which is "
                      f"why sums this small are needed.", counts)
    return {
        "meta": {"algorithm": "subsets_recursion", "view": "tree",
                 "language": "python", "result": subsets, "sums": sums,
                 "matches": counts["matches"] if k is not None else None},
        "steps": t.steps(),
    }
