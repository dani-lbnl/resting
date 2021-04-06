#!/bin/sh
#cd website/database
#python3 ../../../metadata/generate_fields.py
#sed -f sed_script_views.py views_template.py > views.py
#cd ../../
docker build -t acts_webserver:3.7 -t registry.nersc.gov/m3670/acts_webserver:3.7 .
