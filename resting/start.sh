#!/bin/sh
# Should check for Python executable name
if python3 -V
then
    PYTHON=python3
elif python -V
then
    PYTHON=python
else
    echo Could not find Python executable
    exit
fi
# Assume that we're starting in the resting directory, should check for this
APP_NAME=`$PYTHON -c "import project;print(project.app_name)"`
cd ..
TOP=`pwd`
# Create a working directory for Sphinx in the project directory
cd $TOP/webserver
mkdir doc
cd doc
sphinx-quickstart -q -p $APP_NAME -a 'Generated by RESTInG' -v ''
# Generate the Django site files
cd $TOP/resting
$PYTHON generate_rest_site.py
