#!/bin/bash

until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo
echo "Database is available"

if [ "$DEBUG" = 0 ]; then
    echo "Production mode"
    echo "==============="
    echo "Collecting static files to /app/staticfiles"
    poetry run ./manage.py collectstatic --no-input --clear
else
    echo "Debug mode"
    echo "=========="
fi

echo
echo "Running migrations"
poetry run ./manage.py migrate --no-input
migration_success=$?

if [ "$migration_success" = 0 ]; then
    echo
    echo "Preparng DB"
    poetry run ./manage.py prepare_db
else
    echo "Migrations failed"
    echo "================="
fi

echo
echo "Compiling messages"
poetry run ./manage.py compilemessages -i venv

echo "Running the server on port $PORT"
poetry run celery -A manga_reader.celery.app worker -n manga@%h --loglevel=INFO -B &
poetry run ./manage.py runserver 0.0.0.0:$PORT
