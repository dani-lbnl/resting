#!/bin/bash
cd ..
# Create skeleton Sphinx files for RESTInG documentation
mkdir doc
cd doc
sphinx-quickstart -q --extensions=sphinx.ext.napoleon -p 'REST Interface Generator (RESTInG)' -a 'Regents of the University of California' -v ''
# Link in the RESTInG documentation source files
rm index.rst
ln -s ../resting_doc_source/* .
echo -e 'import os.path\nimport sys\nsys.path.append(os.path.abspath("..") + "/resting")' >> conf.py
# Use Sphinx to generate site documentation
make html
cd _build/html
echo To view RESTInG\'s documentation, including setup instructions, open a web browser and open the following file: `pwd`/index.html
echo or try this URL: file://`pwd`/index.html
