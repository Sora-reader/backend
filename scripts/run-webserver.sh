#!/usr/bin/env bash

HOST="${HOST:=0.0.0.0}"
PORT="${PORT:=8000}"

# Get core count
core_count=$(grep 'cpu[0-9]+' /proc/stat | wc -l)
# Calculate worker count, max 12
worker_count=$(expr $core_count \* 2 + 1)
worker_count=$([ "$worker_count" -gt 12 ] && echo 12 || echo "$worker_count")

info "Running the server on $HOST:$PORT"
gunicorn manga_reader.asgi:application \
  --host $HOST --port $PORT --workers $core_count
