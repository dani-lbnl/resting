# There are version problems with mod_wsgi and psycopg2 in the latest (3.8) image, so stay with 3.7
FROM python:3.7

RUN apt-get update && apt-get -y install python3-djangorestframework apache2 libapache2-mod-wsgi-py3 python3-djangorestframework-filters

ENV PYTHONPATH /usr/lib/python3/dist-packages

EXPOSE 8000

WORKDIR /

# Copy in file(s) used to modify stock Apache file(s)
COPY apache etc/apache2/

# In order to access the CFS, this container will run as a NERSC user. This user will not have root privileges in this container, but will be in the root group. Some directory and file permissions must be changed in order for this user to run Apache properly.
# Apache configuration is done here through modification of the stock configuration files.
# Django is then directed to create the skeleton website
RUN umask 007 && chmod -R g+w /var/run/apache2 && chgrp -R root /var/log/apache2 && chmod -R g+w /var/log/apache2 && cd /etc/apache2 && cat append_to_apache2.conf >> apache2.conf && mv ports.conf dist_ports.conf && sed 's/Listen 80/Listen 8000/' dist_ports.conf > ports.conf && cd sites-available && mv 000-default.conf dist_000-default.conf && sed 's/VirtualHost \*:80/VirtualHost \*:8000/' dist_000-default.conf > 000-default.conf && chmod g+rwx /srv && cd /srv && mkdir static && chmod o+x static && chmod g+rwx static && django-admin startproject website && chmod g+rwx website && cd website && \
python manage.py startapp database

# Now that the website skeleton exists, copy in files for customization
COPY website srv/website/

# Use sed scripts to modify stock files, also copy static ifiles
RUN cp /srv/website/templates/* /usr/lib/python3/dist-packages/rest_framework/templates/rest_framework/ && cd /srv/website/website && mv settings.py dist_settings.py && sed -f sed_script_settings.py dist_settings.py > settings.py && cd /srv/website && python manage.py collectstatic

# Run the web server in the foreground so that the container does not immediately exit
CMD ["/usr/sbin/apache2ctl","-DFOREGROUND","-kstart"]
