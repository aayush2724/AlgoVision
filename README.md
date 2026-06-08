# AlgoVision

> See the algorithm **before** you ever see the code.

AlgoVision is an inspiration engine for data structures & algorithms — in the
spirit of 3Blue1Brown, Brilliant and Kurzgesagt. Instead of teaching syntax
first, it reveals what an algorithm *means* in the real world, then pulls back
the curtain on how it works (Hook → Reveal → Mechanics).

This repo is a small, focused full-stack build — only the pieces the project
actually needs.

## Structure

```
algovision/
├─ frontend/      # Cinematic 3D website (Three.js + GSAP, buildless ES modules)
├─ backend/       # FastAPI API: health, trace engine, AI proxy
├─ ml-service/    # FastAPI AI microservice (explain a step, find a bug)
├─ docker-compose.yml
├─ start-dev.sh   # Run all three services locally
└─ README.md
```

### frontend/
A single cinematic landing experience: a Three.js node-constellation hero,
scroll-driven story acts, the A2Z \"worlds\", an AI feature grid, and a **live
engine** section that calls the backend to trace Dijkstra on a sample graph
(with an in-browser fallback if the API is offline). No build step — just static
files and CDN modules.

### backend/
FastAPI app exposing:
- `GET  /api/health`
- `GET  /api/trace/algorithms`
- `POST /api/trace`           — returns step-by-step trace (Dijkstra, BFS)
- `POST /api/ai/explain`      — proxied to the ML service (offline fallback)
- `POST /api/ai/bugfind`      — proxied to the ML service (offline fallback)

### ml-service/
A standalone FastAPI service that holds the AI logic (`/explain`, `/bugfind`).
It is provider-ready (Groq / Gemini via env vars) and ships with a template
fallback so everything works offline.

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
- ML health: http://localhost:8500/health

## Environment
Copy the example files and adjust as needed:
```bash
cp backend/.env.example backend/.env
cp ml-service/.env.example ml-service/.env
```

Add `GROQ_API_KEY` or `GEMINI_API_KEY` to `ml-service/.env` to enable live AI;
without them the service returns high-quality template responses.

---
Inspired by takeuforward's A2Z DSA sheet (not affiliated).
