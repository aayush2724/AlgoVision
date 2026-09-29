"""Linked-list fundamentals the 2026 sheet spells out one operation at a
time (Linked-List / Fundamentals), on the `list` view. Boxes are nodes, solid
arrows `next`, dashed arrows `prev`. Node indices stay stable: a created
node gets a new index and the step's `values` list grows.

Singly: traverse, delete tail / kth / by value, insert at tail / at kth /
before a value. Doubly: build from an array, delete tail / kth / a given
node, insert before the tail / before the kth / before a given node.

Input: the list, plus `| v` for a value to insert; `target` carries k or the
value to look for (see NEEDS_T / NEEDS_V).
"""

from app.tracers.ll_more import L, arrow

TITLES = {
    "ll_traverse": "Traverse a Linked List",
    "ll_delete_tail": "Delete the Tail of a Linked List",
    "ll_delete_kth": "Delete the Kth Node of a Linked List",
    "ll_delete_value": "Delete a Node by Value",
    "ll_insert_tail": "Insert at the Tail of a Linked List",
    "ll_insert_kth": "Insert at the Kth Position of a Linked List",
    "ll_insert_before_value": "Insert Before a Value in a Linked List",
    "dll_from_array": "Build a Doubly Linked List From an Array",
    "dll_delete_tail": "Delete the Tail of a Doubly Linked List",
    "dll_delete_kth": "Delete the Kth Node of a Doubly Linked List",
    "dll_remove_node": "Remove a Given Node From a Doubly Linked List",
    "dll_insert_before_tail": "Insert Before the Tail of a Doubly Linked List",
    "dll_insert_before_kth": "Insert Before the Kth Node of a Doubly Linked List",
    "dll_insert_before_node": "Insert Before a Given Node in a Doubly Linked List",
}
# target = k (1-based position)
NEEDS_K = {"ll_delete_kth", "ll_insert_kth", "dll_delete_kth", "dll_insert_before_kth"}
# target = a value to find
NEEDS_X = {"ll_delete_value", "ll_insert_before_value", "dll_remove_node",
           "dll_insert_before_node", "ll_insert_tail", "dll_insert_before_tail"}
# text carries "| v", the value to insert
NEEDS_V = {"ll_insert_kth", "ll_insert_before_value", "dll_insert_before_kth",
           "dll_insert_before_node"}
MAX = 10


def _ord(k):
    return f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def _nums(text, lo=1):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (lo <= len(a) <= MAX) or any(abs(v) > 99 for v in a):
        raise ValueError(f"Give {lo}–{MAX} values within ±99.")
    return a


def run(algo, text, target=None):
    text = text or ""
    v = None
    if algo in NEEDS_V:
        if "|" not in text:
            raise ValueError("Add '| v' after the list — the value to insert, e.g. 1,2,3 | 9.")
        text, vtxt = text.split("|", 1)
        try:
            v = int(vtxt.strip())
        except ValueError:
            raise ValueError("After '|', give one whole number.") from None
        if abs(v) > 99:
            raise ValueError("Keep the new value within ±99.")
    a = _nums(text)
    t = None
    if algo in NEEDS_K or algo in NEEDS_X:
        if target is None or target != int(target):
            raise ValueError("Give a whole number.")
        t = int(target)
        if algo in NEEDS_K:
            hi = len(a) + 1 if algo == "ll_insert_kth" else len(a)
            if not (1 <= t <= hi):
                raise ValueError(f"k must be 1–{hi}.")
        elif algo in ("ll_insert_tail", "dll_insert_before_tail"):
            if abs(t) > 99:
                raise ValueError("Keep the new value within ±99.")
        elif t not in a:
            raise ValueError(f"{t} is not in the list.")
    if algo in NEEDS_V and len(a) >= MAX:
        raise ValueError(f"At most {MAX - 1} nodes before inserting.")
    if algo in ("ll_insert_tail", "dll_insert_before_tail") and len(a) >= MAX:
        raise ValueError(f"At most {MAX - 1} nodes before inserting.")
    fn = globals()["_" + algo]
    if algo in NEEDS_V:
        return fn(a, t, v)
    if t is not None:
        return fn(a, t)
    return fn(a)


def _walk_to(G, a, stop, label="temp"):
    """Walk from the head to node index `stop`, one step per node."""
    j = 0
    while j is not None and j != stop:
        G.ptr = {"head": 0, label: j}
        G.add(f"At {a[j]} — not there yet, follow next.", j)
        j = G.nxt[j]
    G.ptr = {"head": 0, label: stop}
    return stop


def _ll_traverse(a):
    G = L(a)
    G.counts = {"visited": 0}
    G.add("Start a temp pointer at the head and follow next until it is null.", 0)
    j, out = 0, []
    while j is not None:
        out.append(a[j])
        G.counts["visited"] += 1
        G.ptr = {"head": 0, "temp": j}
        G.add(f"Visit {a[j]}: printed so far {out}.", j)
        j = G.nxt[j]
    G.ptr = {"head": 0}
    G.add(f"temp is null — done: {arrow(out)}.")
    return G.result("ll_traverse", out)


def _delete_tail(a, doubly, algo):
    G = L(a, doubly)
    G.counts = {"links_changed": 0}
    n = len(a)
    if n == 1:
        G.add("Only one node — deleting the tail empties the list.", 0)
        G.removed, G.ptr, G.nxt[0] = [0], {"head": None}, None
        G.add("List is now empty.")
        return G.result(algo, [])
    if doubly:
        G.add(f"With prev pointers there is no walk: tail ({a[-1]}) knows its previous node.", n - 1)
        G.ptr = {"head": 0, "tail": n - 1}
        G.add(f"Step back: newTail = tail.prev = {a[-2]}.", n - 2)
    else:
        G.add(f"Singly linked: to unlink the tail ({a[-1]}) walk to the node BEFORE it.", 0)
        _walk_to(G, a, n - 2)
        G.add(f"temp.next is the tail — stop at {a[-2]}.", n - 2)
    G.nxt[n - 2] = None
    G.counts["links_changed"] += 1
    if doubly:
        G.prv[n - 1] = None
        G.counts["links_changed"] += 1
    G.removed = [n - 1]
    G.ptr = {"head": 0}
    G.add(f"Set {a[-2]}.next = null and free {a[-1]}. List: {arrow(G.order())}.", n - 2)
    return G.result(algo, G.order())


def _ll_delete_tail(a):
    return _delete_tail(a, False, "ll_delete_tail")


def _dll_delete_tail(a):
    return _delete_tail(a, True, "dll_delete_tail")


def _delete_kth(a, k, doubly, algo):
    G = L(a, doubly)
    G.counts = {"links_changed": 0}
    n, i = len(a), k - 1
    if n == 1:
        G.add("The only node is the kth — the list becomes empty.", 0)
        G.removed, G.ptr, G.nxt[0] = [0], {"head": None}, None
        G.add("List is now empty.")
        return G.result(algo, [])
    if i == 0:
        G.add(f"k = 1 is the head ({a[0]}): move head to the second node.", 0)
        G.ptr = {"head": 1}
        G.nxt[0] = None
        if doubly:
            G.prv[1] = None
            G.counts["links_changed"] += 1
        G.removed = [0]
        G.counts["links_changed"] += 1
        G.add(f"Head is now {a[1]}. List: {arrow(G.order())}.", 1)
        return G.result(algo, G.order())
    G.add(f"Walk to the {_ord(k)} node, counting from 1 at the head.", 0)
    j, c = 0, 1
    while c < k:
        G.ptr = {"head": 0, "temp": j}
        G.add(f"Count {c} at {a[j]} — keep going.", j)
        j, c = G.nxt[j], c + 1
    prev = i - 1
    G.ptr = {"head": 0, "temp": j}
    G.add(f"Count {k}: this is it ({a[j]}). Its neighbours are {a[prev]}"
          f"{' and ' + str(a[i + 1]) if i + 1 < n else ''}.", j)
    G.nxt[prev] = G.nxt[i]
    G.counts["links_changed"] += 1
    if doubly and i + 1 < n:
        G.prv[i + 1] = prev
        G.counts["links_changed"] += 1
    G.nxt[i] = None
    if doubly:
        G.prv[i] = None
    G.removed = [i]
    G.ptr = {"head": 0}
    G.add(f"Bypass it: {a[prev]}.next = {a[i + 1] if i + 1 < n else 'null'}"
          f"{'; fix prev on the other side' if doubly and i + 1 < n else ''}. List: {arrow(G.order())}.",
          prev)
    return G.result(algo, G.order())


def _ll_delete_kth(a, k):
    return _delete_kth(a, k, False, "ll_delete_kth")


def _dll_delete_kth(a, k):
    return _delete_kth(a, k, True, "dll_delete_kth")


def _ll_delete_value(a, x):
    return _delete_by_value(a, x, False, "ll_delete_value")


def _delete_by_value(a, x, doubly, algo):
    G = L(a, doubly)
    G.counts = {"checks": 0, "links_changed": 0}
    n, i = len(a), a.index(x)
    G.add(f"Find the first node holding {x}, remembering the node before it.", 0)
    j = 0
    while a[j] != x:
        G.counts["checks"] += 1
        G.ptr = {"head": 0, "prev": j}
        G.add(f"{a[j]} ≠ {x}, move on.", j)
        j = G.nxt[j]
    G.counts["checks"] += 1
    G.ptr = {"head": 0, "temp": i}
    G.add(f"Found {x} at node {i}.", i)
    if n == 1:
        G.removed, G.ptr, G.nxt[0] = [0], {"head": None}, None
        G.add("It was the only node — the list is empty.")
        return G.result(algo, [])
    if i == 0:
        G.ptr = {"head": 1}
        G.nxt[0] = None
        if doubly:
            G.prv[1] = None
            G.counts["links_changed"] += 1
        G.removed = [0]
        G.counts["links_changed"] += 1
        G.add(f"It is the head: head = head.next. List: {arrow(G.order())}.", 1)
        return G.result(algo, G.order())
    prev = i - 1
    G.nxt[prev] = G.nxt[i]
    G.counts["links_changed"] += 1
    if doubly and i + 1 < n:
        G.prv[i + 1] = prev
        G.counts["links_changed"] += 1
    G.nxt[i] = None
    if doubly:
        G.prv[i] = None
    G.removed = [i]
    G.ptr = {"head": 0}
    G.add(f"Bypass it: {a[prev]}.next = {a[i + 1] if i + 1 < n else 'null'}. List: {arrow(G.order())}.", prev)
    return G.result(algo, G.order())


def _dll_remove_node(a, x):
    return _delete_by_value(a, x, True, "dll_remove_node")


def _append(G, v, doubly):
    """Create node v at a new index; return its index (not yet linked)."""
    G.values.append(v)
    G.nxt.append(None)
    if doubly:
        G.prv.append(None)
    return len(G.values) - 1


def _ll_insert_tail(a, v):
    G = L(a)
    G.counts = {"links_changed": 0}
    n = len(a)
    G.add(f"No tail pointer here: walk to the last node, then hang {v} after it.", 0)
    _walk_to(G, a, n - 1)
    G.add(f"{a[-1]}.next is null — this is the tail.", n - 1)
    k = _append(G, v, False)
    G.ptr = {"head": 0, "new": k}
    G.add(f"Create node {v}.", k)
    G.nxt[n - 1] = k
    G.counts["links_changed"] += 1
    G.ptr = {"head": 0}
    G.add(f"{a[-1]}.next = new. List: {arrow(G.order())}.", k)
    return G.result("ll_insert_tail", G.order())


def _ll_insert_kth(a, k, v):
    G = L(a)
    G.counts = {"links_changed": 0}
    n = len(a)
    if k == 1:
        G.add(f"k = 1: the new node becomes the head.", 0)
        j = _append(G, v, False)
        G.nxt[j] = 0
        G.ptr = {"head": j}
        G.counts["links_changed"] += 1
        G.add(f"new.next = old head; head = new. List: {arrow(G.order())}.", j)
        return G.result("ll_insert_kth", G.order())
    G.add(f"Walk to position {k - 1}; the new node goes right after it.", 0)
    j, c = 0, 1
    while c < k - 1:
        G.ptr = {"head": 0, "temp": j}
        G.add(f"Position {c} is {a[j]} — keep going.", j)
        j, c = G.nxt[j], c + 1
    G.ptr = {"head": 0, "temp": j}
    G.add(f"Position {k - 1} is {a[j]}. Insert after it.", j)
    m = _append(G, v, False)
    G.nxt[m] = G.nxt[j]
    G.counts["links_changed"] += 1
    G.ptr = {"head": 0, "temp": j, "new": m}
    G.add(f"new.next = {a[j]}.next ({a[j + 1] if j + 1 < n else 'null'}).", m)
    G.nxt[j] = m
    G.counts["links_changed"] += 1
    G.ptr = {"head": 0}
    G.add(f"{a[j]}.next = new. List: {arrow(G.order())}.", m)
    return G.result("ll_insert_kth", G.order())


def _ll_insert_before_value(a, x, v):
    G = L(a)
    G.counts = {"checks": 0, "links_changed": 0}
    i = a.index(x)
    G.add(f"Find {x}, but stop one node early — that is where the link changes.", 0)
    if i == 0:
        G.counts["checks"] += 1
        G.add(f"{x} is the head: the new node becomes the head.", 0)
        j = _append(G, v, False)
        G.nxt[j] = 0
        G.ptr = {"head": j}
        G.counts["links_changed"] += 1
        G.add(f"new.next = old head; head = new. List: {arrow(G.order())}.", j)
        return G.result("ll_insert_before_value", G.order())
    j = 0
    while a[G.nxt[j]] != x:
        G.counts["checks"] += 1
        G.ptr = {"head": 0, "temp": j}
        G.add(f"{a[j]}'s next is {a[j + 1]}, not {x} — move on.", j)
        j = G.nxt[j]
    G.counts["checks"] += 1
    G.ptr = {"head": 0, "temp": j}
    G.add(f"{a[j]}.next is {x}. Insert between them.", j)
    m = _append(G, v, False)
    G.nxt[m] = i
    G.nxt[j] = m
    G.counts["links_changed"] += 2
    G.ptr = {"head": 0}
    G.add(f"new.next = {x}; {a[j]}.next = new. List: {arrow(G.order())}.", m)
    return G.result("ll_insert_before_value", G.order())


def _dll_from_array(a):
    G = L([], True)
    G.counts = {"nodes": 0}
    G.add(f"Array {a}: create a node per value, linking next forward and prev back.")
    tail = None
    for v in a:
        k = _append(G, v, True)
        G.counts["nodes"] += 1
        if tail is None:
            G.ptr = {"head": k, "tail": k}
            G.add(f"First node {v} — it is both head and tail.", k)
        else:
            G.nxt[tail] = k
            G.prv[k] = tail
            G.ptr = {"head": 0, "tail": k}
            G.add(f"Node {v}: {G.values[tail]}.next = {v}, {v}.prev = {G.values[tail]}.", k)
        tail = k
    G.add(f"Done: {arrow(G.order())}, with every prev pointing back.")
    return G.result("dll_from_array", G.order())


def _dll_insert_before_tail(a, v):
    G = L(a, True)
    G.counts = {"links_changed": 0}
    n = len(a)
    if n == 1:
        G.add(f"One node: 'before the tail' means a new head.", 0)
        k = _append(G, v, True)
        G.nxt[k], G.prv[0] = 0, k
        G.ptr = {"head": k, "tail": 0}
        G.counts["links_changed"] += 2
        G.add(f"new.next = {a[0]}, {a[0]}.prev = new. List: {arrow(G.order())}.", k)
        return G.result("dll_insert_before_tail", G.order())
    G.ptr = {"head": 0, "tail": n - 1}
    G.add(f"Tail is {a[-1]}; its prev ({a[-2]}) is where the new node goes after.", n - 1)
    k = _append(G, v, True)
    G.ptr = {"head": 0, "tail": n - 1, "new": k}
    G.add(f"Create {v}.", k)
    G.nxt[k], G.prv[k] = n - 1, n - 2
    G.counts["links_changed"] += 2
    G.add(f"new.next = tail, new.prev = {a[-2]}.", k)
    G.nxt[n - 2], G.prv[n - 1] = k, k
    G.counts["links_changed"] += 2
    G.ptr = {"head": 0, "tail": n - 1}
    G.add(f"{a[-2]}.next = new, tail.prev = new. List: {arrow(G.order())}.", k)
    return G.result("dll_insert_before_tail", G.order())


def _insert_before_index(G, a, i, v, algo):
    n = len(a)
    k = _append(G, v, True)
    if i == 0:
        G.nxt[k], G.prv[0] = 0, k
        G.ptr = {"head": k}
        G.counts["links_changed"] += 2
        G.add(f"It is the head: new.next = {a[0]}, {a[0]}.prev = new, head = new. "
              f"List: {arrow(G.order())}.", k)
        return G.result(algo, G.order())
    p = i - 1
    G.ptr = {"head": 0, "new": k}
    G.add(f"Create {v}; it sits between {a[p]} and {a[i]}.", k)
    G.nxt[k], G.prv[k] = i, p
    G.counts["links_changed"] += 2
    G.add(f"new.next = {a[i]}, new.prev = {a[p]}.", k)
    G.nxt[p], G.prv[i] = k, k
    G.counts["links_changed"] += 2
    G.ptr = {"head": 0}
    G.add(f"{a[p]}.next = new, {a[i]}.prev = new. List: {arrow(G.order())}.", k)
    return G.result(algo, G.order())


def _dll_insert_before_kth(a, k, v):
    G = L(a, True)
    G.counts = {"links_changed": 0}
    G.add(f"Walk to the {_ord(k)} node; the new node goes just before it.", 0)
    j, c = 0, 1
    while c < k:
        G.ptr = {"head": 0, "temp": j}
        G.add(f"Count {c} at {a[j]}.", j)
        j, c = G.nxt[j], c + 1
    G.ptr = {"head": 0, "temp": j}
    G.add(f"Count {k}: {a[j]}. Its prev is {'null' if j == 0 else a[j - 1]}.", j)
    return _insert_before_index(G, a, j, v, "dll_insert_before_kth")


def _dll_insert_before_node(a, x, v):
    G = L(a, True)
    G.counts = {"checks": 0, "links_changed": 0}
    i = a.index(x)
    G.add(f"Find the node holding {x}. With prev pointers, no need to stop early.", 0)
    j = 0
    while a[j] != x:
        G.counts["checks"] += 1
        G.ptr = {"head": 0, "temp": j}
        G.add(f"{a[j]} ≠ {x}.", j)
        j = G.nxt[j]
    G.counts["checks"] += 1
    G.ptr = {"head": 0, "temp": i}
    G.add(f"Found {x}; its prev is {'null' if i == 0 else a[i - 1]}.", i)
    return _insert_before_index(G, a, i, v, "dll_insert_before_node")
