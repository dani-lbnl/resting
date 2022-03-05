#!/bin/bash
if [[ ${MACHTYPE%cygwin} = $MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
${SUDOPREFIX}docker container rm db ws
