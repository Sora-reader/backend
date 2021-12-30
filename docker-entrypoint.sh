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

until curl --output /dev/null --silent --head --fail "http://$ELASTICSEARCH_HOST"; do
    echo >&2 "Elasticsearch is unavailable - sleeping"
    sleep 1
done
echo
echo "Rebuilding index"
./manage.py search_index --rebuild -f

PORT="${PORT:-8000}"
echo "Running the server on port $PORT"

core_count=$(grep 'cpu[0-9]' /proc/stat | wc -l)
gunicorn manga_reader.wsgi:application --bind 127.0.0.1:$PORT --workers $(expr $core_count \* 2 + 1)
