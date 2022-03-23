#!/bin/sh
# Under podman, it seems that the earlier mode assignment does not hold
chmod a+rwx /srv/media
cd /srv/website
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
