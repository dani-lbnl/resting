#!/bin/sh
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
CWD=`pwd`
. start.sh
cd $CWD
. finish.sh
cd $CWD
. run.sh
$PYTHON tests.py
