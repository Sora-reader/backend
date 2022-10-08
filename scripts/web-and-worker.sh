#!/usr/bin/env bash

nohup python manage.py rqworker default &

uvicorn main:app --port "$PORT" --workers 2