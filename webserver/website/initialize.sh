#!/bin/bash
cd /srv/website
python makemigrations
python migrate
python createsuperuser

