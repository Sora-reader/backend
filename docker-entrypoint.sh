#!/bin/bash
source /venv/bin/activate
echo $(ls -a /venv/bin)

poetry run manage.py

#python manage.py migrate --no-input
#python manage.py flush --no-input
#python manage.py runserver 0.0.0.0:8000