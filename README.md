# AlgoVision

> See the algorithm **before** you ever see the code.

AlgoVision is a learning engine for data structures & algorithms, built for
colleges and self-learners. Instead of teaching syntax first, it reveals what
an algorithm *means* in the real world (Hook → Reveal → Mechanics), then lets
students **run it on their own input, step by step, and analyse the cost**.

## What it actually does

- **15 live algorithm tracers** — Dijkstra, BFS, DFS, Binary Search, Merge /
  Quick / Bubble / Insertion / Selection Sort, Linked-List Reversal, Balanced
  Brackets (stack), BST build & search, Max-Heap build, and memoized
  Fibonacci (DP) — every step computed by the backend from *your* input,
  never a canned animation.
- **Bring your own data** — build a graph by clicking (add/delete nodes and
  edges, edit weights, pick the start node, teaching presets including a
  disconnected graph), paste your own numbers for the array algorithms, pick
  n for the DP table.
- **Step scrubber** — play/pause with speed control, step forward *and
  backward*, drag to any step. Every frame renders from real trace data.
- **Analysis layer** — live operation counters (relaxations, heap pushes,
  comparisons, swaps, cache hits…), a compare mode that runs BFS vs Dijkstra
  side-by-side on the same graph with synced scrubbing, and per-algorithm
  complexity cards that read *your* numbers back in plain language.
- **Metaphor narration** — every algorithm runs inside a real-world scene
  (GPS routing, friend discovery, maze robot, library catalog, leaderboard,
  memo vault), with an optional AI narrator (beginner / intermediate /
  advanced) grounded in the live algorithm state.
- **Real progress tracking** — per-problem viewed/understood status across
  the A2Z roadmap, trace counts, streaks, and a Journey dashboard. Stored in
  the browser; exportable/importable as JSON.
- **Paste-any-code detection** — paste DSA code and AlgoVision detects the
  algorithm and launches the right visual world.
- **Works fully offline** — every tracer has an in-browser emulator and the
  AI narrator has template fallbacks, so nothing breaks without a backend or
  an API key.

## Structure

```
algovision/
├─ frontend/      # Buildless ES modules: Three.js + GSAP + SVG tracers
├─ backend/       # FastAPI: trace engine (7 algorithms), detect, AI proxy
├─ ml-service/    # FastAPI AI microservice (explain a step, find a bug)
├─ docker-compose.yml
├─ start-dev.sh   # Run all three services locally
└─ README.md
```

## Run it

### Option A — one script (no Docker)
```bash
pip install -r backend/requirements.txt -r ml-service/requirements.txt
bash start-dev.sh
```

### Option B — Docker
```bash
docker compose up --build
```

Then open:
- Frontend: http://localhost:5500 (or http://localhost:8080 via Docker)
- API docs: http://localhost:8000/docs
- ML health: http://localhost:8500/health (start-dev.sh only — under Docker the
  ML service is internal to the compose network and not published)

## For educators

- **Zero-setup classroom mode**: the frontend alone (any static file server)
  gives students the full experience — tracers, scrubbing, counters, progress —
  via the offline emulators. The backend adds server-side tracing and the AI
  narrator, but nothing *requires* it.
- **Students keep their progress**: it lives in each student's browser and can
  be exported as a JSON file from the Journey page — useful for handing in,
  moving machines, or restoring after a wipe.
- **Teach reachability**: the graph editor ships a "Disconnected" preset;
  unreachable nodes show `—` and the trace names them.
- **Teach complexity honestly**: the counters are real operation counts from
  the actual run, and compare mode shows BFS vs Dijkstra doing measurably
  different work on the same graph.
- **Level the narration**: the AI narrator has beginner / intermediate /
  advanced tones (requires a `GROQ_API_KEY` in `ml-service/.env`; without it,
  clean template narration is used).

## Tests

```bash
cd backend && python3 -m pytest tests/
```

## Environment

Copy the example files and adjust as needed:
```bash
cp backend/.env.example backend/.env
cp ml-service/.env.example ml-service/.env
```

Add `GROQ_API_KEY` to `ml-service/.env` to enable live AI narration; without
it the service returns high-quality template responses.

---
Inspired by takeuforward's A2Z DSA sheet (not affiliated).
