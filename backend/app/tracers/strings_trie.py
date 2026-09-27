"""String (Step 18) and trie (Step 17) leftovers on the `grid` view.

* bracket_reversals — cancel every matched pair; what is left looks like
  '}}}…{{{'. Two of a kind cost one flip, one of each costs two:
  ceil(close/2) + ceil(open/2).
* count_and_say — read the previous term aloud, run by run.
* longest_happy_prefix — the KMP prefix function: lps[i] = longest proper
  prefix of s[0..i] that is also its suffix; the answer is lps[n − 1].
* count_palindromic_subseq — interval DP counting palindromic subsequences
  (by position): equal ends add both sides + 1; otherwise inclusion–
  exclusion removes the double-counted middle.
* distinct_substrings — insert every suffix into a trie; each NEW node is a
  new distinct substring.
* max_xor_pair — a bitwise trie of the numbers; for each number, walk
  greedily towards the opposite bit to maximise the XOR.
* max_xor_queries — offline: sort queries by their limit m, insert array
  values ≤ m into the trie, then answer x's best XOR (−1 if nothing fits).
* trie_advanced (tree view) — every node keeps 'prefix|end' counts, so
  counting words or prefixes and erasing are one walk each.
"""

from app.tracers.grid_common import Grid

TITLES = {
    "bracket_reversals": "Minimum Bracket Reversals to Balance",
    "count_and_say": "Count and Say",
    "longest_happy_prefix": "Longest Happy Prefix (LPS)",
    "count_palindromic_subseq": "Count Palindromic Subsequences",
    "distinct_substrings": "Number of Distinct Substrings (Trie)",
    "max_xor_pair": "Maximum XOR of Two Numbers (Trie)",
    "max_xor_queries": "Maximum XOR With an Element From an Array",
}
MOD = 10 ** 9 + 7
BITS = 8


def _nums(text, n=8, hi=255):
    try:
        a = [int(t) for t in (text or "").replace(" ", "").split(",") if t != ""]
    except ValueError:
        raise ValueError("Numbers only, separated by commas.") from None
    if not (1 <= len(a) <= n) or any(not (0 <= v <= hi) for v in a):
        raise ValueError(f"Give 1–{n} numbers from 0 to {hi}.")
    return a


def run(algo, text, target=None):
    if algo == "trie_advanced":
        return _trie_advanced(_trie_ops(text))
    s = (text or "").replace(" ", "")
    if algo == "bracket_reversals":
        if not (1 <= len(s) <= 16) or any(c not in "{}" for c in s):
            raise ValueError("Use only { and }, up to 16 characters.")
        return _reversals(s)
    if algo == "count_and_say":
        if not s.isdigit() or not (1 <= int(s) <= 8):
            raise ValueError("Give n (1–8).")
        return _count_say(int(s))
    if algo in ("longest_happy_prefix", "count_palindromic_subseq", "distinct_substrings"):
        cap = {"longest_happy_prefix": 16, "count_palindromic_subseq": 10,
               "distinct_substrings": 8}[algo]
        s = s.lower()
        if not (1 <= len(s) <= cap) or not s.isalpha():
            raise ValueError(f"Give 1–{cap} letters.")
        return {"longest_happy_prefix": _lps, "count_palindromic_subseq": _pal_count,
                "distinct_substrings": _distinct}[algo](s)
    if algo == "max_xor_pair":
        a = _nums(s)
        if len(a) < 2:
            raise ValueError("Give at least two numbers.")
        return _xor_pair(a)
    if "|" not in s:
        raise ValueError("Give 'array | x m, x m, …', e.g. 0,1,2,3,4 | 3 1, 1 3, 5 6.")
    arr_t, q_t = text.split("|", 1)
    arr = _nums(arr_t)
    qs = []
    for part in [p.strip() for p in q_t.split(",") if p.strip()]:
        try:
            x, m = (int(v) for v in part.split())
        except ValueError:
            raise ValueError("Each query is 'x m', e.g. 3 1.") from None
        if not (0 <= x <= 255 and 0 <= m <= 255):
            raise ValueError("Query values 0–255.")
        qs.append((x, m))
    if not (1 <= len(qs) <= 5):
        raise ValueError("Give 1–5 queries.")
    return _xor_queries(arr, qs)


def _reversals(s):
    G = Grid(2, len(s))
    G.grid[0] = list(s)
    G.counts = {"open": 0, "close": 0}
    if len(s) % 2:
        G.add(f"{len(s)} brackets — an odd count can never balance. −1.", match=False)
        return G.result("bracket_reversals", -1, ["bracket", "status"])
    G.add("Scan with a stack of unmatched '{'. A '}' that meets one cancels "
          "it; a '}' with nothing open stays unmatched.")
    stack = []
    for i, c in enumerate(s):
        if c == "{":
            stack.append(i)
            G.counts["open"] += 1
            G.grid[1][i] = "open"
            G.add("'{' waits for a partner.", 0, i)
        elif stack:
            j = stack.pop()
            G.counts["open"] -= 1
            G.grid[1][i] = G.grid[1][j] = "ok"
            G.add(f"'}}' matches the '{{' at {j} — both are settled.", 0, i, [(0, j)])
        else:
            G.counts["close"] += 1
            G.grid[1][i] = "close"
            G.add("'}' has no '{' to match — unmatched.", 0, i, match=False)
    o, c = G.counts["open"], G.counts["close"]
    res = (o + 1) // 2 + (c + 1) // 2
    G.add(f"Left over: {c} '}}' then {o} '{{'. A same-kind pair needs one flip, "
          f"a mixed '}}{{' pair needs two: ceil({c}/2) + ceil({o}/2) = {res}.",
          path=[(1, j) for j in range(len(s)) if G.grid[1][j] == "ok"])
    return G.result("bracket_reversals", res, ["bracket", "status"])


def _count_say(n):
    terms = ["1"]
    for _ in range(n - 1):
        t, out, i = terms[-1], "", 0
        while i < len(t):
            j = i
            while j < len(t) and t[j] == t[i]:
                j += 1
            out += f"{j - i}{t[i]}"
            i = j
        terms.append(out)
    w = max(len(t) for t in terms)
    G = Grid(n, w)
    G.counts = {"runs_read": 0}
    G.grid[0][0] = "1"
    G.add("Term 1 is '1'. Each next term reads the previous one aloud: "
          "'count, digit' for every run of equal digits.", 0, 0)
    for r in range(1, n):
        prev, i, pieces = terms[r - 1], 0, []
        while i < len(prev):
            j = i
            while j < len(prev) and prev[j] == prev[i]:
                j += 1
            pieces.append(f"{j - i}×{prev[i]}")
            G.counts["runs_read"] += 1
            i = j
        G.grid[r] = list(terms[r]) + [None] * (w - len(terms[r]))
        G.add(f"Read term {r} ('{prev}'): {', '.join(pieces)} → '{terms[r]}'.", r, None,
              [(r - 1, j) for j in range(len(prev))])
    G.add(f"Term {n}: {terms[-1]}.", path=[(n - 1, j) for j in range(len(terms[-1]))])
    return G.result("count_and_say", terms[-1], [f"n={r + 1}" for r in range(n)])


def _lps(s):
    n = len(s)
    G = Grid(2, n)
    G.grid[0] = list(s)
    G.counts = {"fallbacks": 0}
    lps = [0] * n
    G.grid[1][0] = 0
    G.add("lps[i] = length of the longest proper prefix that is also a suffix "
          "of s[0..i]. On a mismatch, fall back to lps[len − 1] instead of "
          "restarting.", 1, 0)
    ln = 0
    for i in range(1, n):
        while ln and s[i] != s[ln]:
            G.counts["fallbacks"] += 1
            G.add(f"s[{i}] = '{s[i]}' ≠ s[{ln}] = '{s[ln]}' — fall back to "
                  f"lps[{ln - 1}] = {lps[ln - 1]}.", 0, i, [(0, ln)], match=False)
            ln = lps[ln - 1]
        if s[i] == s[ln]:
            ln += 1
        lps[i] = ln
        G.grid[1][i] = ln
        G.add(f"lps[{i}] = {ln}" + (f": '{s[:ln]}' is both a prefix and a suffix."
                                    if ln else "."), 1, i,
              [(0, k) for k in range(ln)], [(0, k) for k in range(i - ln + 1, i + 1)])
    res = s[:lps[-1]]
    G.add(f"Longest happy prefix: '{res}' (length {lps[-1]}).",
          path=[(0, k) for k in range(lps[-1])])
    return G.result("longest_happy_prefix", res, ["char", "lps"])


def _pal_count(s):
    n = len(s)
    G = Grid(n, n)
    G.counts = {"cells": 0}
    dp = [[0] * n for _ in range(n)]
    G.add("dp[i][j] = palindromic subsequences inside s[i..j]. Fill by "
          "increasing length. Equal ends: dp[i+1][j] + dp[i][j−1] + 1 (the "
          "middle ones reappear wrapped by s[i]…s[j]). Different ends: "
          "dp[i+1][j] + dp[i][j−1] − dp[i+1][j−1].")
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if i == j:
                dp[i][j], note, deps = 1, f"'{s[i]}' alone: 1.", []
            elif s[i] == s[j]:
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] + 1) % MOD
                note = (f"s[{i}] = s[{j}] = '{s[i]}': {dp[i + 1][j]} + "
                        f"{dp[i][j - 1]} + 1 = {dp[i][j]}.")
                deps = [(i + 1, j), (i, j - 1)]
            else:
                mid = dp[i + 1][j - 1] if i + 1 <= j - 1 else 0
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] - mid) % MOD
                note = (f"'{s[i]}' ≠ '{s[j]}': {dp[i + 1][j]} + {dp[i][j - 1]} − {mid} "
                        f"= {dp[i][j]}.")
                deps = [(i + 1, j), (i, j - 1)] + ([(i + 1, j - 1)] if i + 1 <= j - 1 else [])
            G.grid[i][j] = dp[i][j]
            G.counts["cells"] += 1
            G.add(note, i, j, deps, match=s[i] == s[j])
    G.add(f"dp[0][{n - 1}] = {dp[0][n - 1]} palindromic subsequences.",
          path=[(0, n - 1)])
    return G.result("count_palindromic_subseq", dp[0][n - 1], list(s), list(s))


def _distinct(s):
    n = len(s)
    G = Grid(n, n)
    G.counts = {"trie_nodes": 0}
    root, total = {}, 0
    G.add("Every substring is a prefix of some suffix. Insert each suffix into "
          "a trie: walking an existing edge = a substring seen before; creating "
          "a node = a brand-new distinct substring.")
    for i in range(n):
        node, new, old = root, [], []
        for k, ch in enumerate(s[i:]):
            G.grid[i][k] = ch
            if ch in node:
                old.append((i, k))
            else:
                node[ch] = {}
                new.append((i, k))
                total += 1
            node = node[ch]
        G.counts["trie_nodes"] = total
        G.add(f"Suffix '{s[i:]}': {len(new)} new node(s) → {len(new)} new distinct "
              f"substring(s). Total {total}.", i, None, old, new, match=bool(new))
    G.add(f"{total} distinct non-empty substrings ({total + 1} counting the empty "
          f"string).")
    return G.result("distinct_substrings", total, [f"suffix {i}" for i in range(n)])


def _bits(v):
    return [int(b) for b in format(v, f"0{BITS}b")]


def _trie_insert(trie, v):
    node = trie
    for b in _bits(v):
        node = node.setdefault(b, {})
    node["v"] = v


def _trie_best(trie, x):
    node, path = trie, []
    for b in _bits(x):
        if 1 - b in node:
            node = node[1 - b]
            path.append(True)
        else:
            node = node[b]
            path.append(False)
    return node["v"], path


def _xor_pair(a):
    n = len(a)
    G = Grid(n, BITS)
    G.grid = [_bits(v) for v in a]
    G.counts = {"trie_steps": 0}
    trie = {}
    for v in a:
        _trie_insert(trie, v)
    G.add(f"Insert every number's {BITS} bits into a trie (most significant "
          f"first). For each number, walk the trie choosing the OPPOSITE bit "
          f"whenever it exists — a 1 in a high XOR bit beats all lower bits.")
    best, pair = -1, None
    for i, v in enumerate(a):
        mate, path = _trie_best(trie, v)
        G.counts["trie_steps"] += BITS
        x = v ^ mate
        if x > best:
            best, pair = x, (v, mate)
        G.add(f"{v}: the best partner is {mate} → {v} ⊕ {mate} = {x} (the opposite "
              f"bit existed at {sum(path)} of {BITS} levels). Best {best}.",
              i, None, [(i, k) for k, ok in enumerate(path) if ok])
    G.add(f"Maximum XOR: {best} ({pair[0]} ⊕ {pair[1]}).")
    return G.result("max_xor_pair", best, [str(v) for v in a],
                    [f"b{BITS - 1 - k}" for k in range(BITS)])


def _xor_queries(arr, qs):
    srt = sorted(arr)
    order = sorted(range(len(qs)), key=lambda q: qs[q][1])
    G = Grid(2, len(srt))
    G.grid[0] = srt[:]
    G.counts = {"inserted": 0}
    trie, k = {}, 0
    ans = [None] * len(qs)
    G.add("Answer queries offline, sorted by their limit m. Array values are "
          "sorted too; before each query insert every value ≤ m into the bit "
          "trie, then find x's best XOR partner among them.")
    for q in order:
        x, m = qs[q]
        while k < len(srt) and srt[k] <= m:
            _trie_insert(trie, srt[k])
            G.grid[1][k] = "in"
            k += 1
            G.counts["inserted"] = k
        if k == 0:
            ans[q] = -1
            G.add(f"Query ({x}, {m}): no value ≤ {m} — answer −1.", match=False)
            continue
        mate, _ = _trie_best(trie, x)
        ans[q] = x ^ mate
        col = srt.index(mate)
        G.add(f"Query ({x}, {m}): values ≤ {m} are in the trie; the best partner "
              f"is {mate} → {x} ⊕ {mate} = {ans[q]}.", 0, col,
              [(0, j) for j in range(k)], [(0, col)])
    G.add(f"Answers in the original query order: {ans}.")
    return G.result("max_xor_queries", ans, ["sorted array", "in trie"])


# ── trie with counts (tree view) ───────────────────────────────────────
TITLES["trie_advanced"] = "Trie With Counts (insert, count, erase)"
TRIE_OPS = {"insert", "countwords", "countprefix", "erase"}


def _trie_ops(text):
    ops = []
    for part in [p.strip() for p in (text or "").split(",") if p.strip()]:
        words = part.lower().split()
        if len(words) != 2 or words[0] not in TRIE_OPS or not words[1].isalpha() \
                or len(words[1]) > 6:
            raise ValueError("Operations like 'insert apple, countprefix ap, "
                             "countwords apple, erase apple' (words ≤ 6 letters).")
        ops.append((words[0], words[1]))
    if not (1 <= len(ops) <= 12):
        raise ValueError("Give 1–12 operations separated by commas.")
    return ops


def _trie_advanced(ops):
    nodes = [{"id": 0, "ch": "•", "kids": {}, "pre": 0, "end": 0}]
    steps, out = [], []
    counts = {"nodes": 1}

    def snap(note, cur=None, marked=()):
        order, leaves = [], []

        def walk(nid, depth):
            nodes[nid]["depth"] = depth
            kids = [nodes[nid]["kids"][c] for c in sorted(nodes[nid]["kids"])]
            if not kids:
                leaves.append(nid)
            for k in kids:
                walk(k, depth + 1)
            order.append(nid)
        walk(0, 0)
        for rank, nid in enumerate(leaves):
            nodes[nid]["x"] = (rank + 0.5) / max(len(leaves), 1)
        for nid in order:                       # post-order: children first
            kids = list(nodes[nid]["kids"].values())
            if kids:
                nodes[nid]["x"] = sum(nodes[k]["x"] for k in kids) / len(kids)
        tree = [{"id": n["id"], "depth": n["depth"], "x": n["x"],
                 "value": n["ch"] if n["id"] == 0 else f"{n['ch']} {n['pre']}|{n['end']}",
                 "left": None, "right": None,
                 "children": [n["kids"][c] for c in sorted(n["kids"])]}
                for n in (nodes[i] for i in sorted(order))]
        steps.append({"i": len(steps), "line": 0, "note": note,
                      "highlight": {"index": cur},
                      "structures": {"tree": tree, "current": cur,
                                     "marked": list(marked), "counts": dict(counts)}})

    def _walk(word):
        cur, path = 0, []
        for ch in word:
            nxt = nodes[cur]["kids"].get(ch)
            if nxt is None:
                return None, path
            cur = nxt
            path.append(cur)
        return cur, path

    snap("Each node stores two counts, shown as 'prefix|end': how many "
         "inserted words pass through it, and how many end exactly here. "
         "count and erase just read or lower those numbers.")
    for name, w in ops:
        if name == "insert":
            cur, path = 0, []
            for ch in w:
                if ch not in nodes[cur]["kids"]:
                    nodes.append({"id": len(nodes), "ch": ch, "kids": {}, "pre": 0, "end": 0})
                    nodes[cur]["kids"][ch] = len(nodes) - 1
                    counts["nodes"] += 1
                cur = nodes[cur]["kids"][ch]
                nodes[cur]["pre"] += 1
                path.append(cur)
            nodes[cur]["end"] += 1
            snap(f"insert '{w}': +1 prefix count along the path, +1 end count "
                 f"at '{w[-1]}'.", cur, path[:-1])
            continue
        node, path = _walk(w)
        if name == "countwords":
            v = nodes[node]["end"] if node is not None else 0
            out.append(v)
            snap(f"countWordsEqualTo('{w}') = {v} (end count of its last node)."
                 if node is not None else f"'{w}' falls off the trie — 0.", node, path)
        elif name == "countprefix":
            v = nodes[node]["pre"] if node is not None else 0
            out.append(v)
            snap(f"countWordsStartingWith('{w}') = {v} (prefix count of its last "
                 f"node)." if node is not None else f"No word starts with '{w}' — 0.",
                 node, path)
        else:
            if node is None or nodes[node]["end"] == 0:
                snap(f"erase '{w}': it isn't stored — nothing to do.", node, path)
                continue
            parent = 0
            for nid in path:
                nodes[nid]["pre"] -= 1
                if nodes[nid]["pre"] == 0:           # nothing passes here any more
                    del nodes[parent]["kids"][nodes[nid]["ch"]]
                    counts["nodes"] -= len(path) - path.index(nid)
                    break
                parent = nid
            nodes[node]["end"] -= 1
            snap(f"erase '{w}': −1 prefix count along the path, −1 end count. Nodes "
                 f"whose prefix count hits 0 disappear.", None, path)
    snap(f"Count results: {out}.")
    return {"meta": {"algorithm": "trie_advanced", "view": "tree", "language": "python",
                     "result": out},
            "steps": steps}

