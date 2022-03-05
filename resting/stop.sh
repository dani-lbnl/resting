#!/bin/bash
if [[ ${MACHTYPE%cygwin} = $MACHTYPE ]]
then
    SUDOPREFIX='sudo '
else
    SUDOPREFIX=''
fi
${SUDOPREFIX}./stop_db.sh
${SUDOPREFIX}./stop_ws.sh
