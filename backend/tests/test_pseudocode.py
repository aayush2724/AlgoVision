"""Pseudocode panel data (frontend/data/pseudocode.json).

Each line may carry `when`, a case-insensitive regex the engine tests against
a step's note; the first matching line is lit. These tests replay every step
of each algorithm's offline sample trace (the real trace of its default
input) and require that every step lands on a line — so pseudocode can't
drift out of step with its tracer's notes unnoticed.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PSEUDO = json.loads((ROOT / "frontend/data/pseudocode.json").read_text())
PSEUDO.pop("_about", None)
DATA = (ROOT / "frontend/js/data.js").read_text()
IDS = set(re.findall(r'^  \{ id: "([^"]+)"', DATA, flags=re.M))
# Syntax that Python accepts but a JavaScript RegExp does not (or reads differently).
NOT_JS = ("(?P", "(?i", "(?#", "\\A", "\\Z", "(?<=", "(?<!")


def compiled(algo):
    return [(re.compile(l["when"], re.I) if "when" in l else None) for l in PSEUDO[algo]]


def test_entries_are_catalog_algorithms_with_valid_lines():
    assert PSEUDO
    for algo, lines in PSEUDO.items():
        assert algo in IDS, algo
        assert lines and all(isinstance(l.get("code"), str) and l["code"].strip() for l in lines)
        assert any("when" in l for l in lines), algo
        for l in lines:
            if "when" in l:
                assert not any(t in l["when"] for t in NOT_JS), (algo, l["when"])
                re.compile(l["when"])


def test_every_sample_step_lands_on_a_line():
    for algo in PSEUDO:
        pats = compiled(algo)
        steps = json.loads((ROOT / f"frontend/offline/{algo}.json").read_text())["steps"]
        for s in steps:
            note = s.get("note", "")
            assert any(p and p.search(note) for p in pats), f"{algo}: no line for {note!r}"
