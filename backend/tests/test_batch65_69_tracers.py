"""Batches 65–69 — tree construction/Morris/flatten, stack/queue/cache
implementations, hard linked lists, strings & tries, and the last DP / heap
/ DSU leftovers. Each tracer is checked against a direct reference.
"""

import itertools
import random
from collections import OrderedDict

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import (
    ds_impl as DS, lists_hard as LH, misc_hard as MH, strings_trie as ST,
    tree_build as TB,
)

client = TestClient(app)
R = random.Random(65)
res = lambda out: out["meta"]["result"]
csv = lambda a: ",".join(map(str, a))


def rand_tree(n):
    """A random binary tree over distinct values: (level-order text, kids, root)."""
    vals = R.sample(range(1, 60), n)
    kids = {vals[0]: [None, None]}
    for v in vals[1:]:
        while True:
            p = R.choice(list(kids))
            side = R.randint(0, 1)
            if kids[p][side] is None:
                kids[p][side] = v
                kids[v] = [None, None]
                break
    out, q = [], [vals[0]]
    while q:
        x = q.pop(0)
        out.append(x)
        if x is not None:
            q += kids[x]
    while out[-1] is None:
        out.pop()
    return ",".join("null" if v is None else str(v) for v in out), kids, vals[0]


def orders(kids, root):
    pre, ino, post = [], [], []

    def walk(x):
        if x is None:
            return
        pre.append(x)
        walk(kids[x][0])
        ino.append(x)
        walk(kids[x][1])
        post.append(x)
    walk(root)
    return pre, ino, post


def script(ops):
    return ", ".join(" ".join(map(str, o)) for o in ops)


def balanced(t):
    bal = 0
    for c in t:
        bal += 1 if c == "{" else -1
        if bal < 0:
            return False
    return bal == 0


class TestTreeBuild:
    def test_construct_morris_flatten(self):
        for _ in range(30):
            text, kids, root = rand_tree(R.randint(1, 12))
            pre, ino, post = orders(kids, root)
            lvl = [None if t == "null" else int(t) for t in text.split(",")]
            assert res(TB.run("build_pre_in", f"{csv(pre)} | {csv(ino)}")) == lvl
            assert res(TB.run("build_post_in", f"{csv(post)} | {csv(ino)}")) == lvl
            assert res(TB.run("morris_inorder", text)) == ino
            out = TB.run("morris_preorder", text)
            assert res(out) == pre
            assert out["steps"][-1]["structures"]["threads"] == []
            out = TB.run("flatten_tree", text)
            assert res(out) == pre
            assert all(n["left"] is None for n in out["steps"][-1]["structures"]["tree"])

    def test_serialize(self):
        for _ in range(20):
            text, kids, root = rand_tree(R.randint(1, 10))
            toks, q = [], [root]
            while q:
                x = q.pop(0)
                if x is None:
                    toks.append("#")
                    continue
                toks.append(str(x))
                q += kids[x]
            assert res(TB.run("serialize_tree", text)) == ",".join(toks)

    def test_identical_and_merge(self):
        for _ in range(30):
            text, _, _ = rand_tree(R.randint(1, 7))
            assert res(TB.run("identical_trees", f"{text} | {text}")) is True
            other, _, _ = rand_tree(R.randint(1, 7))
            assert res(TB.run("identical_trees", f"{text} | {other}")) == (text == other)
            a, b = R.sample(range(50), R.randint(1, 7)), R.sample(range(50), R.randint(1, 7))
            assert res(TB.run("merge_two_bsts", f"{csv(a)} | {csv(b)}")) == sorted(a + b)

    def test_bad_traversals(self):
        for text in ("1,2,3 | 3,1,2", "1,2 | 1,3", "1,1 | 1,1"):
            try:
                TB.run("build_pre_in", text)
            except ValueError:
                continue
            raise AssertionError(text)


class TestImplementations:
    def test_stacks_and_queues(self):
        for _ in range(40):
            ops = [R.choice([("push", R.randint(0, 9)), ("pop",), ("top",)])
                   for _ in range(R.randint(1, 14))]
            cap = R.randint(1, 6)

            def simulate(seq, fifo, limit=None):
                ref, out = [], []
                for o in seq:
                    if o[0] == "push":
                        if limit is None or len(ref) < limit:
                            ref.append(o[1])
                    elif not ref:
                        out.append(None)
                    elif o[0] == "pop":
                        out.append(ref.pop(0) if fifo else ref.pop())
                    else:
                        out.append(ref[0] if fifo else ref[-1])
                return out

            assert res(DS.run("stack_array", script(ops), cap)) == simulate(ops, False, cap)
            for algo in ("stack_using_queue", "stack_linkedlist"):
                assert res(DS.run(algo, script(ops))) == simulate(ops, False)
            qops = [("front",) if o[0] == "top" else o for o in ops]
            for algo in ("queue_using_stacks", "queue_linkedlist"):
                assert res(DS.run(algo, script(qops))) == simulate(qops, True)
            assert res(DS.run("queue_array", script(qops), cap)) == simulate(qops, True, cap)

    def test_min_stack(self):
        for _ in range(30):
            ops = [R.choice([("push", R.randint(-9, 9)), ("pop",), ("top",), ("getmin",)])
                   for _ in range(R.randint(1, 14))]
            ref, out = [], []
            for o in ops:
                if o[0] == "push":
                    ref.append(o[1])
                elif not ref:
                    out.append(None)
                elif o[0] == "getmin":
                    out.append(min(ref))
                else:
                    out.append(ref.pop() if o[0] == "pop" else ref[-1])
            assert res(DS.run("min_stack", script(ops))) == out

    def test_caches(self):
        for _ in range(40):
            cap = R.randint(1, 3)
            ops = [R.choice([("put", R.randint(1, 4), R.randint(0, 9)), ("get", R.randint(1, 4))])
                   for _ in range(R.randint(1, 14))]
            lru, out = OrderedDict(), []
            for o in ops:
                if o[0] == "get":
                    if o[1] in lru:
                        lru.move_to_end(o[1])
                        out.append(lru[o[1]])
                    else:
                        out.append(-1)
                else:
                    if o[1] in lru:
                        lru.move_to_end(o[1])
                    elif len(lru) == cap:
                        lru.popitem(last=False)
                    lru[o[1]] = o[2]
            assert res(DS.run("lru_cache", script(ops), cap)) == out
            store, freq, last, out = {}, {}, {}, []
            for t, o in enumerate(ops):
                k = o[1]
                if o[0] == "get":
                    if k in store:
                        freq[k] += 1
                        last[k] = t
                        out.append(store[k])
                    else:
                        out.append(-1)
                    continue
                if k in store:
                    freq[k] += 1
                else:
                    if len(store) == cap:
                        old = min(store, key=lambda x: (freq[x], last[x]))
                        for d in (store, freq, last):
                            del d[old]
                    freq[k] = 1
                store[k] = o[2]
                last[k] = t
            assert res(DS.run("lfu_cache", script(ops), cap)) == out

    def test_twitter(self):
        for _ in range(20):
            ops, tid = [], 0
            for _ in range(R.randint(1, 14)):
                kind = R.choice(["post", "post", "follow", "unfollow", "feed"])
                if kind == "post":
                    tid += 1
                    ops.append(("post", R.randint(1, 3), tid))
                elif kind == "feed":
                    ops.append(("feed", R.randint(1, 3)))
                else:
                    ops.append((kind, R.randint(1, 3), R.randint(1, 3)))
            tweets, follows, feeds = [], {}, []
            for o in ops:
                if o[0] == "post":
                    tweets.append((o[1], o[2]))
                elif o[0] == "follow" and o[1] != o[2]:
                    follows.setdefault(o[1], set()).add(o[2])
                elif o[0] == "unfollow":
                    follows.get(o[1], set()).discard(o[2])
                elif o[0] == "feed":
                    who = {o[1]} | follows.get(o[1], set())
                    feeds.append([t for u, t in reversed(tweets) if u in who][:10])
            assert res(DS.run("design_twitter", script(ops))) == feeds


class TestHardLists:
    def test_clone(self):
        for _ in range(30):
            n = R.randint(1, 6)
            vals = [R.randint(0, 9) for _ in range(n)]
            rnd = [R.randint(-1, n - 1) for _ in range(n)]
            out = LH.run("clone_random_list", f"{csv(vals)} | {csv(rnd)}")
            assert res(out) == {"values": vals, "random": rnd}
            final = out["steps"][-1]["structures"]
            assert final["next"][0] == (2 if n > 1 else None)   # originals unwoven

    def test_flatten_and_merge_k(self):
        for _ in range(40):
            k = R.randint(2, 4)
            groups = [sorted(R.randint(0, 20) for _ in range(R.randint(1, 3))) for _ in range(k)]
            text = " | ".join(csv(g) for g in groups)
            flat = sorted(v for g in groups for v in g)
            assert res(LH.run("flatten_list", text)) == flat
            assert res(LH.run("merge_k_lists", text)) == flat


class TestStringsTries:
    def test_reversals(self):
        for _ in range(60):
            s = "".join(R.choice("{}") for _ in range(R.randint(1, 12)))
            want = -1 if len(s) % 2 else min(
                sum(a != b for a, b in zip(s, t))
                for t in ("".join(p) for p in itertools.product("{}", repeat=len(s)))
                if balanced(t))
            assert res(ST.run("bracket_reversals", s)) == want, s

    def test_count_and_say(self):
        seq = ["1", "11", "21", "1211", "111221", "312211", "13112221", "1113213211"]
        for n in range(1, 9):
            assert res(ST.run("count_and_say", str(n))) == seq[n - 1]

    def test_happy_prefix_and_pal_count(self):
        for _ in range(40):
            s = "".join(R.choice("ab") for _ in range(R.randint(1, 10)))
            want = next((s[:k] for k in range(len(s) - 1, 0, -1) if s[:k] == s[-k:]), "")
            assert res(ST.run("longest_happy_prefix", s)) == want
            brute = 0
            for m in range(1, 1 << len(s)):
                t = "".join(s[i] for i in range(len(s)) if m >> i & 1)
                brute += t == t[::-1]
            assert res(ST.run("count_palindromic_subseq", s)) == brute

    def test_distinct_substrings(self):
        for _ in range(30):
            s = "".join(R.choice("abc") for _ in range(R.randint(1, 8)))
            want = len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})
            assert res(ST.run("distinct_substrings", s)) == want

    def test_xor(self):
        for _ in range(40):
            a = [R.randint(0, 255) for _ in range(R.randint(2, 8))]
            assert res(ST.run("max_xor_pair", csv(a))) == max(x ^ y for x in a for y in a)
            qs = [(R.randint(0, 255), R.randint(0, 255)) for _ in range(R.randint(1, 5))]
            want = [max((x ^ v for v in a if v <= m), default=-1) for x, m in qs]
            text = f"{csv(a)} | " + ", ".join(f"{x} {m}" for x, m in qs)
            assert res(ST.run("max_xor_queries", text)) == want

    def test_trie_advanced(self):
        words = ["ab", "abc", "b", "bca", "a"]
        for _ in range(30):
            ops, bag, out = [], [], []
            for _ in range(R.randint(1, 12)):
                kind = R.choice(["insert", "insert", "countwords", "countprefix", "erase"])
                w = R.choice(words)
                if kind == "countprefix":
                    w = w[:R.randint(1, len(w))]
                ops.append((kind, w))
                if kind == "insert":
                    bag.append(w)
                elif kind == "countwords":
                    out.append(bag.count(w))
                elif kind == "countprefix":
                    out.append(sum(x.startswith(w) for x in bag))
                elif w in bag:
                    bag.remove(w)
            got = ST.run("trie_advanced", ", ".join(f"{k} {w}" for k, w in ops))
            assert res(got) == out
            prefixes = {x[:i] for x in bag for i in range(1, len(x) + 1)}
            assert len(got["steps"][-1]["structures"]["tree"]) == 1 + len(prefixes)


class TestLastLeftovers:
    def test_ninja(self):
        for _ in range(30):
            r, c = R.randint(1, 4), R.randint(2, 4)
            g = [[R.randint(0, 9) for _ in range(c)] for _ in range(r)]
            best = -1
            for ma in itertools.product((-1, 0, 1), repeat=r - 1):
                for mb in itertools.product((-1, 0, 1), repeat=r - 1):
                    a, b, tot, ok = 0, c - 1, 0, True
                    for row in range(r):
                        if row:
                            a, b = a + ma[row - 1], b + mb[row - 1]
                            if not (0 <= a < c and 0 <= b < c):
                                ok = False
                                break
                        tot += g[row][a] + (g[row][b] if a != b else 0)
                    if ok:
                        best = max(best, tot)
            assert res(MH.run("ninja_friends", "/".join(csv(row) for row in g))) == best

    def test_max_sum_combination(self):
        for _ in range(30):
            n = R.randint(1, 6)
            a, b = [R.randint(-9, 9) for _ in range(n)], [R.randint(-9, 9) for _ in range(n)]
            k = R.randint(1, n * n)
            want = sorted((x + y for x in a for y in b), reverse=True)[:k]
            assert res(MH.run("max_sum_combination", f"{csv(a)} | {csv(b)}", k)) == want

    def test_accounts(self):
        pool = ["e1", "e2", "e3", "e4", "e5", "e6"]
        for _ in range(30):
            accts = [("Ann", R.sample(pool, R.randint(1, 3))) for _ in range(R.randint(1, 5))]
            groups = [set(e) for _, e in accts]
            merged = True
            while merged:                     # union overlapping sets until stable
                merged = False
                for i, j in itertools.combinations(range(len(groups)), 2):
                    if groups[i] & groups[j]:
                        groups[i] |= groups.pop(j)
                        merged = True
                        break
            want = sorted(["Ann"] + sorted(g) for g in groups)
            text = "; ".join(f"Ann {' '.join(e)}" for _, e in accts)
            assert res(MH.run("accounts_merge", text)) == want


class TestWiring:
    def test_every_id_through_api(self):
        samples = {
            "build_pre_in": "3,9,20,15,7 | 9,3,15,20,7",
            "build_post_in": "9,15,7,20,3 | 9,3,15,20,7",
            "serialize_tree": "1,2,3", "morris_inorder": "1,2,3", "morris_preorder": "1,2,3",
            "flatten_tree": "1,2,5", "identical_trees": "1,2 | 1,2", "merge_two_bsts": "2,1 | 3",
            "stack_using_queue": "push 1, top", "queue_using_stacks": "push 1, front",
            "stack_linkedlist": "push 1, pop", "queue_linkedlist": "push 1, pop",
            "min_stack": "push 2, getmin", "design_twitter": "post 1 1, feed 1",
            "clone_random_list": "1,2 | 1,-1", "flatten_list": "1,5 | 2", "merge_k_lists": "1 | 2",
            "bracket_reversals": "}{", "count_and_say": "4", "longest_happy_prefix": "abab",
            "count_palindromic_subseq": "aba", "distinct_substrings": "aba",
            "max_xor_pair": "3,10", "max_xor_queries": "1,2 | 3 1",
            "trie_advanced": "insert ab, countprefix a",
            "ninja_friends": "1,2/3,4", "accounts_merge": "Ann a b; Ann b c"}
        with_target = {"stack_array": ("push 1, pop", 2), "queue_array": ("push 1, pop", 2),
                       "lru_cache": ("put 1 1, get 1", 1), "lfu_cache": ("put 1 1, get 1", 1),
                       "max_sum_combination": ("1,2 | 3,4", 2)}
        every = set(TB.TITLES) | set(DS.TITLES) | set(LH.TITLES) | set(ST.TITLES) | set(MH.TITLES)
        assert set(samples) | set(with_target) == every
        tree = set(TB.TITLES) | {"trie_advanced"}
        lists = set(LH.TITLES) | {"stack_linkedlist", "queue_linkedlist"}
        for algo, text in samples.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text})
            assert r.status_code == 200, (algo, r.text)
            want = "tree" if algo in tree else "list" if algo in lists else "grid"
            assert r.json()["meta"]["view"] == want, algo
        for algo, (text, t) in with_target.items():
            r = client.post("/api/trace", json={"algorithm": algo, "text": text, "target": t})
            assert r.status_code == 200, (algo, r.text)
        for algo in every:
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo, algo

    def test_bad_inputs(self):
        for p in ({"algorithm": "build_pre_in", "text": "1,2"},
                  {"algorithm": "identical_trees", "text": "1,2"},
                  {"algorithm": "stack_array", "text": "push 1", "target": 0},
                  {"algorithm": "min_stack", "text": "fly 3"},
                  {"algorithm": "lru_cache", "text": "put 1", "target": 2},
                  {"algorithm": "clone_random_list", "text": "1,2 | 5,0"},
                  {"algorithm": "merge_k_lists", "text": "3,1 | 2"},
                  {"algorithm": "bracket_reversals", "text": "(}"},
                  {"algorithm": "count_and_say", "text": "9"},
                  {"algorithm": "max_xor_pair", "text": "300,1"},
                  {"algorithm": "trie_advanced", "text": "delete abc"},
                  {"algorithm": "ninja_friends", "text": "1/2"},
                  {"algorithm": "max_sum_combination", "text": "1,2 | 3", "target": 1},
                  {"algorithm": "accounts_merge", "text": "a"}):
            assert client.post("/api/trace", json=p).status_code == 400, p
