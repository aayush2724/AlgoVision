"""The ML service must only answer the backend.

Run from ml-service/:  python3 -m pytest tests/
"""
from fastapi.testclient import TestClient

from app import main
from app.config import settings

client = TestClient(main.app)


def _with_token(monkeypatch, value):
  monkeypatch.setattr(settings, "INTERNAL_TOKEN", value)


def test_health_is_always_open(monkeypatch):
  _with_token(monkeypatch, "secret")
  assert client.get("/health").status_code == 200


def test_token_required_when_configured(monkeypatch):
  _with_token(monkeypatch, "secret")
  r = client.post("/bugfind", json={"language": "python", "code": "x = 1"})
  assert r.status_code == 403
  assert r.json() == {"detail": "Forbidden."}


def test_wrong_token_rejected(monkeypatch):
  _with_token(monkeypatch, "secret")
  r = client.post("/bugfind", json={"language": "python", "code": "x = 1"},
                  headers={"X-Internal-Token": "nope"})
  assert r.status_code == 403


def test_matching_token_accepted(monkeypatch):
  _with_token(monkeypatch, "secret")
  r = client.post("/bugfind", json={"language": "python", "code": "x = 1"},
                  headers={"X-Internal-Token": "secret"})
  assert r.status_code == 200
  assert "hints" in r.json()


def test_private_ip_does_not_bypass_a_configured_token(monkeypatch):
  # A hosting proxy's private address must not count as "internal" once a
  # token is in play — that was the hole on Render.
  _with_token(monkeypatch, "secret")
  monkeypatch.setattr(main, "_is_internal", lambda host: True)
  r = client.post("/explain", json={"algorithm": "bfs", "step": {}, "level": "beginner"})
  assert r.status_code == 403


def test_without_token_private_callers_are_allowed(monkeypatch):
  _with_token(monkeypatch, "")
  monkeypatch.setattr(main, "_is_internal", lambda host: True)
  r = client.post("/explain", json={"algorithm": "bfs", "step": {}, "level": "beginner"})
  assert r.status_code == 200


def test_without_token_public_callers_are_blocked(monkeypatch):
  _with_token(monkeypatch, "")
  monkeypatch.setattr(main, "_is_internal", lambda host: False)
  r = client.post("/explain", json={"algorithm": "bfs", "step": {}, "level": "beginner"})
  assert r.status_code == 403
