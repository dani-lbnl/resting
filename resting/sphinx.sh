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
cd ..
# Create skeleton Sphinx files for RESTInG documentation
mkdir doc
cd doc
# Creating aliases doesn't seem to work, -x is not recognized on a Mac
$PYTHON -m sphinx.cmd.quickstart -q --extensions=sphinx.ext.napoleon -p 'REST Interface Generator (RESTInG)' -a 'Regents of the University of California' -v ''
# Link in the RESTInG documentation source files
rm index.rst
ln -s ../resting_doc_source/* .
echo -e '\nimport os.path\nimport sys\nsys.path.append(os.path.abspath("..") + "/resting")' >> conf.py
# Use Sphinx to generate site documentation
make SPHINXBUILD="$PYTHON -m sphinx.cmd.build" html
cd _build/html
echo To view RESTInG\'s documentation on a Linux or Mac, including setup instructions, open a web browser and open the following file: `pwd`/index.html
echo or try this URL: file://`pwd`/index.html
USERNAME=`whoami`
echo These will not work when using Cygwin on a Windows computer. Instead, direct a web browser to a file such as "C:\cygwin64\home\$USERNAME\resting\doc\_build\html\index.html", or a corresponding URL such as "file:///C:/cygwin64/home/$USERNAME/resting/doc/_build/html/index.html"
