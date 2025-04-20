#!/bin/bash
set -e

echo "Current environment: $ENV"

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running Alembic migrations..."
  PYTHONPATH=. alembic upgrade head
else
  echo "Skipping Alembic migrations."
fi

echo "Starting API..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
