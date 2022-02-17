#!/bin/bash
# Check for Python executable name
if python3 -V
then
    PYTHON=python3
elif python -V
then
    PYTHON=python
else
    echo Could not find Python executable, edit start.sh and set the PYTHON variable to the executable location.
    exit
fi
# If this script was unable to find the Python executable, delete the if-block above and set the PYTHON variable to the executable location.

# Assume that we're starting in the resting directory, should check for this
APP_NAME=`$PYTHON -c "import project;print(project.app_name)"`
cd ..
TOP=`pwd`
# To provide website documentation create a working directory for Sphinx in the project directory
cd $TOP/webserver
mkdir doc
cd doc
# Create skeleton Sphinx files for website documentation
$PYTHON -m sphinx.cmd.quickstart -q -p $APP_NAME -a 'Generated by RESTInG' -v '' --ext-autodoc --extensions=sphinx.ext.napoleon
echo -e "\nimport os\nimport sys\nsys.path.append(os.path.abspath('../../resting'))\nautodoc_mock_imports=['urllib','urllib.request','request','json','ssl','project','csv','re']\n" >> conf.py
# Generate the Django site files
cd $TOP/resting
$PYTHON generate_rest_site.py
# Create static directory for the app
cd $TOP/webserver/website/$APP_NAME
mkdir static
cd static
mkdir $APP_NAME

# Create static subdirectory for hosting Sphinx-generated documentation
cd $APP_NAME
mkdir doc

# Create static directory for hosting downloads
mkdir downloads

# Copy the REST client Python module to the downloads folder
cp $TOP/resting/rest_client.py downloads
