"""Building, threading and reshaping binary trees (Steps 13, 14) on the
`tree` view.

* build_pre_in / build_post_in — the first preorder (last postorder) value
  is the root; its position in the inorder splits the rest into left and
  right subtrees. Nodes appear as they are created, already in their final
  positions.
* serialize_tree — BFS writes every node and every missing child ('#');
  deserialising reads the same stream back, two children per node.
* morris_inorder / morris_preorder — O(1)-space traversal: before going
  left, thread the left subtree's rightmost node back to the current node
  (drawn dashed via the step's `threads`); meeting the thread again means
  "left side done".
* flatten_tree — for each node with a left child, splice the left subtree
  between the node and its right subtree (rightmost of left → old right).
* identical_trees — walk both trees in lockstep, comparing values and
  shapes.
* merge_two_bsts — the inorder of a BST is sorted: take both inorders, then
  merge two sorted lists.
"""

from app.tracers import bt_common as bt
from app.tracers.tree_traversal import _build as _bst_build, _layout

TITLES = {
    "build_pre_in": "Construct a Binary Tree from Preorder & Inorder",
    "build_post_in": "Construct a Binary Tree from Postorder & Inorder",
    "serialize_tree": "Serialize and Deserialize a Binary Tree",
    "morris_inorder": "Morris Inorder Traversal",
    "morris_preorder": "Morris Preorder Traversal",
    "flatten_tree": "Flatten a Binary Tree to a Linked List",
    "identical_trees": "Check if Two Trees are Identical",
    "merge_two_bsts": "Merge Two BSTs (sorted output)",
}


class _Mismatch(Exception):
    pass


def _nums(text, n=15):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(abs(v) > 999 for v in a):
        raise ValueError(f"Give 1–{n} numbers within ±999.")
    return a


def run(algo, text, target=None):
    if algo in ("build_pre_in", "build_post_in"):
        if "|" not in (text or ""):
            raise ValueError("Give 'order | inorder', e.g. 3,9,20,15,7 | 9,3,15,20,7.")
        first, ino = (_nums(p) for p in text.split("|", 1))
        if sorted(first) != sorted(ino) or len(set(ino)) != len(ino):
            raise ValueError("Both lists need the same distinct values.")
        try:
            return _construct(first, ino, algo)
        except _Mismatch:
            raise ValueError("Those two traversals don't describe the same tree.") from None
    if algo in ("identical_trees", "merge_two_bsts"):
        if "|" not in (text or ""):
            raise ValueError("Give two trees separated by '|'.")
        a, b = text.split("|", 1)
        if algo == "merge_two_bsts":
            return _merge_bsts(_nums(a, 7), _nums(b, 7))
        ta, tb = bt.parse(a), bt.parse(b)
        if sum(v is not None for v in ta + tb) > 15:
            raise ValueError("At most 15 nodes across both trees.")
        return _identical(ta, tb)
    vals = bt.parse(text)
    return {"serialize_tree": _serialize, "morris_inorder": _morris,
            "morris_preorder": _morris, "flatten_tree": _flatten}[algo](vals, algo)


def _level_order(nodes, root):
    out, q = [], [root]
    while q:
        nid = q.pop(0)
        if nid is None:
            out.append(None)
            continue
        out.append(nodes[nid]["value"])
        q += [nodes[nid]["left"], nodes[nid]["right"]]
    while out and out[-1] is None:
        out.pop()
    return out


def _construct(order, ino, algo):
    pre = algo == "build_pre_in"
    where = {v: i for i, v in enumerate(ino)}
    seq = list(order) if pre else list(reversed(order))
    nodes, pos = [], [0]

    def make(lo, hi):                 # full build first, to fix the layout
        if lo > hi:
            return None
        v = seq[pos[0]]
        pos[0] += 1
        k = where[v]
        if not (lo <= k <= hi):
            raise _Mismatch
        nid = len(nodes)
        nodes.append({"id": nid, "value": v, "left": None, "right": None,
                      "lo": lo, "hi": hi, "k": k})
        if pre:
            nodes[nid]["left"] = make(lo, k - 1)
            nodes[nid]["right"] = make(k + 1, hi)
        else:
            nodes[nid]["right"] = make(k + 1, hi)
            nodes[nid]["left"] = make(lo, k - 1)
        return nid

    make(0, len(ino) - 1)
    if pos[0] != len(seq):
        raise _Mismatch
    _layout(nodes, 0)
    S = bt.Stepper([])
    S.counts = {"nodes_built": 0}
    name = "preorder" if pre else "postorder"
    S.add(f"The {'first' if pre else 'last'} {name} value is the root. Find it in "
          f"the inorder: everything left of it is the left subtree, everything "
          f"right of it the right subtree. Recurse "
          f"{'left, then right' if pre else 'right, then left (postorder read backwards)'}.")
    created = []
    for n in nodes:                     # list order == creation order
        created.append(n["id"])
        S.nodes = [nodes[i] for i in created]
        S.counts["nodes_built"] += 1
        S.add(f"Next {name} value {n['value']} roots inorder[{n['lo']}..{n['hi']}]. "
              f"Left subtree {ino[n['lo']:n['k']] or '∅'}, right subtree "
              f"{ino[n['k'] + 1:n['hi'] + 1] or '∅'}.", n["id"], created[:-1])
    S.nodes = nodes
    res = _level_order(nodes, 0)
    S.add(f"Built. Level order: {res}.", None, list(range(len(nodes))))
    return bt.result(algo, S.steps, res)


def _serialize(vals, algo):
    nodes = bt.build(vals)
    S = bt.Stepper(nodes)
    S.counts = {"tokens": 0}
    S.add("Serialise with BFS: write each node's value, and '#' for every "
          "missing child, so the shape survives.")
    out, q, seen = [], [0], []
    while q:
        nid = q.pop(0)
        S.counts["tokens"] += 1
        if nid is None:
            out.append("#")
            continue
        out.append(str(nodes[nid]["value"]))
        seen.append(nid)
        q += [nodes[nid]["left"], nodes[nid]["right"]]
        S.add(f"Write {nodes[nid]['value']}; queue its two children. So far: "
              f"{','.join(out)}", nid, seen[:-1])
    data = ",".join(out)
    S.add(f"Serialised: {data}. Now rebuild it: the first token is the root; "
          f"each dequeued node takes the next two tokens as its children.",
          None, seen)
    shown = [0]
    S.nodes = [nodes[0]]
    S.add(f"Root {nodes[0]['value']}.", 0)
    for nid in seen:
        for side in ("left", "right"):
            c = nodes[nid][side]
            if c is not None:
                shown.append(c)
                S.nodes = [nodes[i] for i in sorted(shown)]
                S.add(f"{nodes[nid]['value']}.{side} = {nodes[c]['value']}.", c,
                      [i for i in shown if i != c])
    S.nodes = nodes
    S.add("Deserialised — the same tree.", None, list(range(len(nodes))))
    return bt.result(algo, S.steps, data)


def _morris(vals, algo):
    nodes = bt.build(vals)
    pre = algo == "morris_preorder"
    right = {n["id"]: n["right"] for n in nodes}   # mutable right pointers
    threads = set()
    S = bt.Stepper(nodes)
    S.counts = {"threads_made": 0, "visits": 0}
    out, done = [], []

    def add(note, cur):
        S.add(note, cur, list(done), threads=[list(t) for t in sorted(threads)])

    add("No stack, no recursion. At a node with a left child, find the "
        "rightmost node of the left subtree. No thread there yet → make one "
        "back to here (dashed) and go left. Thread already there → the left "
        "side is done: remove it and go right.", 0)
    cur = 0
    while cur is not None:
        v = nodes[cur]["value"]
        if nodes[cur]["left"] is None:
            out.append(v)
            done.append(cur)
            S.counts["visits"] += 1
            add(f"{v} has no left child — visit it ({out}), go right.", cur)
            cur = right[cur]
            continue
        p = nodes[cur]["left"]
        while right[p] is not None and right[p] != cur:
            p = right[p]
        if right[p] is None:
            right[p] = cur
            threads.add((p, cur))
            S.counts["threads_made"] += 1
            if pre:
                out.append(v)
                done.append(cur)
                S.counts["visits"] += 1
            add(f"Rightmost of {v}'s left subtree is {nodes[p]['value']}: thread "
                f"it back to {v}" + (f", visit {v} now ({out})" if pre else "")
                + ", go left.", cur)
            cur = nodes[cur]["left"]
        else:
            right[p] = None
            threads.discard((p, cur))
            if not pre:
                out.append(v)
                done.append(cur)
                S.counts["visits"] += 1
            add(f"Back at {v} through the thread from {nodes[p]['value']}: the "
                f"left side is finished. Remove the thread"
                + ("" if pre else f", visit {v} ({out})") + ", go right.", cur)
            cur = right[cur]
    add(f"{'Preorder' if pre else 'Inorder'}: {out}. Every thread was removed — "
        f"the tree is unchanged.", None)
    return bt.result(algo, S.steps, out)


def _flatten(vals, algo):
    nodes = bt.build(vals)
    S = bt.Stepper(nodes)
    S.counts = {"splices": 0}
    pre = []

    def walk(n):
        if n is not None:
            pre.append(nodes[n]["value"])
            walk(nodes[n]["left"])
            walk(nodes[n]["right"])
    walk(0)
    S.add("Target: every node's right pointer follows preorder, left pointers "
          "null. At each node with a left child, splice the left subtree in "
          "between the node and its right subtree.", 0)
    cur, done = 0, []
    while cur is not None:
        n = nodes[cur]
        if n["left"] is not None:
            p = n["left"]
            while nodes[p]["right"] is not None:
                p = nodes[p]["right"]
            nodes[p]["right"] = n["right"]
            n["right"], n["left"] = n["left"], None
            S.counts["splices"] += 1
            _layout(nodes, 0)
            S.add(f"{n['value']} has a left subtree: its rightmost node "
                  f"{nodes[p]['value']} now points at {n['value']}'s old right "
                  f"subtree, and the left subtree moves to the right.", cur, done)
        done.append(cur)
        cur = n["right"]
    S.add(f"Flattened: {pre} — a right-leaning chain in preorder.", None, done)
    return bt.result(algo, S.steps, pre)


def _side_by_side(a, b):
    """Shift b's ids after a's and squeeze a left, b right."""
    off = len(a)
    for n in b:
        n["id"] += off
        n["left"] = n["left"] + off if n["left"] is not None else None
        n["right"] = n["right"] + off if n["right"] is not None else None
    for n in a:
        n["x"] = n["x"] * 0.46
    for n in b:
        n["x"] = 0.54 + n["x"] * 0.46
    return a + b, off


def _identical(ta, tb):
    nodes, off = _side_by_side(bt.build(ta), bt.build(tb))
    S = bt.Stepper(nodes)
    S.counts = {"comparisons": 0}
    S.add("Walk both trees together: two nodes match if both are missing, or "
          "both exist with equal values and matching left and right subtrees.")
    ok = []

    def same(x, y):
        S.counts["comparisons"] += 1
        if x is None and y is None:
            return True
        if x is None or y is None:
            present = x if x is not None else y
            S.add(f"One tree has {nodes[present]['value']} here, the other has no "
                  f"node — different shapes.", present, ok, found=False)
            return False
        if nodes[x]["value"] != nodes[y]["value"]:
            S.add(f"{nodes[x]['value']} ≠ {nodes[y]['value']} — not identical.", x,
                  ok + [y], found=False)
            return False
        ok.extend([x, y])
        S.add(f"Both have {nodes[x]['value']} — compare their subtrees.", x, ok)
        return same(nodes[x]["left"], nodes[y]["left"]) and \
            same(nodes[x]["right"], nodes[y]["right"])

    res = same(0, off)
    if res:
        S.add("Every pair matched — the trees are identical.", None, ok)
    return bt.result("identical_trees", S.steps, res)


def _merge_bsts(x, y):
    na, ra = _bst_build(x)
    nb, rb = _bst_build(y)
    _layout(na, ra)
    _layout(nb, rb)
    nodes, off = _side_by_side(na, nb)
    S = bt.Stepper(nodes)
    S.counts = {"visits": 0, "comparisons": 0}
    S.add("An inorder walk of a BST gives its values sorted. Take both inorders, "
          "then merge the two sorted lists like merge sort does.")

    def inorder(nid, out, label):
        if nid is None:
            return
        inorder(nodes[nid]["left"], out, label)
        out.append(nid)
        S.counts["visits"] += 1
        S.add(f"Inorder of {label}: {[nodes[i]['value'] for i in out]}.", nid,
              out[:-1])
        inorder(nodes[nid]["right"], out, label)

    ia, ib = [], []
    inorder(ra, ia, "BST 1")
    inorder(rb + off, ib, "BST 2")
    i = j = 0
    merged, taken = [], []
    while i < len(ia) or j < len(ib):
        both = i < len(ia) and j < len(ib)
        if both:
            S.counts["comparisons"] += 1
        if j >= len(ib) or (both and nodes[ia[i]]["value"] <= nodes[ib[j]]["value"]):
            nid, i = ia[i], i + 1
        else:
            nid, j = ib[j], j + 1
        merged.append(nodes[nid]["value"])
        taken.append(nid)
        S.add(f"Take the smaller front value {nodes[nid]['value']} → {merged}.", nid,
              taken[:-1])
    S.add(f"Merged: {merged}.", None, taken)
    return bt.result("merge_two_bsts", S.steps, merged)
