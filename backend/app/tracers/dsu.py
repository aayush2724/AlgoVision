"""Disjoint Set Union (union-find) with union by rank and path compression.

Union-find already runs inside Kruskal's, but it is invisible there — students
see edges accepted or rejected without seeing why the check is nearly free.
Standing it up on its own makes the two optimisations legible:

  - union by rank hangs the shorter tree under the taller one, so the trees
    stay shallow instead of degenerating into linked lists;
  - path compression re-points every node touched by a find straight at the
    root, so the next query on that chain is one hop.

The counters report hops saved, which is the whole argument for compression.
"""

from app.tracers.common import Graph, MAX_EDGES, MAX_NODES  # noqa: F401


def trace(graph: Graph, start: str = "A"):
    node_ids = [n.id for n in graph.nodes]
    edges = [(str(e[0]), str(e[1])) for e in graph.edges]
    steps: list = []
    counts = {"finds": 0, "unions": 0, "hops_saved": 0, "rejections": 0}

    parent = {n: n for n in node_ids}
    rank = {n: 0 for n in node_ids}
    merged_edges: list = []

    def root_of(n):
        while parent[n] != n:
            n = parent[n]
        return n

    def components():
        groups: dict = {}
        for n in node_ids:
            groups.setdefault(root_of(n), []).append(n)
        return [sorted(v) for v in groups.values()]

    def add(note, node=None, edge=None, compressed=None):
        steps.append({
            "i": len(steps),
            "line": 0,
            "structures": {
                "visited": sorted({n for e in merged_edges for n in e}),
                "mst_edges": [list(e) for e in merged_edges],
                "components": components(),
                "parent": dict(parent),
                "rank": dict(rank),
                "compressed": list(compressed) if compressed else [],
                "counts": dict(counts),
            },
            "highlight": {"node": node, "edge": list(edge) if edge else None},
            "note": note,
        })

    if not node_ids:
        add("No nodes — nothing to union.")
        return _result(steps, [])

    add(f"{len(node_ids)} nodes, each alone in its own set — {len(node_ids)} "
        f"separate groups. Union-find answers one question fast: are these two "
        f"in the same group? Every node points at a parent; follow the chain "
        f"and you reach the root that names the group.")

    if not edges:
        add(f"No connections given, so all {len(node_ids)} nodes stay separate.")
        return _result(steps, components())

    for a, b in edges:
        add(f"Connect {a} and {b}. First find each one's root.",
            node=a, edge=(a, b))

        ra, path_a = _find_with_path(parent, a)
        rb, path_b = _find_with_path(parent, b)
        counts["finds"] += 2

        if ra == rb:
            counts["rejections"] += 1
            add(f"{a} and {b} both lead to root {ra} — they are already in the "
                f"same group, so this connection adds nothing. (In Kruskal's "
                f"this is exactly the test that rejects a cycle.)",
                node=ra, edge=(a, b))
            continue

        # Union by rank: depth only grows when two equal-height trees meet.
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        grew = rank[ra] == rank[rb]
        if grew:
            rank[ra] += 1
        counts["unions"] += 1
        merged_edges.append((a, b))

        add(f"Different roots ({ra} and {rb}) — merge them. Union by rank hangs "
            f"the shorter tree under the taller one, so {rb} now points at "
            f"{ra}. "
            + (f"Both were the same height, so {ra}'s rank rises to "
               f"{rank[ra]} — the only way depth ever grows."
               if grew else
               f"{ra} was already taller, so no rank changed and the tree "
               f"stayed flat."),
            node=ra, edge=(a, b))

        # Path compression: re-point every node we walked straight at the root.
        touched = []
        for n in path_a + path_b:
            r = root_of(n)
            if n != r and parent[n] != r:
                counts["hops_saved"] += 1
                parent[n] = r
                touched.append(n)
        if touched:
            add(f"Walking those chains told us each node's real root — so point "
                f"{', '.join(touched)} straight at it. Next time any of them is "
                f"queried the answer is one hop. That is path compression, and "
                f"it is why repeated finds get cheaper the more you do them.",
                node=ra, compressed=touched)

    groups = components()
    deepest = max((_depth(parent, n) for n in node_ids), default=0)

    # Be honest about which optimisation actually did the work here: on a small
    # graph union by rank alone usually keeps every tree one level deep, so
    # compression has nothing left to flatten. Claiming otherwise would teach
    # the wrong lesson.
    if counts["hops_saved"]:
        closing = (f"Path compression flattened {counts['hops_saved']} link(s) "
                   f"along the way.")
    else:
        closing = ("Path compression never had to fire: union by rank alone "
                   "kept every tree at most one level deep, so every node "
                   "already pointed straight at its root. Compression earns "
                   "its keep on long chains — which is exactly what rank "
                   "prevents.")

    add(f"{counts['unions']} merge(s) and {counts['rejections']} redundant "
        f"connection(s) later, {len(node_ids)} nodes have collapsed into "
        f"{len(groups)} group{'' if len(groups) == 1 else 's'}: "
        f"{'; '.join('{' + ', '.join(g) + '}' for g in groups)}. "
        f"The deepest chain is {deepest} hop{'' if deepest == 1 else 's'}. "
        f"{closing} With both optimisations each operation is effectively "
        f"constant time (inverse-Ackermann, which never exceeds 4 in practice).")

    return _result(steps, groups)


def _depth(parent, n):
    d = 0
    while parent[n] != n:
        n = parent[n]
        d += 1
    return d


def _find_with_path(parent, n):
    """Return (root, nodes walked). Compression happens after the union."""
    path = []
    while parent[n] != n:
        path.append(n)
        n = parent[n]
    return n, path


def _result(steps, groups):
    return {
        "meta": {
            "algorithm": "dsu",
            "view": "graph",
            "language": "python",
            "groups": [list(g) for g in groups],
            "group_count": len(groups),
        },
        "steps": steps,
    }
