#!/bin/bash
set -e

# Allow Cloud Run to ping PORT
python -m http.server -d /dev/null "$PORT"

poetry run python manage.py rqworker default &

wait -n