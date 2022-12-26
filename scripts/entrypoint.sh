#!/usr/bin/env bash

 . "$(poetry env info --path)/bin/activate"

function info () {
    echo ""
    echo "$1"
    echo "==============="
    echo "$2"
}
export -f info

info "Waiting for postgres"
until psql "$DATABASE_URL" -c ';'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

info "Running migrations"
python ./manage.py migrate --no-input

info "Waiting for typesense"
until curl "http://$TYPESENSE_HOST:8108/health"; do
    echo >&2 "Typesense is unavailable - sleeping"
    sleep 1
done

./scripts/run-webserver.sh
