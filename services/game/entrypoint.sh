#!/usr/bin/env bash
# Entry point for the RPSLS Game Service container.
#
# 1. Applies any pending Alembic migrations (safe to run repeatedly).
# 2. Launches Uvicorn under PID 1 so it receives signals correctly.
#
# Environment variables respected:
#   - HOST (default: 0.0.0.0)
#   - PORT (default: 8000)
#   - WORKERS (optional): number of Uvicorn workers.
#
# Fail fast on any error and propagate signals.
set -euo pipefail

# Run migrations (no-op if already at head)
alembic upgrade head

# Start the FastAPI service
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

APP_MODULE="${ASGI_APP:-services.game.app.main:app}"

# shellcheck disable=SC2236
if [[ -n "${WORKERS:-}" ]]; then
    exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --workers "$WORKERS"
else
    exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT"
fi 