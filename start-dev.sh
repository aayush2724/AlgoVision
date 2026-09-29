#!/usr/bin/env bash
# Run AlgoVision locally without Docker.
#
# The backend serves the frontend directory itself (same origin, no CORS,
# edits to frontend/ are live), so only two processes are needed:
#   backend    -> http://localhost:${PORT:-8000}    (app + API; docs at /docs)
#   ml-service -> http://localhost:${ML_PORT:-8500}
#
# If a port is taken by something else (another project's container, say)
# the script moves to the next free one and prints the URL — it never kills
# another process. Requires python3 with backend/requirements.txt and
# ml-service/requirements.txt installed.
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

port_free() {
  if command -v ss >/dev/null 2>&1; then
    ! ss -ltn 2>/dev/null | awk '{print $4}' | grep -qE "[:.]$1$"
  else
    ! (echo > "/dev/tcp/127.0.0.1/$1") >/dev/null 2>&1
  fi
}

pick_port() {                       # pick_port <preferred> <fallbacks...>
  local p
  for p in "$@"; do
    if port_free "$p"; then echo "$p"; return; fi
  done
  echo "No free port among: $*" >&2
  exit 1
}

API_PORT="$(pick_port "${PORT:-8000}" 8001 8002 8003 8123 8124)"
ML_PORT="$(pick_port "${ML_PORT:-8500}" 8501 8502 8503)"
[ "$API_PORT" != "${PORT:-8000}" ] && echo "Port ${PORT:-8000} is busy — using $API_PORT for the app."
[ "$ML_PORT" != "${ML_PORT_WANTED:-8500}" ] && [ "$ML_PORT" != "8500" ] && echo "Port 8500 is busy — using $ML_PORT for the ML service."

echo "Starting AlgoVision"
echo "  app + API   -> http://localhost:$API_PORT   (docs at /docs)"
echo "  ml-service  -> http://localhost:$ML_PORT"

cleanup() {
  echo
  echo "Shutting down..."
  kill 0
}
trap cleanup EXIT

( cd "$ROOT/ml-service" && exec python3 -m uvicorn app.main:app --port "$ML_PORT" ) &
( cd "$ROOT/backend" && ML_SERVICE_URL="http://localhost:$ML_PORT" \
    exec python3 -m uvicorn app.main:app --port "$API_PORT" ) &

wait
