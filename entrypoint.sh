#!/bin/sh
set -e

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

alembic upgrade head

python -m app.seeds.seed

uvicorn app.main:app --host 0.0.0.0 --port 8000
