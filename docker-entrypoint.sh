#!/bin/sh


echo "Activating venv"
. /venv/bin/activate
echo;
echo "Migrating"
python manage.py migrate --noinput
echo;
echo "Running the server on port $PORT"
python manage.py runserver 0.0.0.0:$PORT
