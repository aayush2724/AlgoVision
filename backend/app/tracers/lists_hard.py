"""Hard linked-list problems (Steps 6, 11) on the `list` view. A second kind
of pointer (random / next-column) is drawn dashed via the step's
`aux_links`, labelled by `aux_label`.

* clone_random_list — weave a copy after every node, point each copy's
  random at its original's random.next, then unweave the two lists. O(1)
  extra space.
* flatten_list — columns hang down `child` pointers (solid), their heads are
  joined by `next` (dashed). Merge columns from the right, like merging two
  sorted lists, until one sorted chain remains.
* merge_k_lists — keep the current head of every list in a min-heap; pop
  the smallest, link it to the result, push its successor.
"""

import heapq

TITLES = {
    "clone_random_list": "Clone a Linked List With Random Pointers",
    "flatten_list": "Flatten a Linked List (sorted columns)",
    "merge_k_lists": "Merge K Sorted Lists",
}


def _nums(text, lo=1, n=8):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (lo <= len(a) <= n) or any(abs(v) > 99 for v in a):
        raise ValueError(f"Each list needs {lo}–{n} values within ±99.")
    return a


def _groups(text, k_max=4):
    groups = [_nums(p, 1, 5) for p in (text or "").split("|")]
    if not (2 <= len(groups) <= k_max) or sum(map(len, groups)) > 14:
        raise ValueError(f"Give 2–{k_max} sorted lists separated by '|', 14 nodes at most.")
    if any(g != sorted(g) for g in groups):
        raise ValueError("Every list must be sorted.")
    return groups


def run(algo, text, target=None):
    if algo == "clone_random_list":
        if "|" not in (text or ""):
            raise ValueError("Give 'values | random indices' (−1 = null), e.g. "
                             "7,13,11,10,1 | -1,0,4,2,0.")
        v, r = text.split("|", 1)
        vals, rnd = _nums(v, 1, 6), _nums(r, 1, 6)
        if len(rnd) != len(vals) or any(not (-1 <= x < len(vals)) for x in rnd):
            raise ValueError("One random index per node, each −1 or a valid index.")
        return _clone(vals, rnd)
    groups = _groups(text)
    return (_flatten if algo == "flatten_list" else _merge_k)(groups)


class _Steps:
    def __init__(self, aux_label=None):
        self.steps, self.counts, self.aux_label = [], {}, aux_label

    def add(self, note, values, nxt, curr=None, pointers=(), aux=None):
        s = {"values": list(values), "next": list(nxt), "curr": curr,
             "removed": [], "pointers": [list(p) for p in pointers],
             "counts": dict(self.counts)}
        if aux is not None:
            s["aux_links"] = list(aux)
            s["aux_label"] = self.aux_label
        self.steps.append({"i": len(self.steps), "line": 0, "structures": s,
                           "highlight": {"index": curr}, "note": note})


def _chain(nxt, head, values):
    out, j = [], head
    while j is not None and len(out) <= len(values):
        out.append(values[j])
        j = nxt[j]
    return out


def _result(algo, values, steps, res):
    return {"meta": {"algorithm": algo, "view": "list", "language": "python",
                     "result": res},
            "array": values, "steps": steps}


def _clone(vals, rnd):
    n = len(vals)
    S = _Steps("SOLID = NEXT · DASHED = RANDOM")
    S.counts = {"copies": 0, "randoms_set": 0}
    # Stable ids: original i is 2i, its copy 2i + 1. Only created ids show.
    labels = [x for v in vals for x in (v, f"{v}'")]
    nxt = [None] * (2 * n)
    aux = [None] * (2 * n)
    for i in range(n):
        nxt[2 * i] = 2 * i + 2 if i < n - 1 else None
        aux[2 * i] = 2 * rnd[i] if rnd[i] >= 0 else None
    shown = [2 * i for i in range(n)]

    def add(note, cur=None, ptrs=None):
        idx = {o: k for k, o in enumerate(shown)}
        S.add(note, [labels[o] for o in shown],
              [idx.get(nxt[o]) for o in shown], idx.get(cur),
              ptrs(idx) if ptrs else [("head", 0)],
              [idx.get(aux[o]) for o in shown])

    add("Copy the list without a hash map. Step 1: put each node's copy (′) "
        "right after it.", 0)
    for i in range(n):
        o, c = 2 * i, 2 * i + 1
        nxt[c] = nxt[o]
        nxt[o] = c
        shown = sorted(shown + [c])
        S.counts["copies"] += 1
        add(f"Insert {vals[i]}′ after {vals[i]}.", c)
    for i in range(n):
        if rnd[i] >= 0:
            aux[2 * i + 1] = aux[2 * i] + 1   # original.random.next = that copy
            S.counts["randoms_set"] += 1
            add(f"Step 2: {vals[i]}′.random = {vals[i]}.random.next = "
                f"{vals[rnd[i]]}′.", 2 * i + 1)
    for i in range(n):
        nxt[2 * i] = 2 * i + 2 if i < n - 1 else None
        nxt[2 * i + 1] = 2 * i + 3 if i < n - 1 else None
    add("Step 3: unweave — each original skips over its copy, each copy links "
        "to the next copy. Two separate lists with the same shape.", None,
        lambda idx: [("head", idx[0]), ("copy", idx[1])])
    # Read the answer back off the copy list's own pointers.
    copies, j = [], 1
    while j is not None:
        copies.append(j)
        j = nxt[j]
    pos = {c: k for k, c in enumerate(copies)}
    res = {"values": [int(labels[c][:-1]) for c in copies],
           "random": [pos[aux[c]] if aux[c] is not None else -1 for c in copies]}
    return _result("clone_random_list", labels, S.steps, res)


def _layout(groups):
    values, starts = [], []
    for g in groups:
        starts.append(len(values))
        values += g
    return values, starts


def _flatten(groups):
    values, starts = _layout(groups)
    N = len(values)
    child = [None] * N                     # drawn solid (next lane)
    for gi, g in enumerate(groups):
        for k in range(len(g) - 1):
            child[starts[gi] + k] = starts[gi] + k + 1

    def across(upto, acc):
        """Dashed head links for the columns not merged yet."""
        right = [None] * N
        for c in range(upto - 1):
            right[starts[c]] = starts[c + 1]
        if upto > 0:
            right[starts[upto - 1]] = acc
        return right

    S = _Steps("SOLID = CHILD (down) · DASHED = NEXT (across)")
    S.counts = {"comparisons": 0, "merges": 0}
    S.add("Each column is a sorted list hanging from its head by child "
          "pointers; the heads are joined by next. Flatten from the right: "
          "merge the last two columns, then merge that into the one before …",
          values, child, 0, [("head", 0)], across(len(groups) - 1, starts[-1]))

    def merge(a, b):
        head = tail = None
        while a is not None and b is not None:
            S.counts["comparisons"] += 1
            if values[a] <= values[b]:
                pick, a = a, child[a]
            else:
                pick, b = b, child[b]
            if tail is None:
                head = pick
            else:
                child[tail] = pick
            tail = pick
        child[tail] = a if a is not None else b
        return head

    acc = starts[-1]
    for gi in range(len(groups) - 2, -1, -1):
        acc = merge(starts[gi], acc)
        S.counts["merges"] += 1
        S.add(f"Merge column {gi + 1} with everything to its right → "
              f"{_chain(child, acc, values)}.", values, child, acc,
              [("head", acc)], across(gi, acc))
    res = _chain(child, acc, values)
    S.add(f"One sorted chain: {res}.", values, child, acc, [("head", acc)], [None] * N)
    return _result("flatten_list", values, S.steps, res)


def _merge_k(groups):
    values, starts = _layout(groups)
    nxt = [None] * len(values)
    for gi, g in enumerate(groups):
        for k in range(len(g) - 1):
            nxt[starts[gi] + k] = starts[gi] + k + 1
    S = _Steps()
    S.counts = {"heap_pops": 0}
    heap = [(values[s], s) for s in starts]
    heapq.heapify(heap)
    S.add(f"{len(groups)} sorted lists. Put every head in a min-heap; the "
          f"smallest head is always the next node of the answer.", values, nxt,
          None, [(f"L{i + 1}", s) for i, s in enumerate(starts)])
    head = tail = None
    while heap:
        v, j = heapq.heappop(heap)
        S.counts["heap_pops"] += 1
        after = nxt[j]
        if tail is None:
            head = j
        else:
            nxt[tail] = j
        tail = j
        if after is not None:
            heapq.heappush(heap, (values[after], after))
        S.add(f"Pop {v} (smallest in the heap) and link it to the result"
              + (f"; push its successor {values[after]}." if after is not None
                 else "; its list is used up."),
              values, nxt, j, [("head", head), ("tail", tail)]
              + [("heap", i) for _, i in sorted(heap, key=lambda x: x[1])])
    res = _chain(nxt, head, values)
    S.add(f"Merged: {res}.", values, nxt, head, [("head", head)])
    return _result("merge_k_lists", values, S.steps, res)
