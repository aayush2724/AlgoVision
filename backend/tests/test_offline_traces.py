"""Offline fallback: every catalog algorithm must have a sample trace that
still matches what the backend produces for its default input.

If this fails after changing a tracer or a default input, rebuild with
`python tools/build_offline_traces.py` (and re-capture the payload with
tools/capture_offline_payloads.js if the default input itself changed).
"""

import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

ROOT = Path(__file__).resolve().parents[2]
PAYLOADS = json.loads((ROOT / "tools/offline_payloads.json").read_text())
OFFLINE = ROOT / "frontend/offline"
DATA = (ROOT / "frontend/js/data.js").read_text()
ENGINE = (ROOT / "frontend/js/engine.js").read_text()
IDS = re.findall(r'^  \{ id: "([^"]+)"', DATA, flags=re.M)
client = TestClient(app)


def test_every_algorithm_has_a_payload_and_a_sample():
    assert set(PAYLOADS) == set(IDS)
    for algo in IDS:
        assert PAYLOADS[algo]["algorithm"] == algo
        sample = json.loads((OFFLINE / f"{algo}.json").read_text())
        assert sample["request"] == PAYLOADS[algo], algo
        assert sample["steps"], algo


def test_samples_match_the_live_tracers():
    for algo in IDS:
        r = client.post("/api/trace", json=PAYLOADS[algo])
        assert r.status_code == 200, (algo, r.text)
        sample = json.loads((OFFLINE / f"{algo}.json").read_text())
        live = r.json()
        assert len(live["steps"]) == len(sample["steps"]), \
            f"{algo}: offline sample is stale — run tools/build_offline_traces.py"
        assert [s.get("note") for s in live["steps"]] == \
            [s.get("note") for s in sample["steps"]], algo


def test_emulated_ids_exist():
    block = re.search(r"const EMULATED = new Set\(\[(.*?)\]\)", ENGINE, flags=re.S).group(1)
    emulated = set(re.findall(r"'([a-z_0-9]+)'", block))
    assert emulated and emulated <= set(IDS)
