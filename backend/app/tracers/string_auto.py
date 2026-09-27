"""String automata and hashing (batch 80).

* aho_corasick (tree view) — put every pattern in a trie, then give each node
  a FAILURE link (dashed): the longest proper suffix of its string that is
  also a trie path. Scanning the text never backs up: on a mismatch follow
  failure links; at each node, report every pattern that ends there or at
  a node reachable through failure links.
* substring_hash (grid view) — prefix hashes h[i] of s[0..i) with base B mod
  M let any substring's hash come out in O(1):
  hash(l, r) = h[r] − h[l]·B^(r−l). Equal hashes ⇒ (almost surely) equal
  substrings.
"""

from collections import deque

from app.tracers.grid_common import Grid

TITLES = {
    "aho_corasick": "Aho–Corasick (Multi-Pattern Search)",
    "substring_hash": "Substring Equality by Rolling Hash",
}
BASE, MOD = 31, 1_000_000_007


def run(algo, text, target=None):
    if "|" not in (text or ""):
        raise ValueError("Give 'text | …' — see the hint.")
    left, right = (p.strip() for p in text.split("|", 1))
    s = left.lower()
    if not (1 <= len(s) <= 14) or not s.isalpha():
        raise ValueError("The text is 1–14 letters.")
    if algo == "aho_corasick":
        pats = [p.strip().lower() for p in right.split(",") if p.strip()]
        if not (1 <= len(pats) <= 4) or not all(p.isalpha() and len(p) <= 5 for p in pats):
            raise ValueError("Give 1–4 patterns of up to 5 letters, comma-separated.")
        return _aho(s, list(dict.fromkeys(pats)))
    qs = []
    for part in [p for p in right.split(",") if p.strip()]:
        try:
            a, b, ln = (int(x) for x in part.split())
        except ValueError:
            raise ValueError("Each query is 'i j len': compare s[i:i+len] with "
                             "s[j:j+len].") from None
        if ln < 1 or not (0 <= a and a + ln <= len(s) and 0 <= b and b + ln <= len(s)):
            raise ValueError("Each query must stay inside the text.")
        qs.append((a, b, ln))
    if not (1 <= len(qs) <= 5):
        raise ValueError("Give 1–5 queries.")
    return _hash(s, qs)


def _aho(s, pats):
    nodes = [{"id": 0, "ch": "•", "kids": {}, "fail": 0, "out": [], "word": ""}]
    for p in pats:
        cur = 0
        for ch in p:
            if ch not in nodes[cur]["kids"]:
                nodes.append({"id": len(nodes), "ch": ch, "kids": {}, "fail": 0,
                              "out": [], "word": nodes[cur]["word"] + ch})
                nodes[cur]["kids"][ch] = len(nodes) - 1
            cur = nodes[cur]["kids"][ch]
        nodes[cur]["out"].append(p)
    leaves, order = [], []                 # layout: leaves spread, parents centred

    def walk(nid, depth):
        nodes[nid]["depth"] = depth
        kids = [nodes[nid]["kids"][c] for c in sorted(nodes[nid]["kids"])]
        if not kids:
            leaves.append(nid)
        for k in kids:
            walk(k, depth + 1)
        order.append(nid)
    walk(0, 0)
    for r, nid in enumerate(leaves):
        nodes[nid]["x"] = (r + 0.5) / len(leaves)
    for nid in order:
        kids = list(nodes[nid]["kids"].values())
        if kids:
            nodes[nid]["x"] = sum(nodes[k]["x"] for k in kids) / len(kids)

    steps, counts, fails = [], {"fail_hops": 0, "matches": 0}, []

    def add(note, cur=None):
        tree = [{"id": n["id"], "value": n["ch"] + ("*" if n["out"] else ""),
                 "depth": n["depth"], "x": n["x"], "left": None, "right": None,
                 "children": [n["kids"][c] for c in sorted(n["kids"])]} for n in nodes]
        steps.append({"i": len(steps), "line": 0, "note": note,
                      "highlight": {"index": cur},
                      "structures": {"tree": tree, "current": cur, "marked": [],
                                     "counts": dict(counts),
                                     "threads": [list(f) for f in fails]}})

    add(f"Trie of the patterns {pats} (* = a pattern ends here). Next, failure "
        f"links (dashed): from each node to the longest proper suffix of its "
        f"string that is also in the trie. Built in BFS order.")
    q = deque(nodes[0]["kids"].values())
    while q:
        u = q.popleft()
        if nodes[u]["fail"]:
            fails.append((u, nodes[u]["fail"]))
        add(f"'{nodes[u]['word']}' fails to "
            f"'{nodes[nodes[u]['fail']]['word'] or 'root'}'"
            + (f"; it reports {nodes[u]['out']}" if nodes[u]["out"] else "") + ".", u)
        for ch, v in sorted(nodes[u]["kids"].items()):
            f = nodes[u]["fail"]
            while f and ch not in nodes[f]["kids"]:
                f = nodes[f]["fail"]
            nxt = nodes[f]["kids"].get(ch)
            nodes[v]["fail"] = nxt if nxt is not None and nxt != v else 0
            nodes[v]["out"] = nodes[v]["out"] + nodes[nodes[v]["fail"]]["out"]
            q.append(v)
    cur, found = 0, []
    add(f"Now scan '{s}' once. Follow the trie while you can; on a mismatch hop "
        f"along failure links instead of restarting.", 0)
    for i, ch in enumerate(s):
        while cur and ch not in nodes[cur]["kids"]:
            cur = nodes[cur]["fail"]
            counts["fail_hops"] += 1
        cur = nodes[cur]["kids"].get(ch, 0)
        hits = nodes[cur]["out"]
        for p in hits:
            found.append([p, i - len(p) + 1])
            counts["matches"] += 1
        add(f"Read '{ch}' (index {i}) → state '{nodes[cur]['word'] or 'root'}'"
            + (f": match {hits} ending at {i}." if hits else "."), cur)
    add(f"Matches (pattern, start): {found or 'none'}.")
    return {"meta": {"algorithm": "aho_corasick", "view": "tree", "language": "python",
                     "result": found},
            "steps": steps}


def _hash(s, qs):
    n = len(s)
    h, pw = [0] * (n + 1), [1] * (n + 1)
    G = Grid(3, n + 1)
    G.grid[0] = list(s) + [""]
    G.counts = {"hash_ops": 0}
    G.grid[1][0], G.grid[2][0] = 0, 1
    G.add(f"h[i] = hash of s[0..i) = h[i−1]·{BASE} + code(s[i−1]) mod 1e9+7, and "
          f"pw[i] = {BASE}^i. Two arrays, built once in O(n).", 1, 0)
    for i in range(1, n + 1):
        h[i] = (h[i - 1] * BASE + ord(s[i - 1]) - 96) % MOD
        pw[i] = pw[i - 1] * BASE % MOD
        G.grid[1][i], G.grid[2][i] = h[i], pw[i]
        G.counts["hash_ops"] += 1
        G.add(f"h[{i}] = h[{i - 1}]·{BASE} + {ord(s[i - 1]) - 96} ('{s[i - 1]}') = {h[i]}.",
              1, i, [(1, i - 1)])
    sub = lambda l, ln: (h[l + ln] - h[l] * pw[ln]) % MOD
    out = []
    for a, b, ln in qs:
        x, y = sub(a, ln), sub(b, ln)
        out.append(x == y)
        G.counts["hash_ops"] += 2
        G.add(f"'{s[a:a + ln]}' vs '{s[b:b + ln]}': hash = h[r] − h[l]·pw[len] → "
              f"{x} vs {y} → {'equal' if x == y else 'different'} — O(1) each.",
              None, None, [(0, k) for k in range(a, a + ln)],
              [(0, k) for k in range(b, b + ln)], match=x == y)
    G.add(f"Answers: {out}.")
    return G.result("substring_hash", out, ["char", "h[i]", "pw[i]"],
                    [str(i) for i in range(n + 1)])
