#!/bin/sh
# https://www.postgresql.org/docs/12/server-shutdown.html
docker exec db 'kill `head -1 /var/lib/postgres/data/postmaster.pid`'
docker container stop db
