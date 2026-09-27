"""Build the offline sample traces: frontend/offline/<algorithm id>.json.

When the API can't be reached, the Experience page replays one of these —
the genuine trace of the algorithm's DEFAULT input — instead of guessing.
(Only a handful of classic algorithms have an in-browser emulator that can
trace a student's own input offline.)

Input: tools/offline_payloads.json, the exact request body the engine sends
for each algorithm's default input (see tools/capture_offline_payloads.js).
Each request is replayed through the real backend app in-process.

    python tools/build_offline_traces.py

Every file holds {"request": <body>, "meta": ..., "steps": ...} (plus any
extra top-level fields the tracer returns, e.g. "array").
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = ROOT / "tools" / "offline_payloads.json"
OUT = ROOT / "frontend" / "offline"


def main():
    os.environ["ALGOVISION_DISABLE_RATELIMIT"] = "1"
    sys.path.insert(0, str(ROOT / "backend"))
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    payloads = json.loads(PAYLOADS.read_text())
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.json"):
        old.unlink()
    failed, total = [], 0
    for algo, body in sorted(payloads.items()):
        r = client.post("/api/trace", json=body)
        if r.status_code != 200:
            failed.append((algo, r.status_code, r.text[:120]))
            continue
        data = {"request": body, **r.json()}
        text = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
        (OUT / f"{algo}.json").write_text(text)
        total += len(text)
    print(f"wrote {len(payloads) - len(failed)} traces, {total / 1024:.0f} KiB")
    for f in failed:
        print("FAILED", *f)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
