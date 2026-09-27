"""Subsets II — every *distinct* subset of a list that has duplicates.

Sort first so equal values sit together. Each call loops over the elements it
may add next (index idx..n−1) and makes one child per choice — but among equal
values only the first is tried at a given level; the rest would recreate the
same subsets, so those branches are never built. Every node (not just the
leaves) is one subset, so the whole tree is the answer.

Uses the `tree` view through RecTree with n-ary children: every node glows
green because every node is a distinct subset.
"""

from app.tracers.recursion_tree import RecTree

MAX_LEN = 4


def _label(picked):
    return "".join(str(v) for v in picked) or "∅"


def trace(array: list):
    arr = sorted(int(v) for v in array)
    t = RecTree()
    counts = {"calls": 0, "skipped_duplicates": 0}
    out: list = []

    t.event(None, f"Sorted: {arr}. Each call adds one more element from its "
                  f"position onward. Equal values are only tried once per "
                  f"level — that is what removes duplicate subsets.", counts)

    def rec(idx, picked, parent):
        counts["calls"] += 1
        nid = t.node(_label(picked), parent, side=None)
        out.append(list(picked))
        dups = []
        for i in range(idx, len(arr)):
            if i > idx and arr[i] == arr[i - 1]:
                counts["skipped_duplicates"] += 1
                dups.append(str(arr[i]))
        extra = (f" Skipping another {', '.join(dups)} at this level — it "
                 f"would repeat a subset." if dups else "")
        t.event(nid, f"Subset {{{', '.join(map(str, picked))}}} recorded. "
                     f"Next, try adding each element from position {idx}."
                     + extra, counts, good=True)
        for i in range(idx, len(arr)):
            if i > idx and arr[i] == arr[i - 1]:
                continue
            picked.append(arr[i])
            rec(i + 1, picked, nid)
            picked.pop()

    rec(0, [], None)
    t.event(None, f"{len(out)} distinct subsets (every node). "
                  f"{counts['skipped_duplicates']} duplicate branch(es) never "
                  f"built — versus 2^{len(arr)} = {2 ** len(arr)} with repeats.",
            counts)
    return {
        "meta": {"algorithm": "subsets_ii", "view": "tree", "language": "python",
                 "result": out, "nodes": t.size()},
        "steps": t.steps(),
    }
