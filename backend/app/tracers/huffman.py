"""Huffman coding — the greedy build of an optimal prefix code.

The whole idea is greedy and local: repeatedly take the two lowest-frequency
nodes and merge them under a new parent whose frequency is their sum. Rare
characters sink deep in the tree (long codes); common ones stay shallow (short
codes). Because every character is a *leaf*, no code is ever a prefix of
another, so the packed bitstream decodes unambiguously.

The tree is built bottom-up but renders in the shared `tree` view: each step
emits the whole forest (many roots early on, one at the end) as
{id, value, depth, x, left, right} nodes — the same shape tree_traversal and
bst_insert use, so the front end needs no new renderer.
"""

import heapq
import math

MAX_LEN = 24


def _fmt(v: float) -> str:
    return f"{v:g}"


def trace(text: str):
    steps: list = []
    counts = {"merges": 0, "picks": 0}

    # Frequency table — stable order (frequency asc, then character) so the
    # trace is deterministic and the rarest characters read left-to-right.
    freq: dict = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    ordered = sorted(freq.items(), key=lambda kv: (kv[1], kv[0]))
    n_leaves = len(ordered)

    nodes: dict = {}
    next_id = 0

    def new_node(value, f, char=None, left=None, right=None, slot=None):
        nonlocal next_id
        nid = next_id
        next_id += 1
        nodes[nid] = {"id": nid, "value": value, "freq": f, "char": char,
                      "left": left, "right": right, "slot": slot}
        return nid

    leaf_ids = [new_node(ch, f, char=ch, slot=slot)
                for slot, (ch, f) in enumerate(ordered)]

    def snapshot():
        """Lay out the current forest: leaves keep a fixed column, internal
        nodes float to the midpoint of their children, depth is measured from
        each current root downward."""
        child = set()
        for nd in nodes.values():
            for c in (nd["left"], nd["right"]):
                if c is not None:
                    child.add(c)
        roots = [i for i in nodes if i not in child]

        depth: dict = {}

        def set_depth(i, d):
            depth[i] = d
            for c in (nodes[i]["left"], nodes[i]["right"]):
                if c is not None:
                    set_depth(c, d + 1)
        for r in roots:
            set_depth(r, 0)

        xcache: dict = {}

        def get_x(i):
            if i in xcache:
                return xcache[i]
            nd = nodes[i]
            kids = [c for c in (nd["left"], nd["right"]) if c is not None]
            if not kids:
                x = (nd["slot"] + 0.5) / max(n_leaves, 1)
            else:
                x = sum(get_x(c) for c in kids) / len(kids)
            xcache[i] = x
            return x

        return [{"id": i, "value": nodes[i]["value"], "freq": nodes[i]["freq"],
                 "depth": depth.get(i, 0), "x": get_x(i),
                 "left": nodes[i]["left"], "right": nodes[i]["right"]}
                for i in sorted(nodes)]

    codes: dict = {}

    def add(note, current=None):
        steps.append({
            "i": len(steps), "line": 0,
            "structures": {
                "tree": snapshot(),
                "current": current,
                "codes": dict(codes),
                "counts": dict(counts),
            },
            "highlight": {"index": current},
            "note": note,
        })

    freq_str = ", ".join(f"{ch}:{_fmt(f)}" for ch, f in ordered)
    add(f"Frequencies counted — {freq_str}. Each character starts as its own "
        f"node. Greedy plan: keep merging the two rarest until one tree remains.")

    # Min-heap keyed by (frequency, id); the id is a stable tie-breaker.
    heap = [(nodes[i]["freq"], i) for i in leaf_ids]
    heapq.heapify(heap)

    while len(heap) > 1:
        f1, a = heapq.heappop(heap)
        f2, b = heapq.heappop(heap)
        counts["picks"] += 2
        add(f"The two rarest nodes: {nodes[a]['value']} ({_fmt(f1)}) and "
            f"{nodes[b]['value']} ({_fmt(f2)}). Greedily merge them.", current=a)
        parent = new_node(_fmt(f1 + f2), f1 + f2, left=a, right=b)
        counts["merges"] += 1
        heapq.heappush(heap, (f1 + f2, parent))
        add(f"A new node of frequency {_fmt(f1 + f2)} sits above them; push it "
            f"back into the pool. {len(heap)} node(s) left to merge.",
            current=parent)

    root = heap[0][1]
    add("One tree remains — the Huffman tree. Now read each character's code "
        "from the root: go left for 0, right for 1.", current=root)

    def assign(i, code):
        nd = nodes[i]
        if nd["left"] is None and nd["right"] is None:
            codes[nd["char"]] = code or "0"
            return
        if nd["left"] is not None:
            assign(nd["left"], code + "0")
        if nd["right"] is not None:
            assign(nd["right"], code + "1")
    assign(root, "")

    code_str = ", ".join(f"{ch}={codes[ch]}" for ch, _ in ordered)
    huff_bits = sum(freq[ch] * len(codes[ch]) for ch in freq)
    fixed_len = max(1, math.ceil(math.log2(n_leaves)))
    fixed_bits = len(text) * fixed_len
    saved = fixed_bits - huff_bits
    pct = (saved / fixed_bits * 100) if fixed_bits else 0.0

    add(f"Codes: {code_str}. The rarest letters ended up deepest, with the "
        f"longest codes — that is exactly what makes the total short.",
        current=root)
    add(f"Packed size: {huff_bits} bits vs {fixed_bits} bits for a flat "
        f"{fixed_len}-bit code — {saved} bits saved ({pct:.0f}%). No code is a "
        f"prefix of another, so the stream still decodes unambiguously.",
        current=root)

    return {
        "meta": {
            "algorithm": "huffman",
            "view": "tree",
            "language": "python",
            "codes": codes,
            "huffman_bits": huff_bits,
            "fixed_bits": fixed_bits,
        },
        "array": list(text),
        "steps": steps,
    }
