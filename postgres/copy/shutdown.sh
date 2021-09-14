#!/bin/sh
kill `head -1 /var/lib/postgres/data/postmaster.pid`
