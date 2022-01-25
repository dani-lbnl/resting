#!/bin/sh
cd ..
# Create skeleton Sphinx files for RESTInG documentation
mkdir doc
cd doc
sphinx-quickstart -q -p 'REST Interface Generator (RESTInG)' -a 'Regents of the University of California' -v ''
# Link in the RESTInG documentation source files
rm index.rst
ln -s ../resting_doc_source/* .
# Use Sphinx to generate site documentation
make html
cd _build/html
echo To view RESTInG\'s documentation, including setup instructions, open a web browser and open the following file: `pwd`/index.html
echo or try this URL: file://`pwd`/index.html
