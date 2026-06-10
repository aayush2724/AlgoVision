#!/usr/bin/env bash
# Run the full AlgoVision stack locally without Docker.
# Requires: python3 with the deps in backend/requirements.txt and ml-service/requirements.txt.
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Free the ports we need in case a previous run is still holding them.
free_port() {
  if command -v fuser >/dev/null 2>&1; then
    fuser -k "$1/tcp" >/dev/null 2>&1 || true
  fi
}
free_port 8000
free_port 8500
free_port 5500
sleep 1

echo "Starting AlgoVision"
echo "  backend     -> http://localhost:8000  (docs at /docs)"
echo "  ml-service  -> http://localhost:8500"
echo "  frontend    -> http://localhost:5500"

cleanup() {
  echo
  echo "Shutting down..."
  kill 0
}
trap cleanup EXIT

( cd "$ROOT/ml-service" && python3 -m uvicorn app.main:app --port 8500 ) &
( cd "$ROOT/backend" && python3 -m uvicorn app.main:app --port 8000 ) &
( cd "$ROOT/frontend" && python3 -m http.server 5500 ) &

wait
