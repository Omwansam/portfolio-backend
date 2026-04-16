#!/bin/sh
set -e

if [ -n "${DATABASE_URL}" ]; then
  DB_HOST="$(python3 -c "from urllib.parse import urlparse; import os; print(urlparse(os.environ['DATABASE_URL']).hostname or '')")"
  DB_PORT="$(python3 -c "from urllib.parse import urlparse; import os; print(urlparse(os.environ['DATABASE_URL']).port or 5432)")"
  if [ -n "${DB_HOST}" ]; then
    echo "Waiting for database at ${DB_HOST}:${DB_PORT}..."
    until nc -z "${DB_HOST}" "${DB_PORT}"; do
      sleep 1
    done
  fi
fi

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running database migrations..."
  flask --app server.app db --directory server/migrations upgrade
fi

exec "$@"
