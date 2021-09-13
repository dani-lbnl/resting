#!/bin/sh
. stop_db.sh
docker container restart db
