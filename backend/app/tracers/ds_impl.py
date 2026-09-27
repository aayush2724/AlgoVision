"""Implementing stacks, queues and caches (Steps 9, 11) — the input is a
script of operations, e.g. "push 3, push 5, pop, top". Every operation is
one step; the result lists what the reading operations returned (None when
the structure was empty, −1 for a cache miss).

Grid view: stack_array (top index), queue_array (circular front/rear),
stack_using_queue (rotate after push), queue_using_stacks (in/out stacks,
move only when out is empty), min_stack (each entry remembers the minimum
below it), lru_cache (recency order), lfu_cache (frequency, then recency),
design_twitter (merge the newest tweets of a user and their followees).

List view: stack_linkedlist (push/pop at the head), queue_linkedlist
(enqueue at the rear, dequeue at the front).
"""

from app.tracers.grid_common import Grid

TITLES = {
    "stack_array": "Implement a Stack Using an Array",
    "queue_array": "Implement a Queue Using an Array",
    "stack_using_queue": "Implement a Stack Using a Queue",
    "queue_using_stacks": "Implement a Queue Using Stacks",
    "min_stack": "Implement a Min Stack",
    "lru_cache": "LRU Cache",
    "lfu_cache": "LFU Cache",
    "design_twitter": "Design Twitter",
    "stack_linkedlist": "Implement a Stack Using a Linked List",
    "queue_linkedlist": "Implement a Queue Using a Linked List",
}
OPS = {
    "stack_array": {"push": 1, "pop": 0, "top": 0},
    "queue_array": {"push": 1, "pop": 0, "front": 0},
    "stack_using_queue": {"push": 1, "pop": 0, "top": 0},
    "queue_using_stacks": {"push": 1, "pop": 0, "front": 0},
    "min_stack": {"push": 1, "pop": 0, "top": 0, "getmin": 0},
    "lru_cache": {"put": 2, "get": 1},
    "lfu_cache": {"put": 2, "get": 1},
    "design_twitter": {"post": 2, "follow": 2, "unfollow": 2, "feed": 1},
    "stack_linkedlist": {"push": 1, "pop": 0, "top": 0},
    "queue_linkedlist": {"push": 1, "pop": 0, "front": 0},
}
NEEDS_CAP = {"stack_array", "queue_array", "lru_cache", "lfu_cache"}
MAX_OPS = 14


def _script(algo, text):
    ops = []
    for part in [p.strip() for p in (text or "").split(",") if p.strip()]:
        words = part.lower().split()
        name, args = words[0], words[1:]
        name = {"enqueue": "push", "dequeue": "pop", "poll": "pop"}.get(name, name)
        if name == "peek":
            name = "top" if "top" in OPS[algo] else "front"
        want = OPS[algo].get(name)
        if want is None:
            raise ValueError(f"Unknown operation '{words[0]}'. Use: {', '.join(OPS[algo])}.")
        try:
            nums = [int(x) for x in args]
        except ValueError:
            raise ValueError(f"'{part}': arguments must be whole numbers.") from None
        if len(nums) != want or any(abs(v) > 999 for v in nums):
            raise ValueError(f"'{part}': {name} takes {want} number(s) within ±999.")
        ops.append((name, nums))
    if not (1 <= len(ops) <= MAX_OPS):
        raise ValueError(f"Give 1–{MAX_OPS} operations separated by commas.")
    return ops


def run(algo, text, target=None):
    ops = _script(algo, text)
    if algo in NEEDS_CAP:
        if target is None or target != int(target) or not (1 <= target <= 6):
            raise ValueError("Capacity must be 1–6.")
        return globals()["_" + algo](ops, int(target))
    return globals()["_" + algo](ops)


def _show(v):
    return "∅" if v is None else v


def _pad(xs, w):
    return (list(xs) + [None] * w)[:w]


# ── array-backed ───────────────────────────────────────────────────────
def _stack_array(ops, cap):
    G = Grid(1, cap)
    G.counts = {"size": 0}
    arr, top, out = [None] * cap, -1, []
    G.add(f"An array of {cap} slots and a 'top' index (−1 = empty). push "
          f"writes at top + 1; pop reads arr[top] and moves top down.")
    for name, a in ops:
        if name == "push":
            if top == cap - 1:
                G.add(f"push {a[0]}: top = {top} is the last slot — overflow.",
                      match=False)
                continue
            top += 1
            arr[top] = a[0]
            note = f"push {a[0]}: top → {top}, arr[{top}] = {a[0]}."
        elif top == -1:
            out.append(None)
            G.add(f"{name}: top = −1 — the stack is empty.", match=False)
            continue
        elif name == "pop":
            out.append(arr[top])
            note = f"pop → {arr[top]}; top → {top - 1}."
            arr[top] = None
            top -= 1
        else:
            out.append(arr[top])
            note = f"top → {arr[top]} (arr[{top}])."
        G.grid[0] = arr[:]
        G.counts["size"] = top + 1
        G.add(note, 0, top if top >= 0 else None,
              path=[(0, j) for j in range(top + 1)])
    G.add(f"Returned: {[_show(v) for v in out]}.")
    return G.result("stack_array", out, ["slots"])


def _queue_array(ops, cap):
    G = Grid(1, cap)
    G.counts = {"size": 0}
    arr, front, size, out = [None] * cap, 0, 0, []
    G.add(f"A circular array of {cap} slots: 'front' is the next to leave, "
          f"rear = (front + size) mod {cap} is where the next arrival goes. "
          f"Indices wrap around, so freed slots get reused.")
    for name, a in ops:
        if name == "push":
            if size == cap:
                G.add(f"push {a[0]}: all {cap} slots are used — overflow.", match=False)
                continue
            rear = (front + size) % cap
            arr[rear] = a[0]
            size += 1
            note, col = f"push {a[0]} at rear index {rear}.", rear
        elif size == 0:
            out.append(None)
            G.add(f"{name}: size 0 — the queue is empty.", match=False)
            continue
        elif name == "pop":
            out.append(arr[front])
            note, col = (f"pop → {arr[front]} from front index {front}; front → "
                         f"{(front + 1) % cap}."), front
            arr[front] = None
            front = (front + 1) % cap
            size -= 1
        else:
            out.append(arr[front])
            note, col = f"front → {arr[front]} (index {front}).", front
        G.grid[0] = arr[:]
        G.counts["size"] = size
        G.add(note, 0, col, path=[(0, (front + k) % cap) for k in range(size)])
    G.add(f"Returned: {[_show(v) for v in out]}.")
    return G.result("queue_array", out, ["slots"])


def _width(ops):
    return max(1, sum(1 for n, _ in ops if n == "push"))


def _stack_using_queue(ops):
    w = _width(ops)
    G = Grid(1, w)
    G.counts = {"rotations": 0}
    q, out = [], []
    G.add("One queue (front on the left). After pushing x, rotate the older "
          "items behind it — x ends up at the front, so the front is always "
          "the stack's top.")
    for name, a in ops:
        if name == "push":
            q.append(a[0])
            G.grid[0] = _pad(q, w)
            G.add(f"push {a[0]}: enqueue at the back.", 0, len(q) - 1)
            for _ in range(len(q) - 1):
                q.append(q.pop(0))
                G.counts["rotations"] += 1
            G.grid[0] = _pad(q, w)
            G.add(f"Rotate {len(q) - 1} older item(s) behind it — {a[0]} is at the "
                  f"front.", 0, 0, path=[(0, 0)])
        elif not q:
            out.append(None)
            G.add(f"{name}: the queue is empty.", match=False)
        else:
            out.append(q[0])
            if name == "pop":
                q.pop(0)
            G.grid[0] = _pad(q, w)
            G.add(f"{name} → {out[-1]} (the front).", 0, 0 if q else None)
    G.add(f"Returned: {[_show(v) for v in out]}.")
    return G.result("stack_using_queue", out, ["queue"])


def _queue_using_stacks(ops):
    w = _width(ops)
    G = Grid(2, w)
    G.counts = {"moves": 0}
    ins, outs, res = [], [], []

    def draw():
        G.grid = [_pad(ins, w), _pad(outs, w)]

    G.add("Two stacks (bottom on the left). push goes onto 'in'. pop/front "
          "read 'out' — only when 'out' is empty, pour all of 'in' into it, "
          "which reverses the order. Each item moves once: amortised O(1).")
    for name, a in ops:
        if name == "push":
            ins.append(a[0])
            draw()
            G.add(f"push {a[0]} onto in.", 0, len(ins) - 1)
            continue
        if not outs and ins:
            while ins:
                outs.append(ins.pop())
                G.counts["moves"] += 1
            draw()
            G.add("out is empty — pour in → out (the oldest is now on top).", 1,
                  len(outs) - 1)
        if not outs:
            res.append(None)
            G.add(f"{name}: both stacks are empty.", match=False)
            continue
        res.append(outs[-1])
        if name == "pop":
            outs.pop()
        draw()
        G.add(f"{name} → {res[-1]} (top of out).", 1, len(outs) - 1 if outs else None)
    G.add(f"Returned: {[_show(v) for v in res]}.")
    return G.result("queue_using_stacks", res, ["in", "out"])


def _min_stack(ops):
    w = _width(ops)
    G = Grid(2, w)
    G.counts = {"size": 0}
    st, out = [], []

    def draw():
        G.grid = [_pad([v for v, _ in st], w), _pad([m for _, m in st], w)]

    G.add("Store each value with the minimum of everything at or below it. The "
          "top pair then answers getMin in O(1), and a pop restores the old "
          "minimum automatically.")
    for name, a in ops:
        if name == "push":
            m = a[0] if not st else min(a[0], st[-1][1])
            st.append((a[0], m))
            draw()
            G.counts["size"] = len(st)
            G.add(f"push {a[0]}: minimum at or below it is {m}.", 1, len(st) - 1)
        elif not st:
            out.append(None)
            G.add(f"{name}: the stack is empty.", match=False)
        else:
            v, m = st[-1]
            out.append(m if name == "getmin" else v)
            if name == "pop":
                st.pop()
            draw()
            G.counts["size"] = len(st)
            col = len(st) - 1 if name != "pop" and st else None
            G.add(f"{name} → {out[-1]}.", 1 if name == "getmin" else 0, col)
    G.add(f"Returned: {[_show(v) for v in out]}.")
    return G.result("min_stack", out, ["value", "min"])


# ── caches ─────────────────────────────────────────────────────────────
def _lru_cache(ops, cap):
    G = Grid(1, cap)
    G.counts = {"evictions": 0}
    order, store, out = [], {}, []     # order: most recent first

    def draw():
        G.grid[0] = _pad([f"{k}:{store[k]}" for k in order], cap)

    G.add(f"Capacity {cap}. Keep keys in recency order (most recent on the "
          f"left) — a hash map plus a doubly linked list does both in O(1). "
          f"get and put both make a key most recent; a full put evicts the "
          f"rightmost (least recently used).")
    for name, a in ops:
        k = a[0]
        if name == "get":
            if k in store:
                order.remove(k)
                order.insert(0, k)
                out.append(store[k])
                draw()
                G.add(f"get {k} → {store[k]}; it becomes most recent.", 0, 0)
            else:
                out.append(-1)
                G.add(f"get {k} → −1 (not cached).", match=False)
            continue
        note = f"put {k}:{a[1]}"
        if k in store:
            order.remove(k)
            note += " — update the existing key"
        elif len(order) == cap:
            old = order.pop()
            del store[old]
            G.counts["evictions"] += 1
            note += f" — full, evict least recent key {old}"
        store[k] = a[1]
        order.insert(0, k)
        draw()
        G.add(note + ".", 0, 0)
    G.add(f"get results: {out}.")
    return G.result("lru_cache", out, ["recent → old"])


def _lfu_cache(ops, cap):
    G = Grid(3, cap)
    G.counts = {"evictions": 0}
    store, freq, last, out = {}, {}, {}, []

    def draw():
        keys = sorted(store, key=lambda k: (-freq[k], -last[k]))
        G.grid = [_pad([f"{k}:{store[k]}" for k in keys], cap),
                  _pad([freq[k] for k in keys], cap),
                  _pad([last[k] for k in keys], cap)]
        return keys

    G.add(f"Capacity {cap}. Every key counts its uses. A full put evicts the "
          f"key used LEAST often; ties go to the least recently used. "
          f"(Columns are sorted: most used on the left.)")
    for clock, (name, a) in enumerate(ops, 1):
        k = a[0]
        if name == "get":
            if k in store:
                freq[k] += 1
                last[k] = clock
                out.append(store[k])
                keys = draw()
                G.add(f"get {k} → {store[k]}; its count rises to {freq[k]}.", 1,
                      keys.index(k))
            else:
                out.append(-1)
                G.add(f"get {k} → −1 (not cached).", match=False)
            continue
        note = f"put {k}:{a[1]}"
        if k in store:
            freq[k] += 1
            note += f" — update; count {freq[k]}"
        else:
            if len(store) == cap:
                old = min(store, key=lambda x: (freq[x], last[x]))
                note += (f" — full, evict key {old} (used {freq[old]}×, the least "
                         f"recently used among the least used)")
                for d in (store, freq, last):
                    del d[old]
                G.counts["evictions"] += 1
            freq[k] = 1
        store[k] = a[1]
        last[k] = clock
        keys = draw()
        G.add(note + ".", 0, keys.index(k))
    G.add(f"get results: {out}.")
    return G.result("lfu_cache", out, ["key:value", "uses", "last used"])


def _design_twitter(ops):
    w = max(1, min(10, sum(1 for n, _ in ops if n == "post")))
    G = Grid(2, w)
    G.counts = {"tweets": 0}
    tweets, follows, feeds = [], {}, []    # tweets: (time, user, id)

    def draw(ids=()):
        recent = tweets[::-1][:w]
        G.grid = [_pad([f"#{t}" for _, _, t in recent], w),
                  _pad([f"u{u}" for _, u, _ in recent], w)]
        return [(0, j) for j, (_, _, t) in enumerate(recent) if t in ids]

    G.add("Store tweets with a timestamp (newest on the left) and a follow set "
          "per user. A feed = the 10 newest tweets by the user or anyone they "
          "follow — in code, a heap merges each author's newest-first list.")
    for time, (name, a) in enumerate(ops):
        if name == "post":
            u, t = a
            tweets.append((time, u, t))
            G.counts["tweets"] += 1
            draw()
            G.add(f"User {u} posts tweet {t}.", 0, 0)
        elif name == "follow":
            if a[0] != a[1]:
                follows.setdefault(a[0], set()).add(a[1])
            G.add(f"User {a[0]} follows {a[1]}. {a[0]} now follows "
                  f"{sorted(follows.get(a[0], ())) or 'nobody'}.")
        elif name == "unfollow":
            follows.get(a[0], set()).discard(a[1])
            G.add(f"User {a[0]} unfollows {a[1]}. {a[0]} now follows "
                  f"{sorted(follows.get(a[0], ())) or 'nobody'}.")
        else:
            u = a[0]
            who = {u} | follows.get(u, set())
            feed = [t for _, au, t in sorted(tweets, reverse=True) if au in who][:10]
            feeds.append(feed)
            cells = draw(set(feed))
            G.add(f"Feed of user {u} (self + {sorted(who - {u}) or 'nobody'}): {feed}.",
                  deps=cells, path=cells)
    G.add(f"Feeds returned: {feeds}.")
    return G.result("design_twitter", feeds, ["tweet", "author"])


# ── linked-list backed (list view) ─────────────────────────────────────
def _list_steps(ops, algo):
    queue = algo == "queue_linkedlist"
    items, out, steps = [], [], []
    counts = {"size": 0, "nodes_created": 0}

    def add(note, curr=None, removed=()):
        n = len(items)
        ptrs = [["front" if queue else "top", 0]] if n else []
        if queue and n:
            ptrs.append(["rear", n - 1])
        steps.append({"i": len(steps), "line": 0, "note": note,
                      "highlight": {"index": curr},
                      "structures": {"values": list(items),
                                     "next": [i + 1 if i < n - 1 else None for i in range(n)],
                                     "curr": curr, "removed": list(removed),
                                     "pointers": ptrs, "counts": dict(counts)}})

    add("Each item is a node; no fixed capacity. " +
        ("Enqueue links a new node after 'rear'; dequeue moves 'front' to the "
         "next node. Both O(1)." if queue else
         "push makes a new node point at the old top; pop moves 'top' to the "
         "next node. Both O(1)."))
    for name, a in ops:
        if name == "push":
            counts["nodes_created"] += 1
            if queue:
                items.append(a[0])
                counts["size"] = len(items)
                add(f"enqueue {a[0]}: rear.next = new node; rear moves to it.",
                    len(items) - 1)
            else:
                items.insert(0, a[0])
                counts["size"] = len(items)
                add(f"push {a[0]}: new node → old top; top moves to it.", 0)
        elif not items:
            out.append(None)
            add(f"{name}: {'front' if queue else 'top'} is null — empty.")
        elif name == "pop":
            out.append(items[0])
            add(f"{'dequeue' if queue else 'pop'} → {items[0]}: move "
                f"{'front' if queue else 'top'} to the next node.", 0, [0])
            items.pop(0)
            counts["size"] = len(items)
            add(f"The old node is freed. Size {len(items)}.", 0 if items else None)
        else:
            out.append(items[0])
            add(f"{name} → {items[0]}.", 0)
    add(f"Returned: {[_show(v) for v in out]}.")
    return {"meta": {"algorithm": algo, "view": "list", "language": "python",
                     "result": out},
            "array": steps[0]["structures"]["values"], "steps": steps}


def _stack_linkedlist(ops):
    return _list_steps(ops, "stack_linkedlist")


def _queue_linkedlist(ops):
    return _list_steps(ops, "queue_linkedlist")
