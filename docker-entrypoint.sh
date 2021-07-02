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
    ./manage.py collectstatic --no-input --clear
else
    echo "Debug mode"
    echo "=========="
fi

echo
echo "Running migrations"
./manage.py migrate --no-input

echo
echo "Compiling messages"
./manage.py compilemessages -i venv

echo "Running the server on port $PORT"

if [ "$RUN_CELERY" = 1 ]; then
    echo "Running celery worker"
    echo "====================="
    celery -A manga_reader.celery.app worker -n manga@%h --loglevel=INFO -B &
fi

./manage.py runserver 0.0.0.0:$PORT
