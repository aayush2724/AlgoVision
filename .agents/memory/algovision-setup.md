---
name: AlgoVision Setup
description: Architecture and key decisions for the AlgoVision app running in Replit
---

# AlgoVision Architecture

**Why:** Running FastAPI + vanilla JS frontend + ML service. Key decisions needed for Replit environment.

## Server Setup
- FastAPI (port 5000) serves BOTH the static frontend AND all `/api/*` routes via `StaticFiles` mount
- ML service runs separately on port 8000 with Groq API (offline fallback when key absent)
- No separate static server needed — `backend/` serves `frontend/` files

## Frontend
- Buildless vanilla JS with ES module importmap (no bundler)
- `window.ALGOVISION_API = ""` — empty string means same-origin API calls
- Three.js via importmap at `three@0.160.0`; GSAP via CDN (global `gsap`)
- Hash-based SPA router (`#/route`)

## 3D Visualizations (vizScenes.js)
- Each viz creates its own Three.js WebGLRenderer inside the container div
- Auto-cleanup: `!renderer.domElement.isConnected` check in animLoop stops the loop when navigating away
- WebGL fails in Replit headless screenshot (no GPU) — expected; graceful fallback message shown
- Try/catch in both `setup3D()` and in `pages.js` draw call for resilience
- 40+ viz types covering all A2Z problem categories

## Deployment
- Configured as `autoscale` target
- Run command: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8080`
- Working directory must be `backend/` (run from there)
