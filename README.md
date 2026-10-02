# AlgoVision

> See the algorithm **before** you ever see the code.

AlgoVision is a learning engine for data structures & algorithms, built for
colleges and self-learners. Instead of teaching syntax first, it reveals what
an algorithm *means* in the real world (Hook → Reveal → Mechanics), then lets
students **run it on their own input, step by step, and analyse the cost**.

## What it actually does

- **474 live algorithm tracers** — graphs (Dijkstra, BFS, DFS, MSTs,
  Bellman-Ford, SCCs…), sorting, searching, sliding windows, stacks and
  queues, trees and heaps, strings, greedy, dynamic programming and number
  theory — every step computed by the backend from *your* input, never a
  canned animation. The A2Z roadmap links each sheet row to one of them
  where a trace exists.
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
- **Degrades honestly offline** — 23 classic algorithms have an in-browser
  emulator that traces your own input; every other algorithm replays the
  built-in trace of its sample input, labelled as such. The AI narrator has
  template fallbacks, so nothing breaks without a backend or an API key.

## Structure

```
algovision/
├─ frontend/      # Buildless ES modules: Three.js + GSAP + SVG tracers
├─ backend/       # FastAPI: trace engine, code detection, AI proxy
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
- App: http://localhost:8000 (or http://localhost:8080 via Docker). With the
  script, the backend serves the frontend directory itself, so there is one
  origin and edits to `frontend/` are live on reload. If port 8000 is busy the
  script picks the next free one and prints the URL — it never kills another
  process. Override with `PORT=8123 bash start-dev.sh`.
- API docs: http://localhost:8000/docs
- ML health: http://localhost:8500/health (start-dev.sh only — under Docker the
  ML service is internal to the compose network and not published)

If the API is unreachable the status pill says so (`OFFLINE — SAMPLE TRACE
ONLY`), Run replays the built-in trace of the sample input, and your own input
stays in the box for when the server is back. A sleeping free-tier server
(Render) is waited out — Run shows `WAKING THE SERVER…` for up to 45 s.

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
cd ml-service && python3 -m pytest tests/
```

## Data & privacy

The privacy policy shown at `/privacy` (defined in `frontend/js/pages.js`) is
written from this list. Change both together.

- **Browser storage:** `algovision.progress.v1` and `algovision.game.v1` in
  localStorage. No cookies, no analytics, no accounts.
- **Sent to the API:** trace inputs, pasted code (detect / bug scan), and the
  current trace step (explain). Not stored; logs hold paths and errors only.
- **Sent to Groq** (only when `GROQ_API_KEY` is set): the step description for
  explanations, and pasted code for bug scans.
- **Third-party scripts:** GSAP from cdnjs on every page; three.js from
  jsDelivr on the desktop home page and the A2Z problem pages. Fonts are
  self-hosted under `frontend/fonts/` (SIL OFL, licence alongside).

Owner-supplied values (contact email, operator name) live in
`frontend/js/site.js`. Until they are set the site points people to GitHub
issues and says "the AlgoVision maintainers".

## Security headers

The CSP and other headers are defined once in `backend/app/security.py` and
copied into `vercel.json` and `frontend/nginx-headers.inc`;
`backend/tests/test_security.py` fails if the copies drift. If you edit an
inline `<script>` in `index.html`, run `python3 tools/csp_hashes.py` and
update the two hashes in all three places.

## Environment

Copy the example files and adjust as needed (every variable is documented
inside them; `.env` files are git-ignored):
```bash
cp backend/.env.example backend/.env
cp ml-service/.env.example ml-service/.env
```

Add `GROQ_API_KEY` to `ml-service/.env` to enable live AI narration; without
it the service returns high-quality template responses.

---
Inspired by takeuforward's A2Z DSA sheet (not affiliated).
