"""Batch 23 — Binary Trees (Step 13): level-order traversal, maximum depth,
diameter, and lowest common ancestor. Each is checked against an independent
reference implementation over the same BST the tracer builds.
"""

from collections import deque

from fastapi.testclient import TestClient

from app.main import app
from app.tracers import level_order, tree_max_depth, tree_diameter, lca_bt

client = TestClient(app)


# ── Reference tree (mirrors tracer's BST insertion order) ──
def _build_ref(values):
    """Same rule as tree_traversal._build: < goes left, >= goes right."""
    nodes = []

    def insert(root, v):
        if root is None:
            nodes.append({"v": v, "l": None, "r": None})
            return len(nodes) - 1
        if v < nodes[root]["v"]:
            nodes[root]["l"] = insert(nodes[root]["l"], v)
        else:
            nodes[root]["r"] = insert(nodes[root]["r"], v)
        return root

    root = None
    for v in values:
        root = insert(root, v)
    return nodes, root


def _ref_level_order(values):
    nodes, root = _build_ref(values)
    out, q = [], deque([root] if root is not None else [])
    while q:
        nid = q.popleft()
        out.append(nodes[nid]["v"])
        for c in (nodes[nid]["l"], nodes[nid]["r"]):
            if c is not None:
                q.append(c)
    return out


def _ref_height(values):
    nodes, root = _build_ref(values)

    def h(nid):
        return 0 if nid is None else 1 + max(h(nodes[nid]["l"]), h(nodes[nid]["r"]))

    return h(root)


def _ref_diameter(values):
    nodes, root = _build_ref(values)
    best = [0]

    def h(nid):
        if nid is None:
            return 0
        lh, rh = h(nodes[nid]["l"]), h(nodes[nid]["r"])
        best[0] = max(best[0], lh + rh)
        return 1 + max(lh, rh)

    h(root)
    return best[0]


def _ref_lca(values, a, b):
    nodes, root = _build_ref(values)

    def lca(nid):
        if nid is None:
            return None
        if nodes[nid]["v"] in (a, b):
            return nid
        left, right = lca(nodes[nid]["l"]), lca(nodes[nid]["r"])
        if left is not None and right is not None:
            return nid
        return left if left is not None else right

    r = lca(root)
    return None if r is None else nodes[r]["v"]


CASES = [
    [8, 3, 10, 1, 6, 14, 4],
    [5, 3, 8, 1, 9, 2, 7],
    [1, 2, 3, 4, 5],          # right-leaning chain
    [5, 4, 3, 2, 1],          # left-leaning chain
    [42],
]


class TestTreeTracers:
    def test_level_order(self):
        for vals in CASES:
            flat = [v for lvl in level_order.trace(vals)["meta"]["levels"] for v in lvl]
            ref = [f"{v:g}" for v in _ref_level_order(vals)]
            assert flat == ref, vals

    def test_max_depth(self):
        for vals in CASES:
            assert tree_max_depth.trace(vals)["meta"]["max_depth"] == _ref_height(vals), vals

    def test_diameter(self):
        for vals in CASES:
            assert tree_diameter.trace(vals)["meta"]["diameter"] == _ref_diameter(vals), vals

    def test_lca(self):
        vals = [8, 3, 10, 1, 6, 14, 4]
        for a, b in [(1, 6), (1, 4), (4, 14), (3, 10), (1, 14)]:
            got = lca_bt.trace(vals, a, b)["meta"]["lca"]
            assert got == _ref_lca(vals, a, b), (a, b, got)

    def test_lca_found_flag(self):
        # the final step marks the LCA node green
        steps = lca_bt.trace([8, 3, 10, 1, 6], 1, 6)["steps"]
        assert steps[-1]["structures"]["found"] is True

    def test_steps_carry_tree(self):
        for tr, vals in ((level_order, CASES[0]), (tree_max_depth, CASES[0]),
                         (tree_diameter, CASES[0])):
            first = tr.trace(vals)["steps"][0]["structures"]
            assert first["tree"], tr.__name__


class TestEndpoints:
    def test_all_listed(self):
        ids = {a["id"] for a in client.get("/api/trace/algorithms").json()["algorithms"]}
        assert {"level_order", "tree_max_depth", "tree_diameter", "lca_bt"} <= ids

    def test_endpoints_ok(self):
        payloads = [
            ("level_order", {"array": [8, 3, 10, 1, 6, 14, 4]}),
            ("tree_max_depth", {"array": [8, 3, 10, 1, 6, 14, 4]}),
            ("tree_diameter", {"array": [8, 3, 10, 1, 6, 14, 4]}),
            ("lca_bt", {"text": "8,3,10,1,6,14,4 | 1 6"}),
        ]
        for algo, p in payloads:
            r = client.post("/api/trace", json={"algorithm": algo, **p})
            assert r.status_code == 200, (algo, r.text)
            assert r.json()["steps"]

    def test_validation(self):
        # empty array rejected
        assert client.post("/api/trace", json={"algorithm": "level_order", "array": []}).status_code == 400
        # too many values
        assert client.post("/api/trace", json={"algorithm": "tree_diameter",
                                               "array": list(range(20))}).status_code == 400
        # lca needs the pipe + two targets
        assert client.post("/api/trace", json={"algorithm": "lca_bt", "text": "8,3,10"}).status_code == 400
        assert client.post("/api/trace", json={"algorithm": "lca_bt", "text": "8,3,10 | 8"}).status_code == 400
        # targets must exist in the tree
        assert client.post("/api/trace", json={"algorithm": "lca_bt", "text": "8,3,10 | 3 99"}).status_code == 400
        # distinct values required
        assert client.post("/api/trace", json={"algorithm": "lca_bt", "text": "8,8,3 | 8 3"}).status_code == 400

    def test_detect_resolves(self):
        for algo in ("level_order", "tree_max_depth", "tree_diameter", "lca_bt"):
            body = client.post("/api/detect", json={"code": "", "problem": algo}).json()
            assert body["algorithm"] == algo
            assert body["realworld"]["scene"] and body["realworld"]["title"]
