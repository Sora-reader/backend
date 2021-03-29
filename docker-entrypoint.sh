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
python manage.py runserver 0.0.0.0:$PORT
echo;
