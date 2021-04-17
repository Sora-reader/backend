#!/bin/sh


echo "Activating venv"
. /venv/bin/activate
echo;
echo "Migrating"
python manage.py migrate --noinput
echo;
if [ -n $DEBUG ]; then
    echo "Production mode, collecting static"
    python manage.py collectstatic --noinput --clear
    echo;
fi
echo "Running the server on port $PORT"
celery -A manga_reader.celery.app worker -n manga@%h --loglevel=INFO -B;
python manage.py runserver 0.0.0.0:$PORT
echo;

