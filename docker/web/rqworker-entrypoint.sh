#!/bin/bash

# Allow Cloud Run to ping PORT
nohup python -m http.server -d /dev/null "$PORT" &

poetry run python manage.py rqworker default