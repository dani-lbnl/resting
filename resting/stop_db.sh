#!/bin/sh
# https://www.postgresql.org/docs/12/server-shutdown.html
docker exec db /shutdown.sh
docker container stop db
