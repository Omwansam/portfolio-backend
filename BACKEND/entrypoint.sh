#!/bin/sh
set -e

if [ -n "${DATABASE_URL}" ] && [ -n "${DB_HOST}" ]; then
  echo "Waiting for database at ${DB_HOST}:${DB_PORT:-5432}..."
  until nc -z "${DB_HOST}" "${DB_PORT:-5432}"; do
    sleep 1
  done
fi

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running database migrations..."
  flask --app server.app db upgrade
fi

exec "$@"
