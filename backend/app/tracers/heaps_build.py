"""Heap construction (Heaps / Theory and Implementation).

On the `tree` view — the array read as a complete binary tree, index i has
children 2i+1 and 2i+2 (node ids are array indices):
* heapify — sift one node down until both children are smaller (max-heap).
* build_heap — call heapify on every internal node from the last parent
  back to the root; O(n), not O(n log n).

On the `grid` view:
* sort_k_sorted — every element is at most k places from its sorted spot,
  so a min-heap of k+1 elements always has the next smallest on top.
"""

import heapq

from app.tracers import bt_common as bt
from app.tracers.grid_common import Grid

TITLES = {
    "heapify": "Heapify (Sift Down)",
    "build_heap": "Build a Max-Heap From an Array",
    "sort_k_sorted": "Sort a K-Sorted Array",
}


def _nums(text, n_max=12):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n_max) or any(abs(v) > 999 for v in a):
        raise ValueError(f"Give 1–{n_max} numbers within ±999.")
    return a


def run(algo, text, target=None):
    tree_text, extra = bt.split_query(text)
    a = _nums(tree_text)
    if algo == "heapify":
        if len(extra) != 1:
            raise ValueError("Add '| i' — the index to sift down, e.g. 4,10,3,5,1 | 0.")
        i = extra[0]
        if not (0 <= i < len(a)):
            raise ValueError(f"Index must be 0–{len(a) - 1}.")
        return _heapify(a, i)
    if algo == "sort_k_sorted":
        if len(extra) != 1:
            raise ValueError("Add '| k', e.g. 6,5,3,2,8,10,9 | 3.")
        k = extra[0]
        if not (0 <= k < len(a)):
            raise ValueError(f"k must be 0–{len(a) - 1}.")
        s = sorted(a)
        if any(abs(s.index(v) - i) > k for i, v in enumerate(a) if a.count(v) == 1):
            raise ValueError(f"Some element is more than {k} places from its sorted spot.")
        return _sort_k(a, k)
    if extra:
        raise ValueError("This one takes only the array.")
    return _build(a)


def _sift(s, nodes, arr, i, start, n):
    while True:
        l, r, big = 2 * i + 1, 2 * i + 2, i
        if l < n and arr[l] > arr[big]:
            big = l
        if r < n and arr[r] > arr[big]:
            big = r
        if big == i:
            s.add(f"{arr[i]} (index {i}) is ≥ its children — settled.", i,
                  list(range(start, n)))
            return
        arr[i], arr[big] = arr[big], arr[i]
        nodes[i]["value"], nodes[big]["value"] = arr[i], arr[big]
        s.counts["swaps"] += 1
        s.add(f"Swap {arr[big]} down with its bigger child {arr[i]}.", big,
              list(range(start, n)))
        i = big


def _heapify(a, i):
    nodes = bt.build(list(a))
    s = bt.Stepper(nodes)
    s.counts = {"swaps": 0}
    arr, n = a[:], len(a)
    s.add(f"heapify(i = {i}): compare {arr[i]} with its children and sink it "
          f"until it is the largest of the three.", i)
    _sift(s, nodes, arr, i, i, n)
    s.add(f"Subtree at {i} is a max-heap: {arr}.", None, list(range(i, n)), found=True)
    return bt.result("heapify", s.steps, arr)


def _build(a):
    nodes = bt.build(list(a))
    s = bt.Stepper(nodes)
    s.counts = {"swaps": 0, "heapify_calls": 0}
    arr, n = a[:], len(a)
    s.add(f"Leaves (indices {n // 2}–{n - 1}) are already heaps. Heapify each "
          f"internal node from the last parent ({n // 2 - 1}) back to the root.")
    for start in range(n // 2 - 1, -1, -1):
        s.counts["heapify_calls"] += 1
        s.add(f"heapify({start}) on value {arr[start]}.", start, list(range(start + 1, n)))
        _sift(s, nodes, arr, start, start, n)
    s.add(f"Max-heap: {arr}. Total work is O(n) — most nodes sit near the bottom.",
          None, list(range(n)), found=True)
    return bt.result("build_heap", s.steps, arr)


def _sort_k(a, k):
    n = len(a)
    G = Grid(3, n)
    G.grid = [a[:], [None] * n, [None] * n]
    G.counts = {"pushed": 0, "popped": 0}
    heap: list = []
    out: list = []
    G.add(f"Each value is at most {k} places off. Keep a min-heap of {k + 1} values: "
          f"its top is always the next smallest.")
    for i, v in enumerate(a):
        heapq.heappush(heap, v)
        G.counts["pushed"] += 1
        hv = sorted(heap)
        G.grid[1] = hv + [None] * (n - len(hv))
        G.add(f"Push {v}; heap {hv}.", 0, i, deps=[(1, c) for c in range(len(hv))],
              path=[(2, c) for c in range(len(out))])
        if len(heap) > k:
            x = heapq.heappop(heap)
            out.append(x)
            G.counts["popped"] += 1
            hv = sorted(heap)
            G.grid[1] = hv + [None] * (n - len(hv))
            G.grid[2][len(out) - 1] = x
            G.add(f"Heap has {k + 1} — pop the min {x} into the output.", 2, len(out) - 1,
                  deps=[(1, c) for c in range(len(hv))], path=[(2, c) for c in range(len(out))])
    while heap:
        x = heapq.heappop(heap)
        out.append(x)
        G.counts["popped"] += 1
        hv = sorted(heap)
        G.grid[1] = hv + [None] * (n - len(hv))
        G.grid[2][len(out) - 1] = x
        G.add(f"Drain the heap: pop {x}.", 2, len(out) - 1, path=[(2, c) for c in range(len(out))])
    G.add(f"Sorted: {out}. O(n log k).", path=[(2, c) for c in range(n)])
    return G.result("sort_k_sorted", out, ["input", "heap", "output"])
