"""Longest Word With All Prefixes (the "complete string") — a trie check.

A word is complete when every one of its prefixes is also in the list:
"ninja" needs "n", "ni", "nin", "ninj". Put every word in a trie; then a word
is complete exactly when each node along its path carries the end-of-word
mark. Checking a word costs O(its length), with no set of prefixes to build.
Ties on length go to the alphabetically smaller word.

Reuses the `tree` view exactly as trie_insert does (letters as nodes, ▪ marks
a word's end, `current` is the node under the cursor). No new renderer.
"""

MAX_WORDS = 7
MAX_WORD_LEN = 8


def trace(words: list):
    words = [w for w in words if w]
    steps: list = []
    counts = {"nodes": 0, "checks": 0}
    nodes: list = [{"id": 0, "value": "•", "children": {}, "terminal": False,
                    "depth": 0, "x": 0.5}]

    def layout():
        leaves: list = []

        def order(nid, depth):
            nodes[nid]["depth"] = depth
            kids = [nodes[nid]["children"][c] for c in sorted(nodes[nid]["children"])]
            if not kids:
                leaves.append(nid)
            for kid in kids:
                order(kid, depth + 1)

        order(0, 0)
        for rank, nid in enumerate(leaves):
            nodes[nid]["x"] = (rank + 0.5) / max(len(leaves), 1)

        def centre(nid):
            kids = [nodes[nid]["children"][c] for c in sorted(nodes[nid]["children"])]
            if kids:
                xs = [centre(kid) for kid in kids]
                nodes[nid]["x"] = sum(xs) / len(xs)
            return nodes[nid]["x"]

        centre(0)

    def snapshot():
        layout()
        out = []
        for nd in nodes:
            kids = [nd["children"][c] for c in sorted(nd["children"])]
            out.append({
                "id": nd["id"],
                "value": nd["value"] + ("▪" if nd["terminal"] else ""),
                "depth": nd["depth"],
                "x": nd["x"],
                "left": kids[0] if kids else None,
                "right": kids[1] if len(kids) > 1 else None,
                "children": kids,
            })
        return out

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {"tree": snapshot(), "current": current,
                           "counts": dict(counts)},
            "highlight": {"index": current},
            "note": note,
        })

    if not words:
        add("No words — there is no complete string.")
        return _result(words, steps, None)

    add(f"Words: {', '.join(words)}. A word is 'complete' if every prefix of "
        f"it is also a word. First build a trie; ▪ marks where a word ends.")

    for w in words:
        cur = 0
        for ch in w:
            if ch not in nodes[cur]["children"]:
                nodes.append({"id": len(nodes), "value": ch, "children": {},
                              "terminal": False, "depth": 0, "x": 0.5})
                nodes[cur]["children"][ch] = len(nodes) - 1
                counts["nodes"] += 1
            cur = nodes[cur]["children"][ch]
        nodes[cur]["terminal"] = True
        add(f"Inserted '{w}' — its last letter gets the ▪ end mark.",
            current=cur)

    best = None
    for w in sorted(set(words), key=lambda s: (-len(s), s)):
        # Longest-first, alphabetical within a length: the first complete word
        # found is the answer, so stop there.
        cur = 0
        ok = True
        for i, ch in enumerate(w):
            cur = nodes[cur]["children"][ch]
            counts["checks"] += 1
            if not nodes[cur]["terminal"]:
                add(f"Checking '{w}': prefix '{w[:i + 1]}' has no ▪ — it isn't "
                    f"a word, so '{w}' is not complete.", current=cur)
                ok = False
                break
        if ok:
            best = w
            add(f"Every letter of '{w}' carries ▪ — all its prefixes are "
                f"words. Checking longest-first, so '{w}' is the answer.",
                current=cur)
            break

    if best is None:
        add(f"No word is complete — every one has a missing prefix. Answer: "
            f"None. ({counts['checks']} node checks.)")
    else:
        add(f"Longest complete string: '{best}'. {counts['checks']} node "
            f"checks in total — each word costs only its own length.")
    return _result(words, steps, best)


def _result(words, steps, best):
    return {
        "meta": {
            "algorithm": "longest_complete_word",
            "view": "tree",
            "language": "python",
            "words": words,
            "result": best,
        },
        "steps": steps,
    }
