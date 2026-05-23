#!/usr/bin/env bash
# docker-entrypoint.sh — wait for Postgres, apply migrations, collect static, then exec CMD.
set -euo pipefail

DB_HOST="${POSTGRES_HOST:-db}"
DB_PORT="${POSTGRES_PORT:-5432}"

echo "[entrypoint] Waiting for Postgres at ${DB_HOST}:${DB_PORT} ..."
until nc -z "${DB_HOST}" "${DB_PORT}"; do
  sleep 1
done
echo "[entrypoint] Postgres is up."

echo "[entrypoint] Running migrations ..."
python manage.py migrate --noinput

echo "[entrypoint] Collecting static files ..."
python manage.py collectstatic --noinput

echo "[entrypoint] Starting: $*"
exec "$@"
