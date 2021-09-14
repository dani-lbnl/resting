#!/bin/sh
# http://httpd.apache.org/docs/current/stopping.html
docker exec ws apache2ctl -k stop
docker container stop ws
