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
ENGINE=`$PYTHON -c 'from project import engine
print(engine)'`
if [[ ${MACHTYPE%cygwin} = $MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
${SUDOPREFIX}${ENGINE} container rm ws
