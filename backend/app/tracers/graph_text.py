"""Graph problems whose graph is *implied* by typed input (Step 15).

* word_ladder / word_ladder_ii — words are nodes, one-letter changes are
  edges. BFS from the start word gives the shortest transformation; the BFS
  tree is drawn level by level (tree view). Ladder II keeps every parent on
  a shortest layer, so every shortest sequence can be read back.
* alien_dictionary — each adjacent pair of sorted words reveals one letter
  order (at their first difference); Kahn's topological sort of those rules
  is the alphabet.
* cheapest_flight_k — Bellman-Ford limited to k+1 rounds (k stops): each round
  relaxes every flight from the previous round's prices only.
* ways_to_arrive — Dijkstra that also counts: an equal-length path adds its
  count, a shorter one replaces it.
* min_multiplications — BFS over values mod 100000: each multiplication by an
  allowed factor is one step.
* most_stones — stones sharing a row or a column are connected; each
  connected group can shrink to one stone, so the answer is stones − groups.

Grid tables for the rest (rows = rounds / BFS levels / nodes' dist & ways).
"""

import heapq

from app.tracers.grid_common import Grid
from app.tracers.recursion_tree import RecTree

TITLES = {
    "word_ladder": "Word Ladder I",
    "word_ladder_ii": "Word Ladder II (All Shortest Sequences)",
    "alien_dictionary": "Alien Dictionary",
    "cheapest_flight_k": "Cheapest Flights Within K Stops",
    "ways_to_arrive": "Number of Ways to Arrive at Destination",
    "min_multiplications": "Minimum Multiplications to Reach End",
    "most_stones": "Most Stones Removed With Same Row or Column",
}
TREE_IDS = {"word_ladder", "word_ladder_ii"}
MOD = 100000


def run(algo, text, target=None):
    raw = (text or "").replace(" ", "")
    if algo in TREE_IDS:
        return _ladder(algo, *_ladder_input(raw))
    if algo == "alien_dictionary":
        words = [w for w in raw.lower().split(",") if w]
        if not (2 <= len(words) <= 8) or any(not w.isalpha() or len(w) > 6 for w in words):
            raise ValueError("Give 2–8 words (letters, up to 6 each) in alien sorted order.")
        return _alien(words)
    if algo == "most_stones":
        try:
            stones = [tuple(int(v) for v in p.split(":")) for p in raw.split(",") if p]
        except ValueError:
            raise ValueError("Give stones as r:c, e.g. 0:0,0:1,1:0.") from None
        if not (1 <= len(stones) <= 12) or len(set(stones)) != len(stones) or \
                any(len(p) != 2 or not (0 <= p[0] <= 5 and 0 <= p[1] <= 5) for p in stones):
            raise ValueError("1–12 distinct stones, rows and columns 0–5.")
        return _stones(stones)
    if algo == "min_multiplications":
        usage = "Give 'start end | factors', e.g. 3 30 | 2,5,7."
        if "|" not in raw:
            raise ValueError(usage)
        head, facs = (text or "").split("|", 1)
        try:
            start, end = (int(x) for x in head.split())
            factors = [int(x) for x in facs.replace(" ", "").split(",") if x]
        except ValueError:
            raise ValueError(usage) from None
        if not (0 <= start < MOD and 0 <= end < MOD) or not (1 <= len(factors) <= 5) \
                or any(not (1 <= f <= 9999) for f in factors):
            raise ValueError("start/end 0–99999, 1–5 factors of 1–9999.")
        return _mult(start, end, factors)
    if "|" not in raw:
        raise ValueError("Give the edges, then '| src dst' (and k for flights).")
    edges_txt, q = (text or "").split("|", 1)
    q = q.split()
    sep = ">" if algo == "cheapest_flight_k" else "-"
    edges = []
    for tok in [t for t in edges_txt.replace(" ", "").split(",") if t]:
        try:
            ends, w = tok.split(":")
            a, b = ends.split(sep)
            w = int(w)
        except ValueError:
            raise ValueError(f"'{tok}' should look like A{sep}B:5.") from None
        if not (a.isalnum() and b.isalnum()) or not (0 <= w <= 9999):
            raise ValueError(f"'{tok}': names letters/digits, weight 0–9999.")
        edges.append((a, b, w))
    names = sorted({x for a, b, _ in edges for x in (a, b)})
    if not edges or len(names) > 7:
        raise ValueError("Give 1+ edges over at most 7 nodes.")
    if algo == "cheapest_flight_k":
        if len(q) != 3 or q[0] not in names or q[1] not in names or \
                not q[2].isdigit() or int(q[2]) > 5:
            raise ValueError("After '|', give src dst k (k = max stops, 0–5).")
        return _flights(names, edges, q[0], q[1], int(q[2]))
    if len(q) != 2 or q[0] not in names or q[1] not in names:
        raise ValueError("After '|', give src dst.")
    return _ways(names, edges, q[0], q[1])


def _ladder_input(raw):
    usage = "Give 'begin,end | word,word,…', e.g. hit,cog | hot,dot,dog,cog."
    if "|" not in raw:
        raise ValueError(usage)
    head, rest = raw.lower().split("|", 1)
    ends = [w for w in head.split(",") if w]
    words = [w for w in rest.split(",") if w]
    if len(ends) != 2 or not (1 <= len(words) <= 12):
        raise ValueError(usage)
    L = len(ends[0])
    if L > 5 or any(len(w) != L or not w.isalpha() for w in ends + words):
        raise ValueError("All words must be letters of the same length (≤ 5).")
    return ends[0], ends[1], list(dict.fromkeys(words))


def _ladder(algo, begin, end, words):
    t = RecTree()
    counts = {"words_seen": 1, "levels": 1}
    near = lambda a, b: sum(x != y for x, y in zip(a, b)) == 1
    empty = 0 if algo == "word_ladder" else []
    t.event(None, f"Words are nodes; changing one letter is an edge. BFS from "
                  f"'{begin}' reaches words in order of the number of changes.", counts)
    if end not in words:
        t.event(None, f"'{end}' isn't in the dictionary — no ladder can end there.", counts)
        return {"meta": {"algorithm": algo, "view": "tree", "language": "python",
                         "result": empty}, "steps": t.steps()}
    root = t.node(begin)
    t.event(root, f"Level 1: '{begin}'.", counts)
    parents = {begin: []}
    frontier = [(begin, root)]
    level, found = 1, False
    while frontier and not found:
        level += 1
        counts["levels"] = level
        nxt, this_level = [], set()
        for w, nid in frontier:
            for cand in words:
                if not near(w, cand) or (cand in parents and cand not in this_level):
                    continue
                if cand in this_level:
                    parents[cand].append(w)       # another shortest parent
                    continue
                this_level.add(cand)
                parents[cand] = [w]
                cid = t.node(cand, nid, side=None)
                counts["words_seen"] += 1
                hit = cand == end
                t.event(cid, f"'{w}' → '{cand}' (one letter changed), level {level}."
                             + (" That's the target!" if hit else ""), counts, good=hit)
                nxt.append((cand, cid))
                found = found or hit
        frontier = nxt
    if not found:
        t.event(None, f"The BFS ran out of words — '{end}' is unreachable.", counts)
        res = empty
    elif algo == "word_ladder":
        res = level
        t.event(None, f"Shortest transformation: {level} words.", counts)
    else:
        seqs = []

        def back(w, acc):
            if w == begin:
                seqs.append([begin] + acc[::-1])
                return
            for p in parents[w]:
                back(p, acc + [w])
        back(end, [])
        res = sorted(seqs)
        t.event(None, f"{len(res)} shortest sequence(s): "
                      + "; ".join(" → ".join(s) for s in res) + ".", counts)
    return {"meta": {"algorithm": algo, "view": "tree", "language": "python",
                     "result": res}, "steps": t.steps()}


def _alien(words):
    pairs = list(zip(words, words[1:]))
    G = Grid(len(pairs), 3)
    G.counts = {"rules": 0}
    edges: dict = {}
    letters = sorted({c for w in words for c in w})
    labels = dict(row_labels=[f"pair {i}" for i in range(len(pairs))],
                  col_labels=["word", "next", "rule"])
    G.add("Adjacent words in alien order disagree first at one position — that "
          "pair of letters is one rule of the alphabet.")
    for r, (a, b) in enumerate(pairs):
        G.grid[r][0], G.grid[r][1] = a, b
        diff = next(((x, y) for x, y in zip(a, b) if x != y), None)
        if diff is None:
            if len(a) > len(b):
                G.grid[r][2] = "✗"
                G.add(f"'{a}' comes before its own prefix '{b}' — impossible order.",
                      r, 2, match=False)
                return G.result("alien_dictionary", "", **labels)
            G.grid[r][2] = "—"
            G.add(f"'{a}' is a prefix of '{b}' — no rule.", r, 2)
            continue
        x, y = diff
        edges.setdefault(x, set()).add(y)
        G.counts["rules"] += 1
        G.grid[r][2] = f"{x}<{y}"
        G.add(f"'{a}' vs '{b}': first difference {x} vs {y} → {x} comes before {y}.",
              r, 2, [(r, 0), (r, 1)])
    indeg = {c: 0 for c in letters}
    for x, ys in edges.items():
        for y in ys:
            indeg[y] += 1
    q = sorted(c for c in letters if indeg[c] == 0)
    order = []
    while q:
        c = q.pop(0)
        order.append(c)
        for y in sorted(edges.get(c, ())):
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
                q.sort()
    res = "".join(order) if len(order) == len(letters) else ""
    G.add(f"Topological sort of the rules: {res or 'a cycle — no valid alphabet'}.",
          path=[(r, 2) for r in range(len(pairs)) if G.grid[r][2] != "—"])
    return G.result("alien_dictionary", res, **labels)


def _flights(names, edges, src, dst, k):
    G = Grid(k + 2, len(names))
    G.counts = {"relaxations": 0}
    price = {n: None for n in names}
    price[src] = 0
    col = {n: i for i, n in enumerate(names)}
    show = lambda: [("∞" if price[n] is None else price[n]) for n in names]
    G.grid[0] = show()
    G.add(f"At most {k} stop(s) means at most {k + 1} flights. Each round relaxes "
          f"every flight using only the previous round's prices (no chaining "
          f"within a round).", 0, col[src])
    for rnd in range(1, k + 2):
        new = dict(price)
        for a, b, w in edges:
            G.counts["relaxations"] += 1
            if price[a] is not None and (new[b] is None or price[a] + w < new[b]):
                new[b] = price[a] + w
        price = new
        G.grid[rnd] = show()
        G.add(f"Round {rnd} (≤ {rnd} flight(s)): cheapest known prices.", rnd,
              col[dst], [(rnd - 1, c) for c in range(len(names))])
    res = -1 if price[dst] is None else price[dst]
    G.add(f"Cheapest {src} → {dst} with at most {k} stop(s): {res}.",
          path=[(k + 1, col[dst])], match=res != -1)
    return G.result("cheapest_flight_k", res,
                    [f"≤{r} flights" for r in range(k + 2)], names)


def _ways(names, edges, src, dst):
    adj = {n: [] for n in names}
    for a, b, w in edges:
        adj[a].append((b, w))
        adj[b].append((a, w))
    col = {n: i for i, n in enumerate(names)}
    G = Grid(2, len(names))
    G.counts = {"settled": 0}
    dist = {n: None for n in names}
    ways = {n: 0 for n in names}
    dist[src], ways[src] = 0, 1
    G.grid[0] = ["∞"] * len(names)
    G.grid[1] = [0] * len(names)
    G.grid[0][col[src]], G.grid[1][col[src]] = 0, 1
    pq = [(0, src)]
    done: set = set()
    G.add("Dijkstra, but each node also counts shortest routes: a strictly "
          "shorter route replaces the count, an equally short one adds to it.",
          0, col[src])
    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        G.counts["settled"] += 1
        for v, w in adj[u]:
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v], ways[v] = nd, ways[u]
                heapq.heappush(pq, (nd, v))
                why = f"shorter ({nd}) — ways becomes {ways[v]}"
            elif nd == dist[v] and v not in done:
                ways[v] += ways[u]
                why = f"equally short ({nd}) — ways grows to {ways[v]}"
            else:
                continue
            G.grid[0][col[v]], G.grid[1][col[v]] = dist[v], ways[v]
            G.add(f"From {u}: route to {v} is {why}.", 1, col[v],
                  [(0, col[u]), (1, col[u])])
    res = ways[dst]
    G.add(f"{res} shortest route(s) from {src} to {dst} (length {dist[dst]}).",
          path=[(0, col[dst]), (1, col[dst])])
    return G.result("ways_to_arrive", res, ["dist", "ways"], names)


def _mult(start, end, factors):
    seen = {start}
    level = [start]
    levels = [[start]]
    while level and end not in seen and len(levels) <= 12:
        nxt = []
        for v in level:
            for f in factors:
                nv = v * f % MOD
                if nv not in seen:
                    seen.add(nv)
                    nxt.append(nv)
        levels.append(nxt)
        level = nxt
    shown = [lv[:8] + (["…"] if len(lv) > 8 else []) for lv in levels]
    width = max(len(r) for r in shown)
    G = Grid(len(shown), width)
    G.counts = {"values": len(seen)}
    G.add(f"BFS over values mod {MOD}: each step multiplies by one of "
          f"{factors}. The first level that contains {end} is the answer.")
    for r, row in enumerate(shown):
        G.grid[r] = row + [None] * (width - len(row))
        hit = end in levels[r]
        G.add(f"Level {r}: {len(levels[r])} new value(s)"
              + (f" — {end} is here!" if hit else "."), r, 0,
              path=[(r, row.index(end))] if hit and end in row else [],
              match=hit or r == 0)
    res = next((r for r, lv in enumerate(levels) if end in lv), -1)
    if res == -1:
        G.add(f"{end} was not reached within 12 multiplications.", match=False)
    return G.result("min_multiplications", res,
                    [f"{r} steps" for r in range(len(shown))])


def _stones(stones):
    R = max(r for r, _ in stones) + 1
    C = max(c for _, c in stones) + 1
    G = Grid(R, C, "·")
    parent = list(range(len(stones)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    G.counts = {"groups": len(stones)}
    for r, c in stones:
        G.grid[r][c] = "S"
    G.add("Stones sharing a row or column are connected. Every connected group "
          "can be removed down to one stone, so answer = stones − groups.")
    for i, (r, c) in enumerate(stones):
        for j in range(i):
            if stones[j][0] == r or stones[j][1] == c:
                a, b = find(i), find(j)
                if a != b:
                    parent[a] = b
                    G.counts["groups"] -= 1
                    same = "row" if stones[j][0] == r else "column"
                    G.add(f"({r},{c}) shares a {same} with {stones[j]} — merge "
                          f"their groups.", r, c, [stones[j]])
    labels = {}
    for i, (r, c) in enumerate(stones):
        labels.setdefault(find(i), chr(65 + len(labels)))
        G.grid[r][c] = labels[find(i)]
    groups = len(labels)
    res = len(stones) - groups
    G.add(f"{groups} group(s) (lettered). {len(stones)} − {groups} = {res} stone(s) "
          f"can be removed.", path=stones)
    return G.result("most_stones", res)
