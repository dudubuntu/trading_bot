#!/bin/bash

sleep 3

if [[ $MAKE_MIGRATIONS == "True" ]]
    then
        python manage.py makemigrations --no-input

        python manage.py makemigrations admin_proj --no-input

        python manage.py migrate --no-input

        python manage.py migrate admin_proj --no-input

        python manage.py createsuperuser --no-input
fi

if [[ $COLLECT_STATIC == "True" ]]
    then
        python manage.py collectstatic --no-input
fi

# python manage.py runserver
python manage.py runcrons --force

python manage.py runcrons

exec gunicorn admin_proj.wsgi:application -b 0.0.0.0:8000 --reload