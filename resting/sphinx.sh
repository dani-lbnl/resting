#!/bin/bash
cd ..
# Create skeleton Sphinx files for RESTInG documentation
mkdir doc
cd doc
# Creating aliases doesn't seem to work, -x is not recognized on a Mac
python3 -m sphinx.cmd.quickstart -q --extensions=sphinx.ext.napoleon -p 'REST Interface Generator (RESTInG)' -a 'Regents of the University of California' -v ''
# Link in the RESTInG documentation source files
rm index.rst
ln -s ../resting_doc_source/* .
echo -e '\nimport os.path\nimport sys\nsys.path.append(os.path.abspath("..") + "/resting")' >> conf.py
# Use Sphinx to generate site documentation
make SPHINXBUILD='python3 -m sphinx.cmd.build' html
cd _build/html
echo To view RESTInG\'s documentation, including setup instructions, open a web browser and open the following file: `pwd`/index.html
echo or try this URL: file://`pwd`/index.html
