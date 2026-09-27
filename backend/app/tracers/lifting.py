"""Binary lifting (batch 72) on the `tree` view — jump pointers are drawn as
dashed `threads`.

up[0][v] is v's parent; up[k][v] = up[k−1][up[k−1][v]] is its 2^k-th
ancestor. Any jump of d levels is a sum of powers of two, so it takes at most
log n hops.

* kth_ancestor — hop by the set bits of k.
* lca_lifting — lift the deeper node to the same depth, then for k from
  high to low jump BOTH nodes while their 2^k-th ancestors differ; the LCA
  is then the parent of either.
"""

from app.tracers import bt_common as bt

TITLES = {
    "lca_lifting": "Lowest Common Ancestor (Binary Lifting)",
    "kth_ancestor": "K-th Ancestor (Binary Lifting)",
}


def run(algo, text, target=None):
    tree_t, extra = bt.split_query(text)
    vals = bt.parse(tree_t)
    real = [v for v in vals if v is not None]
    if len(set(real)) != len(real):
        raise ValueError("Node values must be distinct.")
    if len(extra) != 2:
        raise ValueError("After '|', give two numbers: " +
                         ("the two nodes, e.g. | 4 5." if algo == "lca_lifting"
                          else "the node and k, e.g. | 7 2."))
    nodes = bt.build(vals)
    by_val = {n["value"]: n["id"] for n in nodes}
    if algo == "lca_lifting":
        a, b = extra
        if a not in by_val or b not in by_val:
            raise ValueError("Both nodes must be in the tree.")
        return _lift(nodes, by_val[a], by_val[b], None)
    v, k = extra
    if v not in by_val or not (0 <= k <= 15):
        raise ValueError("The node must be in the tree and k within 0–15.")
    return _lift(nodes, by_val[v], None, k)


def _lift(nodes, a, b, k):
    n = len(nodes)
    parent = [None] * n
    for x in nodes:
        for c in (x["left"], x["right"]):
            if c is not None:
                parent[c] = x["id"]
    depth = [x["depth"] for x in nodes]
    LOG = max(1, max(depth).bit_length())
    up = [list(parent)]
    S = bt.Stepper(nodes)
    S.counts = {"table_cells": 0, "jumps": 0}
    S.add(f"Precompute jump pointers: up[0][v] is v's parent, and "
          f"up[k][v] = up[k−1][up[k−1][v]] — two 2^(k−1) jumps make one 2^k jump. "
          f"Depth ≤ {max(depth)}, so {LOG} level(s) are enough.")
    for lvl in range(LOG):
        if lvl:
            up.append([up[lvl - 1][up[lvl - 1][v]] if up[lvl - 1][v] is not None
                       else None for v in range(n)])
        S.counts["table_cells"] += n
        threads = [[v, up[lvl][v]] for v in range(n) if up[lvl][v] is not None]
        S.add(f"up[{lvl}]: every node's 2^{lvl} = {1 << lvl}-th ancestor (dashed).",
              None, [], threads=threads)
    val = lambda v: nodes[v]["value"]

    def jump(v, j, why, marked):
        S.counts["jumps"] += 1
        S.add(f"{why}: {val(v)} → up[{j}] = {val(up[j][v])} ({1 << j} level(s) up).",
              up[j][v], marked, threads=[[v, up[j][v]]])
        return up[j][v]

    if b is None:                                   # k-th ancestor
        v = a
        S.add(f"k = {k} = {bin(k)[2:]} in binary: hop by each set bit.", v, [])
        if k > depth[v]:
            S.add(f"{val(v)} is only {depth[v]} level(s) deep — no {k}-th "
                  f"ancestor (−1).", v, [], found=False)
            return bt.result("kth_ancestor", S.steps, -1)
        for j in range(LOG):
            if k >> j & 1:
                v = jump(v, j, f"bit {j} of k is set", [a])
        S.add(f"The {k}-th ancestor is {val(v)}.", v, [a], found=True)
        return bt.result("kth_ancestor", S.steps, val(v))

    marked = [a, b]
    if depth[a] < depth[b]:
        a, b = b, a
    diff = depth[a] - depth[b]
    S.add(f"{val(a)} is at depth {depth[a]}, {val(b)} at depth {depth[b]}: first "
          f"lift {val(a)} by {diff} to the same depth.", a, marked)
    for j in range(LOG):
        if diff >> j & 1:
            a = jump(a, j, f"bit {j} of {diff}", marked)
    if a == b:
        S.add(f"They meet at {val(a)} — it is the LCA.", a, marked, found=True)
        return bt.result("lca_lifting", S.steps, val(a))
    for j in range(LOG - 1, -1, -1):
        if up[j][a] is not None and up[j][a] != up[j][b]:
            S.counts["jumps"] += 2
            S.add(f"up[{j}] differs ({val(up[j][a])} vs {val(up[j][b])}) — both jump "
                  f"{1 << j} level(s).", up[j][a], marked,
                  threads=[[a, up[j][a]], [b, up[j][b]]])
            a, b = up[j][a], up[j][b]
        else:
            S.add(f"up[{j}] would land both on the same node (or past the root) — "
                  f"too far, don't jump.", a, marked)
    lca = parent[a]
    S.add(f"{val(a)} and {val(b)} are now just below their meeting point: "
          f"the LCA is their parent, {val(lca)}.", lca, marked + [a, b], found=True)
    return bt.result("lca_lifting", S.steps, val(lca))
