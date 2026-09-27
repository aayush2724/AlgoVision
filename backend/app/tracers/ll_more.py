"""Linked-list problems (Step 6) on the `list` view — boxes are nodes, solid
arrows are `next`, dashed arrows are `prev` (doubly linked lists). Node
indices stay stable; a step may carry a different `values` list when a node
is created, and the view redraws its boxes.

Basics (batch 60): insert/delete the head of a singly or doubly linked list,
length, search, pairs with a given sum in a sorted DLL (two ends walking
inward), remove duplicates from a sorted DLL.

Medium/hard (batch 61): reverse recursively (the unwinding flips each
arrow), length of a loop (Floyd, then walk the ring once), sort 0s/1s/2s
(three chains, then join), sort a list (merge sort by relinking), Y-shaped
intersection (two pointers that swap heads so both walk a + b + c), reverse
in groups of k.
"""

TITLES = {
    "ll_insert_head": "Insert at the Head of a Linked List",
    "ll_delete_head": "Delete the Head of a Linked List",
    "ll_length": "Length of a Linked List",
    "ll_search": "Search in a Linked List",
    "dll_insert_head": "Insert Before the Head of a Doubly Linked List",
    "dll_delete_head": "Delete the Head of a Doubly Linked List",
    "dll_pairs_sum": "Pairs With a Given Sum in a Sorted DLL",
    "dll_remove_duplicates": "Remove Duplicates From a Sorted DLL",
    "ll_reverse_recursive": "Reverse a Linked List (Recursive)",
    "loop_length": "Length of a Loop in a Linked List",
    "sort_012_list": "Sort a Linked List of 0s, 1s and 2s",
    "sort_list": "Sort a Linked List (Merge Sort)",
    "y_intersection": "Intersection Point of a Y-Shaped Linked List",
    "reverse_k_group": "Reverse a Linked List in Groups of K",
}
NEEDS_T = {"ll_insert_head", "ll_search", "dll_insert_head", "dll_pairs_sum",
           "loop_length", "reverse_k_group"}
MAX = 10


def _nums(text, lo=1):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (lo <= len(a) <= MAX) or any(abs(v) > 99 for v in a):
        raise ValueError(f"Give {lo}–{MAX} values within ±99.")
    return a


def run(algo, text, target=None):
    if algo == "y_intersection":
        parts = (text or "").split("|")
        if len(parts) != 3:
            raise ValueError("Give 'A only | B only | shared', e.g. 1,2 | 9,8,7 | 4,5.")
        a, b, c = (_nums(p, 0) for p in parts)
        if not a and not c or not b and not c or len(a) + len(b) + len(c) > 12:
            raise ValueError("Both lists need at least one node; 12 nodes at most.")
        return _y(a, b, c)
    a = _nums(text)
    if algo in NEEDS_T and (target is None or target != int(target)):
        raise ValueError("Give a whole-number target.")
    t = int(target) if target is not None else None
    if algo in ("dll_pairs_sum", "dll_remove_duplicates") and a != sorted(a):
        raise ValueError("This DLL must be sorted.")
    if algo == "sort_012_list" and any(v not in (0, 1, 2) for v in a):
        raise ValueError("Only 0, 1 and 2.")
    if algo == "loop_length" and not (-1 <= t < len(a)):
        raise ValueError(f"The tail links back to index 0–{len(a) - 1}, or −1 for no loop.")
    if algo == "reverse_k_group" and not (1 <= t <= len(a)):
        raise ValueError(f"k must be 1–{len(a)}.")
    if algo in ("ll_insert_head", "dll_insert_head"):
        if abs(t) > 99 or len(a) >= MAX:
            raise ValueError(f"New value within ±99, and at most {MAX - 1} nodes before it.")
    fn = globals()["_" + algo]
    return fn(a, t) if algo in NEEDS_T else fn(a)


class L:
    def __init__(self, values, doubly=False):
        n = len(values)
        self.values = list(values)
        self.nxt = [i + 1 if i < n - 1 else None for i in range(n)]
        self.prv = [i - 1 if i else None for i in range(n)] if doubly else None
        self.removed: list = []
        self.ptr: dict = {"head": 0 if n else None}
        self.counts: dict = {}
        self.steps: list = []

    def add(self, note, curr=None):
        s = {"values": list(self.values), "next": list(self.nxt), "curr": curr,
             "removed": list(self.removed),
             "pointers": [[k, v] for k, v in self.ptr.items() if v is not None],
             "counts": dict(self.counts)}
        if self.prv is not None:
            s["prev_links"] = list(self.prv)
        self.steps.append({"i": len(self.steps), "line": 0, "structures": s,
                           "highlight": {"index": curr}, "note": note})

    def order(self, start=None):
        out, j = [], self.ptr["head"] if start is None else start
        while j is not None and len(out) <= len(self.values):
            out.append(self.values[j])
            j = self.nxt[j]
        return out

    def result(self, algo, res):
        return {"meta": {"algorithm": algo, "view": "list", "language": "python",
                         "result": res},
                "array": self.values, "steps": self.steps}


def arrow(order):
    return " → ".join(map(str, order)) or "(empty)"


# ── batch 60: basics ───────────────────────────────────────────────────
def _insert(a, x, doubly, algo):
    G = L(a, doubly)
    G.counts = {"links_changed": 0}
    G.add(f"The list starts at the head ({a[0]}). A new head needs no walk — "
          f"just a new node pointing at the old head.", 0)
    G.values = [x] + a
    G.nxt = [None] + [j + 1 if j is not None else None for j in G.nxt]
    if doubly:
        G.prv = [None] + [j + 1 if j is not None else None for j in G.prv]
    G.ptr = {"head": 1, "new": 0}
    G.add(f"Create node {x}.", 0)
    G.nxt[0] = 1
    G.counts["links_changed"] += 1
    G.add(f"new.next = head: {x} now points at {a[0]}.", 0)
    if doubly:
        G.prv[1] = 0
        G.counts["links_changed"] += 1
        G.add(f"head.prev = new: {a[0]} points back at {x}.", 1)
    G.ptr = {"head": 0}
    G.add(f"Move head to the new node. List: {arrow(G.order())}. O(1).", 0)
    return G.result(algo, G.order())


def _ll_insert_head(a, x):
    return _insert(a, x, False, "ll_insert_head")


def _dll_insert_head(a, x):
    return _insert(a, x, True, "dll_insert_head")


def _delete(a, doubly, algo):
    G = L(a, doubly)
    G.counts = {"links_changed": 0}
    G.add(f"To delete the head ({a[0]}), remember it, then move head one step.", 0)
    if len(a) == 1:
        G.removed = [0]
        G.ptr = {"head": None}
        G.add("It was the only node — the list is now empty.")
        return G.result(algo, [])
    G.ptr = {"head": 1, "old": 0}
    G.add(f"head = head.next → {a[1]}.", 1)
    if doubly:
        G.prv[1] = None
        G.counts["links_changed"] += 1
        G.add(f"The new head's prev must not point at the deleted node: "
              f"{a[1]}.prev = null.", 1)
    G.nxt[0] = None
    G.removed = [0]
    G.counts["links_changed"] += 1
    G.ptr = {"head": 1}
    G.add(f"Detach and free the old head. List: {arrow(G.order())}.", 1)
    return G.result(algo, G.order())


def _ll_delete_head(a):
    return _delete(a, False, "ll_delete_head")


def _dll_delete_head(a):
    return _delete(a, True, "dll_delete_head")


def _ll_length(a):
    G = L(a)
    G.counts = {"count": 0}
    G.add("A list doesn't store its length: walk from the head, counting nodes "
          "until next is null.", 0)
    j = 0
    while j is not None:
        G.counts["count"] += 1
        G.ptr = {"head": 0, "temp": j}
        G.add(f"Count node {a[j]} → {G.counts['count']}.", j)
        j = G.nxt[j]
    G.add(f"next is null — length {len(a)}.")
    return G.result("ll_length", len(a))


def _ll_search(a, x):
    G = L(a)
    G.counts = {"checks": 0}
    G.add(f"No indexing in a list: walk from the head comparing each value "
          f"with {x}.", 0)
    j = 0
    while j is not None:
        G.counts["checks"] += 1
        G.ptr = {"head": 0, "temp": j}
        if a[j] == x:
            G.add(f"Node {j} holds {x} — found.", j)
            return G.result("ll_search", j)
        G.add(f"Node {j} holds {a[j]}, not {x}. Move on.", j)
        j = G.nxt[j]
    G.ptr = {"head": 0}
    G.add(f"Reached null — {x} is not in the list.")
    return G.result("ll_search", -1)


def _dll_pairs_sum(a, t):
    G = L(a, True)
    G.counts = {"checks": 0}
    l, r = 0, len(a) - 1
    G.ptr = {"left": l, "right": r}
    G.add(f"The DLL is sorted, and prev lets us walk back from the tail: start "
          f"left at the head and right at the tail, like two pointers in an "
          f"array. Target {t}.", l)
    pairs = []
    while l < r:
        G.counts["checks"] += 1
        s = a[l] + a[r]
        G.ptr = {"left": l, "right": r}
        if s == t:
            pairs.append([a[l], a[r]])
            G.add(f"{a[l]} + {a[r]} = {t} — record the pair; move both inward.", l)
            l, r = l + 1, r - 1
        elif s < t:
            G.add(f"{a[l]} + {a[r]} = {s} < {t} — left moves forward (next).", l)
            l += 1
        else:
            G.add(f"{a[l]} + {a[r]} = {s} > {t} — right moves back (prev).", r)
            r -= 1
    G.ptr = {}
    G.add(f"The pointers met. Pairs: {pairs or 'none'}.")
    return G.result("dll_pairs_sum", pairs)


def _dll_remove_duplicates(a):
    G = L(a, True)
    G.counts = {"removed": 0}
    G.add("Sorted, so duplicates sit next to each other. At each node, unlink "
          "every following node with the same value.", 0)
    j = 0
    while j is not None:
        k = G.nxt[j]
        while k is not None and a[k] == a[j]:
            G.nxt[j] = G.nxt[k]
            if G.nxt[k] is not None:
                G.prv[G.nxt[k]] = j
            G.nxt[k] = G.prv[k] = None
            G.removed.append(k)
            G.counts["removed"] += 1
            G.ptr = {"head": 0, "curr": j}
            G.add(f"Node {k} repeats {a[j]}: link {a[j]} past it (both next and "
                  f"prev), then drop it.", j)
            k = G.nxt[j]
        G.ptr = {"head": 0, "curr": j}
        G.add(f"{a[j]} is now unique; move on.", j)
        j = G.nxt[j]
    G.ptr = {"head": 0}
    G.add(f"Result: {arrow(G.order())}.")
    return G.result("dll_remove_duplicates", G.order())


# ── batch 61: medium / hard ────────────────────────────────────────────
def _ll_reverse_recursive(a):
    G = L(a)
    G.counts = {"calls": 0, "links_flipped": 0}
    G.add("reverse(node): reverse everything after node first, then make the "
          "next node point back at node. The last node becomes the new head.", 0)

    def rev(j):
        G.counts["calls"] += 1
        G.ptr = {"head": 0, "call": j}
        if G.nxt[j] is None:
            G.add(f"reverse({a[j]}): the last node — it is the new head. Return it.", j)
            return j
        G.add(f"reverse({a[j]}): first reverse the rest, starting at "
              f"{a[G.nxt[j]]}.", j)
        head = rev(G.nxt[j])
        nx = G.nxt[j]
        G.nxt[nx] = j
        G.nxt[j] = None
        G.counts["links_flipped"] += 1
        G.ptr = {"newHead": head, "call": j}
        G.add(f"Back in reverse({a[j]}): {a[nx]}.next = {a[j]}, and {a[j]}.next = "
              f"null.", j)
        return head

    head = rev(0)
    G.ptr = {"head": head}
    G.add(f"Reversed: {arrow(G.order())}.", head)
    return G.result("ll_reverse_recursive", G.order())


def _loop_length(a, to):
    G = L(a)
    n = len(a)
    G.counts = {"steps": 0}
    if to >= 0:
        G.nxt[n - 1] = to
    G.add("Floyd: slow moves 1, fast moves 2. If they meet, there is a loop — "
          + (f"the tail links back to node {to}." if to >= 0
             else "(here the tail ends in null)."), 0)
    slow = fast = 0
    while fast is not None and G.nxt[fast] is not None:
        slow, fast = G.nxt[slow], G.nxt[G.nxt[fast]]
        G.counts["steps"] += 1
        G.ptr = {"slow": slow, "fast": fast}
        G.add(f"slow → {a[slow]}, fast → {a[fast] if fast is not None else 'null'}.",
              slow)
        if slow == fast:
            break
    else:
        G.ptr = {}
        G.add("fast hit null — no loop, length 0.")
        return G.result("loop_length", 0)
    length, j = 1, G.nxt[slow]
    G.add(f"They met at {a[slow]}: that node is inside the loop. Walk once "
          f"around and count.", slow)
    while j != slow:
        length += 1
        G.ptr = {"meet": slow, "walk": j}
        G.add(f"Walk to {a[j]}: count {length}.", j)
        j = G.nxt[j]
    G.ptr = {"meet": slow}
    G.add(f"Back at the meeting node — the loop has {length} node(s).", slow)
    return G.result("loop_length", length)


def _sort_012_list(a):
    G = L(a)
    G.counts = {"relinks": 0}
    G.add("Don't swap values — relink. Walk once, appending each node to the "
          "end of the 0-chain, 1-chain or 2-chain; then join the chains.", 0)
    tails, heads = {}, {}
    j = 0
    while j is not None:
        nx = G.nxt[j]
        v = a[j]
        if v in tails:
            G.nxt[tails[v]] = j
        else:
            heads[v] = j
        tails[v] = j
        G.nxt[j] = None
        G.counts["relinks"] += 1
        G.ptr = {f"tail{k}": t for k, t in sorted(tails.items())}
        G.ptr["walk"] = nx
        G.add(f"{v} joins the {v}-chain.", j)
        j = nx
    chain = [v for v in (0, 1, 2) if v in heads]
    for x, y in zip(chain, chain[1:]):
        G.nxt[tails[x]] = heads[y]
        G.counts["relinks"] += 1
        G.ptr = {"head": heads[chain[0]]}
        G.add(f"Join: the end of the {x}-chain points at the start of the "
              f"{y}-chain.", tails[x])
    G.ptr = {"head": heads[chain[0]]}
    G.add(f"Sorted: {arrow(G.order())}.", heads[chain[0]])
    return G.result("sort_012_list", G.order())


def _sort_list(a):
    G = L(a)
    G.counts = {"merges": 0, "comparisons": 0}
    G.add("Merge sort suits lists: find the middle with slow/fast, cut there, "
          "sort both halves, then merge them by relinking — no extra array.", 0)

    def sort(h):
        if h is None or G.nxt[h] is None:
            return h
        slow, fast = h, G.nxt[h]
        while fast is not None and G.nxt[fast] is not None:
            slow, fast = G.nxt[slow], G.nxt[G.nxt[fast]]
        right = G.nxt[slow]
        G.nxt[slow] = None
        G.ptr = {"left": h, "right": right}
        G.add(f"Split after {a[slow]}: [{arrow(G.order(h))}] and "
              f"[{arrow(G.order(right))}].", slow)
        return merge(sort(h), sort(right))

    def merge(x, y):
        head = tail = None
        while x is not None and y is not None:
            G.counts["comparisons"] += 1
            if a[x] <= a[y]:
                pick, x = x, G.nxt[x]
            else:
                pick, y = y, G.nxt[y]
            if tail is None:
                head = pick
            else:
                G.nxt[tail] = pick
            tail = pick
        G.nxt[tail] = x if x is not None else y
        G.counts["merges"] += 1
        G.ptr = {"merged": head}
        G.add(f"Merge → {arrow(G.order(head))}.", head)
        return head

    head = sort(0)
    G.ptr = {"head": head}
    G.add(f"Sorted: {arrow(G.order())}.", head)
    return G.result("sort_list", G.order())


def _y(a, b, c):
    va = a + b + c
    na, nb = len(a), len(b)
    G = L(va)
    ia = list(range(na))
    ib = list(range(na, na + nb))
    ic = list(range(na + nb, len(va)))
    G.nxt = [None] * len(va)
    for chain in (ia + ic, ib + ic):
        for x, y in zip(chain, chain[1:]):
            G.nxt[x] = y
    ha, hb = (ia + ic)[0], (ib + ic)[0]
    G.counts = {"steps": 0}
    G.ptr = {"headA": ha, "headB": hb}
    G.add("Two lists may merge into one tail. Walk p from A and q from B; when "
          "one runs off the end, restart it at the OTHER head. Both then walk "
          "(A-only + B-only + shared) nodes, so they meet at the join — or both "
          "run out together.", ha)
    p, q = ha, hb
    while p != q:
        p = hb if G.nxt[p] is None else G.nxt[p]
        q = ha if G.nxt[q] is None else G.nxt[q]
        G.counts["steps"] += 1
        if p == q:
            break
        G.ptr = {"p": p, "q": q}
        G.add(f"p → {va[p]}, q → {va[q]}.", p)
        if not ic and G.counts["steps"] >= na + nb:
            G.add("Both pointers have walked A + B with no common node — no "
                  "intersection.")
            return G.result("y_intersection", None)
    G.ptr = {"p": p, "q": q}
    G.add(f"p and q are the same node ({va[p]}) — the intersection point.", p)
    return G.result("y_intersection", va[p])


def _reverse_k_group(a, k):
    G = L(a)
    G.counts = {"groups": 0, "links_flipped": 0}
    G.add(f"Take k = {k} nodes at a time; if a full group exists, reverse it in "
          f"place and stitch it to the previous group's tail. A short last "
          f"group stays as is.", 0)
    head, prev_tail, start = None, None, 0
    while start is not None:
        end, cnt = start, 1
        while cnt < k and G.nxt[end] is not None:
            end, cnt = G.nxt[end], cnt + 1
        if cnt < k:
            G.ptr = {"head": head, "rest": start}
            G.add(f"Only {cnt} node(s) left — fewer than {k}, leave them.", start)
            break
        nxt_start = G.nxt[end]
        prev, cur = nxt_start, start
        while cur != nxt_start:
            nx = G.nxt[cur]
            G.nxt[cur] = prev
            prev, cur = cur, nx
            G.counts["links_flipped"] += 1
        G.counts["groups"] += 1
        if prev_tail is None:
            head = end
        else:
            G.nxt[prev_tail] = end
        G.ptr = {"head": head, "groupHead": end, "groupTail": start}
        G.add(f"Reversed a group: it now starts at {a[end]} and ends at "
              f"{a[start]}, which points on to "
              f"{a[nxt_start] if nxt_start is not None else 'null'}.", end)
        prev_tail, start = start, nxt_start
    G.ptr = {"head": head}
    G.add(f"Result: {arrow(G.order())}.", head)
    return G.result("reverse_k_group", G.order())
