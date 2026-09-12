"""Trie (prefix tree) — building the autocomplete structure word by word.

The lesson is shared prefixes: the second word reuses whatever path already
exists and only branches where it must. Node values are single characters, so
the tree renderer shows letters rather than numbers.
"""

MAX_WORDS = 5
MAX_WORD_LEN = 8


def trace(words: list[str]):
    words = [w for w in words if w]
    steps: list = []
    counts = {"nodes_created": 0, "prefix_reuses": 0, "words_added": 0}

    # nodes[0] is the root; children maps a character to a node index.
    nodes: list[dict] = [{"id": 0, "value": "•", "children": {},
                          "terminal": False, "depth": 0, "x": 0.5}]

    def layout():
        """Spread leaves evenly, then centre each parent over its children."""
        leaves: list[int] = []

        def order(nid, depth):
            nodes[nid]["depth"] = depth
            kids = [nodes[nid]["children"][c]
                    for c in sorted(nodes[nid]["children"])]
            if not kids:
                leaves.append(nid)
                return
            for k in kids:
                order(k, depth + 1)

        order(0, 0)
        n = max(len(leaves), 1)
        for rank, nid in enumerate(leaves):
            nodes[nid]["x"] = (rank + 0.5) / n

        def centre(nid):
            kids = [nodes[nid]["children"][c]
                    for c in sorted(nodes[nid]["children"])]
            if not kids:
                return nodes[nid]["x"]
            xs = [centre(k) for k in kids]
            nodes[nid]["x"] = sum(xs) / len(xs)
            return nodes[nid]["x"]

        centre(0)

    def snapshot():
        """The tree renderer wants left/right, so expose the first two kids."""
        layout()
        out = []
        for n in nodes:
            kids = [n["children"][c] for c in sorted(n["children"])]
            out.append({
                "id": n["id"],
                "value": n["value"] + ("▪" if n["terminal"] else ""),
                "depth": n["depth"],
                "x": n["x"],
                "left": kids[0] if len(kids) > 0 else None,
                "right": kids[1] if len(kids) > 1 else None,
                "children": list(kids),
            })
        return out

    def add(note, current=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "tree": snapshot(),
                "current": current,
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    if not words:
        add("No words to insert — the trie stays empty.")
        return _result(words, steps)

    add(f"Insert {', '.join(words)} into a prefix tree. Every node is one "
        f"character; words that start the same way share the same path.")

    for word in words:
        cur = 0
        add(f"Inserting '{word}' — start at the root.", current=0)
        for ch in word:
            if ch in nodes[cur]["children"]:
                cur = nodes[cur]["children"][ch]
                counts["prefix_reuses"] += 1
                add(f"'{ch}' already exists on this path — reuse it, no new "
                    f"node needed.", current=cur)
            else:
                nodes.append({"id": len(nodes), "value": ch, "children": {},
                              "terminal": False, "depth": 0, "x": 0.5})
                nodes[cur]["children"][ch] = len(nodes) - 1
                cur = len(nodes) - 1
                counts["nodes_created"] += 1
                add(f"No '{ch}' branch here yet — create one.", current=cur)
        nodes[cur]["terminal"] = True
        counts["words_added"] += 1
        add(f"Mark the end of '{word}' (▪) — without that flag the trie could "
            f"not tell a whole word from a prefix of a longer one.",
            current=cur)

    total_chars = sum(len(w) for w in words)
    add(f"All {counts['words_added']} words stored in {counts['nodes_created']} "
        f"nodes instead of {total_chars} characters — {counts['prefix_reuses']} "
        f"steps reused an existing prefix. Lookup costs O(length of the word), "
        f"no matter how many words the trie holds.")
    return _result(words, steps)


def _result(words, steps):
    return {
        "meta": {
            "algorithm": "trie_insert",
            "view": "tree",
            "language": "python",
            "words": words,
        },
        "steps": steps,
    }
