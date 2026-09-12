import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

GRAPH = {
    "nodes": [{"id": "A"}, {"id": "B"}, {"id": "C"}],
    "edges": [["A", "B", 1], ["B", "C", 2]],
}


class TestTraceEndpoint:
    def test_dijkstra_trace_ok(self):
        r = client.post("/api/trace",
                        json={"algorithm": "dijkstra", "start": "A", "graph": GRAPH})
        assert r.status_code == 200
        body = r.json()
        assert body["meta"]["algorithm"] == "dijkstra"
        assert body["steps"][-1]["structures"]["dist"]["C"] == 3

    def test_unknown_algorithm_400(self):
        r = client.post("/api/trace",
                        json={"algorithm": "bogus", "start": "A", "graph": GRAPH})
        assert r.status_code == 400

    def test_missing_start_node_400(self):
        r = client.post("/api/trace",
                        json={"algorithm": "bfs", "start": "Z", "graph": GRAPH})
        assert r.status_code == 400

    def test_invalid_graph_422(self):
        bad = {"nodes": [{"id": "A"}], "edges": [["A", "Z", 1]]}
        r = client.post("/api/trace",
                        json={"algorithm": "bfs", "start": "A", "graph": bad})
        assert r.status_code == 422

    def test_algorithms_listing(self):
        r = client.get("/api/trace/algorithms")
        assert r.status_code == 200
        ids = {a["id"] for a in r.json()["algorithms"]}
        assert {"dijkstra", "bfs"} <= ids


class TestDetectEndpoint:
    def test_detects_dijkstra(self):
        code = "import heapq\ndist = {}\nheapq.heappush(pq, (0, s))  # dijkstra"
        r = client.post("/api/detect", json={"code": code})
        assert r.status_code == 200
        body = r.json()
        assert body["algorithm"] == "dijkstra"
        assert "realworld" in body


class TestAIEndpoint:
    def test_code_with_prose_phrases_is_accepted(self):
        # The old injection blocklist 422'd legitimate code containing
        # phrases like "act as" — this must stay accepted.
        code = "# this variable will act as a stack\nstack = []"
        r = client.post("/api/ai/bugfind",
                        json={"language": "python", "code": code})
        assert r.status_code == 200
        assert "hints" in r.json()  # live or offline fallback, either way

    def test_unknown_language_normalised(self):
        r = client.post("/api/ai/bugfind",
                        json={"language": "cobol", "code": "x = 1"})
        assert r.status_code == 200

    def test_health(self):
        r = client.get("/api/health")
        assert r.status_code == 200


class TestMLServiceURL:
    """Render's `fromService: property: host` yields a bare hostname with no
    scheme. httpx refuses to parse that, so every AI call fell through to the
    offline fallback with no visible error."""

    @pytest.mark.parametrize("raw,expected", [
        ("algovision-ml-abc.onrender.com", "https://algovision-ml-abc.onrender.com"),
        ("http://localhost:8500",          "http://localhost:8500"),
        ("localhost:8500",                 "http://localhost:8500"),
        ("https://x.onrender.com/",        "https://x.onrender.com"),
        ("",                               ""),
    ])
    def test_scheme_is_normalised(self, raw, expected, monkeypatch):
        monkeypatch.setenv("ML_SERVICE_URL", raw)
        from app.config import Settings
        assert Settings().ml_service_url == expected
