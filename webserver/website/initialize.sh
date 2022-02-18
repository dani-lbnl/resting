#!/bin/sh
cd /srv/website
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
