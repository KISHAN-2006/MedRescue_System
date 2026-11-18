#!/usr/bin/env bash
set -e
echo ">>> Running database migrations..."
alembic upgrade head
echo ">>> Seeding demo data..."
python -m app.seed
echo ">>> Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
