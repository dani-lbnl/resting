#!/bin/sh
openssl req -new -newkey rsa:2048 -nodes -keyout covidscreen.lbl.gov.key -out covidscreen.lbl.gov.csr
