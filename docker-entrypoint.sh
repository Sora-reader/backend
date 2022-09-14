#!/bin/bash

function info () {
    echo ""
    echo "$1"
    echo "==============="
    echo "$2"
}
function is_debug() {
    [ ! "$DEBUG" = 0 ]
}

if $(is_debug); then
    info "Debug mode" "Installing dependencies"
    sudo chown sora:sora ~/.cache/pypoetry/
    poetry install
else
    info "Production mode" "Collecting static files to /app/staticfiles"
    poetry run ./manage.py collectstatic --no-input --clear
fi

info "Waiting for postgres"
until psql "$DATABASE_URL" -c ';'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

info "Running migrations"
poetry run ./manage.py migrate --no-input

info "Waiting for elasticsearch"
until curl "http://$ELASTICSEARCH_HOST/_cat/health"; do
    echo >&2 "Elasticsearch is unavailable - sleeping"
    sleep 1
done

info "Rebuilding index"
poetry run ./manage.py search_index --rebuild -f

# Get core count
core_count=$(grep 'cpu[0-9]+' /proc/stat | wc -l)
# Calculate worker count, max 12
worker_count=$(expr $core_count \* 2 + 1)
worker_count=$([ "$worker_count" -gt 12 ] && echo 12 || echo "$worker_count")

info "Running the server on $HOST:$PORT"
poetry run uvicorn manga_reader.asgi:application \
  $(is_debug && echo --reload) \
  --host $HOST --port $PORT --workers $core_count
