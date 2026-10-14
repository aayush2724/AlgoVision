"""Offline narration (no GROQ_API_KEY) must read as a sentence.

Run from ml-service/:  python3 -m pytest tests/
"""
from app import llm
from app.config import settings


def _offline(monkeypatch):
  monkeypatch.setattr(settings, "GROQ_API_KEY", "")


META = {"title": "Number of Islands",
        "metaphors": {"node": "cell", "visit": "Scanning"}}


def test_step_without_an_element_is_just_the_note(monkeypatch):
  _offline(monkeypatch)
  out = llm.explain_step("number_of_islands",
                         {"i": 3, "note": "Flood cell (1,2) from island #1", "highlight": {"cells": [[1, 2]]}},
                         "beginner", META)
  assert out["live"] is False
  assert out["text"] == "Flood cell (1,2) from island #1"
  assert "  " not in out["text"] and "()" not in out["text"]


def test_step_with_an_element_names_it_in_scene_language(monkeypatch):
  _offline(monkeypatch)
  out = llm.explain_step("dijkstra",
                         {"i": 2, "note": "Relax edge A->B", "highlight": {"node": "B"}},
                         "advanced", {"title": "GPS", "metaphors": {"node": "intersection", "visit": "Scanning"}})
  assert out["text"] == "Scanning B (intersection) — Relax edge A->B"
  assert out["level"] == "advanced" and out["scene"] == "GPS"


def test_missing_meta_still_works(monkeypatch):
  _offline(monkeypatch)
  out = llm.explain_step("bfs", {"note": "Dequeue A", "node": "A"}, "beginner", None)
  assert out["text"] == "Processing A (node) — Dequeue A"
