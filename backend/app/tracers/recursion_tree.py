"""Shared scaffolding for recursion-tree tracers (subsets, parentheses, …).

A backtracking recursion that makes a two-way choice at each call (take/skip,
'('/')', '0'/'1') *is* a binary tree. Tracers record every call as a node and
every visit as an event; once the recursion has finished, the whole tree is
laid out (leaves evenly spaced, parents centred over their children) and the
steps reveal it call by call in DFS order — so nodes never jump around as the
tree grows. The existing `tree` view renders it: `current` is the call being
made, `marked` are the leaves that are answers.
"""


class RecTree:
    def __init__(self):
        self.nodes: list = []
        self.events: list = []

    def node(self, label: str, parent: int | None = None,
             side: str | None = "left"):
        """Add a call. Binary tracers pass side='left'/'right'; tracers whose
        recursion loops over choices pass side=None and get n-ary children."""
        nid = len(self.nodes)
        depth = 0 if parent is None else self.nodes[parent]["depth"] + 1
        self.nodes.append({"id": nid, "value": label, "depth": depth,
                           "x": 0.5, "left": None, "right": None,
                           "children": []})
        if parent is not None:
            if side:
                self.nodes[parent][side] = nid
            self.nodes[parent]["children"].append(nid)
            if side:
                # Keep children in left-then-right order for binary trees.
                kids = self.nodes[parent]["children"]
                kids.sort(key=lambda k: (self.nodes[parent]["right"] == k))
        return nid

    def size(self) -> int:
        return len(self.nodes)

    def event(self, nid: int | None, note: str, counts: dict,
              good: bool = False):
        self.events.append({"nid": nid, "note": note, "counts": dict(counts),
                            "good": good})

    def _layout(self):
        if not self.nodes:
            return
        leaves: list = []

        def order(nid):
            kids = self.nodes[nid]["children"]
            if not kids:
                leaves.append(nid)
            for k in kids:
                order(k)

        order(0)
        for rank, nid in enumerate(leaves):
            self.nodes[nid]["x"] = (rank + 0.5) / len(leaves)

        def centre(nid):
            kids = self.nodes[nid]["children"]
            if kids:
                xs = [centre(k) for k in kids]
                self.nodes[nid]["x"] = sum(xs) / len(xs)
            return self.nodes[nid]["x"]

        centre(0)

    def steps(self) -> list:
        self._layout()
        revealed: set = set()
        good: set = set()
        out: list = []
        for ev in self.events:
            if ev["nid"] is not None:
                revealed.add(ev["nid"])
                if ev["good"]:
                    good.add(ev["nid"])
            tree = [dict(n, children=[k for k in n["children"] if k in revealed])
                    for n in self.nodes if n["id"] in revealed]
            out.append({
                "i": len(out),
                "line": 0,
                "structures": {
                    "tree": tree,
                    "current": ev["nid"],
                    "marked": sorted(good),
                    "counts": ev["counts"],
                },
                "highlight": {"index": ev["nid"]},
                "note": ev["note"],
            })
        return out
