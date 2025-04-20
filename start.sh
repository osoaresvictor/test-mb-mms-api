#!/bin/bash

echo "Current environment: $ENV"

if [ "$ENV" = "prod" ]; then
  echo "Skipping Alembic migration in production."
else
  echo "Running Alembic migrations..."
  PYTHONPATH=. alembic upgrade head
fi

echo "Starting API..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
