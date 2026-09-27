"""Heap problems (Step 11).

On the `tree` view (the array read as a complete binary tree — index i has
children 2i+1 and 2i+2):
* is_min_heap — every parent must be ≤ both children.
* min_to_max_heap — heapify bottom-up: sift each internal node down, from the
  last parent back to the root, swapping with its bigger child.
* connect_sticks — always join the two cheapest sticks (a min-heap pops them);
  the joined stick goes back in. The heap shrinks by one each round.

On the `grid` view:
* rank_replace — sort the distinct values; each element becomes its rank.
* top_k_frequent — count, then keep a size-k min-heap of (count, value).
* hand_of_straights — greedily start every group at the smallest card left.
* task_scheduler — each tick run the most frequent task that isn't cooling
  down; idle when none can run.
* median_stream — a max-heap for the lower half, a min-heap for the upper
  half, kept balanced; the median sits on top.
"""

import heapq
from collections import Counter

from app.tracers import bt_common as bt
from app.tracers.grid_common import Grid

TITLES = {
    "is_min_heap": "Check if an Array is a Min-Heap",
    "min_to_max_heap": "Convert a Min-Heap to a Max-Heap",
    "connect_sticks": "Minimum Cost to Connect Sticks",
    "rank_replace": "Replace Elements by Their Rank",
    "top_k_frequent": "Top K Frequent Elements",
    "hand_of_straights": "Hand of Straights",
    "task_scheduler": "Task Scheduler",
    "median_stream": "Find Median From a Data Stream",
}
TREE_IDS = {"is_min_heap", "min_to_max_heap", "connect_sticks"}
MAX_LEN = 12


def _nums(text, lo=-999, hi=999):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= MAX_LEN) or any(not (lo <= v <= hi) for v in a):
        raise ValueError(f"Give 1–{MAX_LEN} numbers, each {lo}–{hi}.")
    return a


def run(algo, text, target=None):
    if algo == "task_scheduler":
        tasks = [t for t in (text or "").replace(" ", "").upper().split(",") if t]
        if not (1 <= len(tasks) <= 12) or any(len(t) != 1 or not t.isalpha() for t in tasks):
            raise ValueError("Give 1–12 tasks as single letters, e.g. A,A,B.")
        if target is None or target != int(target) or not (0 <= target <= 4):
            raise ValueError("The cooldown n must be 0–4.")
        return _scheduler(tasks, int(target))
    a = _nums(text, 1 if algo == "connect_sticks" else -999)
    if algo in ("top_k_frequent", "hand_of_straights"):
        if target is None or target != int(target) or not (1 <= target <= len(a)):
            raise ValueError(f"The group size / k must be 1–{len(a)}.")
        return (_topk if algo == "top_k_frequent" else _straights)(a, int(target))
    return {"is_min_heap": _is_min, "min_to_max_heap": _to_max,
            "connect_sticks": _sticks, "rank_replace": _ranks,
            "median_stream": _median}[algo](a)


def _is_min(a):
    nodes = bt.build(list(a))
    s = bt.Stepper(nodes)
    s.counts = {"checks": 0}
    ok_nodes: list = []
    s.add("Read the array as a complete tree (children of i are 2i+1, 2i+2). "
          "A min-heap needs every parent ≤ its children.")
    res = True
    for i in range(len(a) // 2):
        for c in (2 * i + 1, 2 * i + 2):
            if c < len(a):
                s.counts["checks"] += 1
                if a[i] > a[c]:
                    res = False
                    s.add(f"Parent {a[i]} (index {i}) > child {a[c]} (index {c}) — "
                          f"not a min-heap.", c, ok_nodes, found=False)
                    break
        if not res:
            break
        ok_nodes.append(i)
        s.add(f"{a[i]} (index {i}) is ≤ its children.", i, ok_nodes)
    if res:
        s.add("Every parent is ≤ its children — a valid min-heap.",
              None, list(range(len(a))), found=True)
    return bt.result("is_min_heap", s.steps, res)


def _to_max(a):
    nodes = bt.build(list(a))
    s = bt.Stepper(nodes)
    s.counts = {"swaps": 0}
    arr = a[:]
    n = len(arr)
    s.add("Ignore the min-heap order and heapify from scratch: sift each "
          "internal node down, from the last parent up to the root. O(n).")
    for start in range(n // 2 - 1, -1, -1):
        i = start
        while True:
            l, r, big = 2 * i + 1, 2 * i + 2, i
            if l < n and arr[l] > arr[big]:
                big = l
            if r < n and arr[r] > arr[big]:
                big = r
            if big == i:
                s.add(f"{arr[i]} (index {i}) is ≥ its children — settled.", i,
                      list(range(start, n)))
                break
            arr[i], arr[big] = arr[big], arr[i]
            nodes[i]["value"], nodes[big]["value"] = arr[i], arr[big]
            s.counts["swaps"] += 1
            s.add(f"Swap {arr[big]} down with its bigger child {arr[i]}.", big,
                  list(range(start, n)))
            i = big
    s.add(f"Max-heap: {arr}.", None, list(range(n)), found=True)
    return bt.result("min_to_max_heap", s.steps, arr)


def _sticks(a):
    heap = sorted(a)
    s = bt.Stepper(bt.build(heap))
    s.counts = {"joins": 0, "cost": 0}
    s.add("Joining two sticks costs their total length. Always join the two "
          "cheapest (a min-heap pops them), then push the result back.", 0)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x + y)
        s.counts["joins"] += 1
        s.counts["cost"] += x + y
        s.nodes = bt.build(heap)
        s.add(f"Pop {x} and {y}, join them for {x + y} (total cost "
              f"{s.counts['cost']}), push {x + y} back.", heap.index(x + y))
    s.add(f"One stick left. Minimum total cost: {s.counts['cost']}.", 0,
          [0], found=True)
    return bt.result("connect_sticks", s.steps, s.counts["cost"])


def _ranks(a):
    G = Grid(2, len(a))
    G.grid[0] = a[:]
    rank = {v: i + 1 for i, v in enumerate(sorted(set(a)))}
    G.counts = {"distinct": len(rank)}
    G.add(f"Sort the distinct values {sorted(rank)}; the smallest gets rank 1. "
          f"(A min-heap popping them in order does the same job.)")
    for i, v in enumerate(a):
        G.grid[1][i] = rank[v]
        G.add(f"{v} has rank {rank[v]}.", 1, i, [(0, i)])
    res = [rank[v] for v in a]
    G.add(f"Ranks: {res}.", path=[(1, i) for i in range(len(a))])
    return G.result("rank_replace", res, ["value", "rank"])


def _topk(a, k):
    cnt = Counter(a)
    vals = sorted(cnt)
    G = Grid(2, len(vals))
    G.grid[0] = vals[:]
    G.counts = {"heap_size": 0}
    G.add("First count every value, then keep a min-heap of the k best "
          "(count, value) pairs — the weakest sits on top and is evicted.")
    heap: list = []
    for i, v in enumerate(vals):
        G.grid[1][i] = cnt[v]
        heapq.heappush(heap, (cnt[v], -v))
        note = f"{v} appears {cnt[v]} time(s); push it."
        if len(heap) > k:
            c, nv = heapq.heappop(heap)
            note += f" Heap over size {k}: evict {-nv} (count {c})."
        G.counts["heap_size"] = len(heap)
        G.add(note + f" Heap: {sorted(-nv for c, nv in heap)}.", 1, i, [(0, i)])
    res = sorted((-nv for c, nv in heap), key=lambda v: (-cnt[v], v))
    G.add(f"Top {k} frequent: {res}.", path=[(1, vals.index(v)) for v in res])
    return G.result("top_k_frequent", res, ["value", "count"])


def _straights(a, g):
    cnt = Counter(a)
    vals = sorted(cnt)
    G = Grid(2, len(vals))
    G.grid[0] = vals[:]
    G.grid[1] = [cnt[v] for v in vals]
    G.counts = {"groups": 0}
    G.add(f"Groups of {g} consecutive cards. The smallest card left must start "
          f"a group (nothing smaller can take it), so start there each time.")
    res = True
    if len(a) % g:
        res = False
        G.add(f"{len(a)} cards can't split into groups of {g}.", match=False)
    while res and any(cnt[v] for v in vals):
        start = next(v for v in vals if cnt[v])
        for v in range(start, start + g):
            if cnt.get(v, 0) == 0:
                res = False
                G.add(f"Group starting at {start} needs {v}, but none is left.",
                      match=False)
                break
            cnt[v] -= 1
            G.grid[1][vals.index(v)] = cnt[v]
        if res:
            G.counts["groups"] += 1
            cols = [vals.index(v) for v in range(start, start + g)]
            G.add(f"Group {list(range(start, start + g))} formed.", 1, cols[0],
                  deps=[(1, c) for c in cols])
    if res:
        G.add(f"All cards grouped — {G.counts['groups']} straight(s).")
    return G.result("hand_of_straights", res, ["card", "left"])


def _scheduler(tasks, n):
    cnt = Counter(tasks)
    heap = [(-c, t) for t, c in cnt.items()]
    heapq.heapify(heap)
    cooling: list = []            # (ready_time, -count, task)
    timeline: list = []
    time = 0
    while heap or cooling:
        while cooling and cooling[0][0] <= time:
            _, c, t = heapq.heappop(cooling)
            heapq.heappush(heap, (c, t))
        if heap:
            c, t = heapq.heappop(heap)
            timeline.append(t)
            if c + 1 < 0:
                heapq.heappush(cooling, (time + n + 1, c + 1, t))
        else:
            timeline.append("idle")
        time += 1
    G = Grid(1, len(timeline))
    G.counts = {"ticks": 0, "idle": 0}
    G.add(f"Tasks {dict(sorted(cnt.items()))}, cooldown {n}. Each tick, run the "
          f"most frequent task that isn't cooling down; if none can run, idle.")
    for i, t in enumerate(timeline):
        G.grid[0][i] = t if t != "idle" else "·"
        G.counts["ticks"] += 1
        G.counts["idle"] += t == "idle"
        G.add(f"Tick {i}: " + ("idle — every remaining task is cooling down."
                               if t == "idle" else f"run {t}."), 0, i,
              match=t != "idle")
    G.add(f"Finished in {len(timeline)} ticks ({G.counts['idle']} idle).")
    return G.result("task_scheduler", len(timeline), ["tick"])


def _median(a):
    n = len(a)
    G = Grid(4, n)
    G.counts = {"rebalances": 0}
    low: list = []   # max-heap (negated)
    high: list = []  # min-heap
    res = []
    G.add("Lower half in a max-heap, upper half in a min-heap, sizes within "
          "one. The median is the top of the bigger heap (or the average of "
          "both tops).")
    for i, x in enumerate(a):
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
            G.counts["rebalances"] += 1
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
            G.counts["rebalances"] += 1
        med = -low[0] if len(low) > len(high) else (-low[0] + high[0]) / 2
        med = int(med) if med == int(med) else med
        res.append(med)
        G.grid[0][i] = x
        G.grid[1][i] = ",".join(str(v) for v in sorted(-v for v in low))
        G.grid[2][i] = ",".join(str(v) for v in sorted(high)) or "—"
        G.grid[3][i] = med
        G.add(f"Add {x}. Lower half {sorted(-v for v in low)}, upper half "
              f"{sorted(high)} → median {med}.", 3, i, [(1, i), (2, i)])
    G.add(f"Medians after each number: {res}.", path=[(3, i) for i in range(n)])
    return G.result("median_stream", res, ["incoming", "low (max-heap)",
                                            "high (min-heap)", "median"])
