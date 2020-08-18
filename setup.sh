#!/bin/sh

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'

. $(dirname "$0")/env.sh
if ! [ -f ${VENV_BINDIR}/pip3 ]; then
    python3 -m venv ${VENV_NAME} || echo "Cannot create virtualenv ${VENV_NAME}" 1>&2
fi

${VENV_BINDIR}/pip3 install pip --upgrade
${VENV_BINDIR}/pip3 install -r requirements.txt

exit_value=0

if docker -v > /dev/null 2>&1; then
    :
else
    echo "${HIGHLIGHT}Please install docker${NO_COLOR}"
    exit_value=$(($exit_value+1))
fi

if chromedriver -v > /dev/null 2>&1; then
    :
else
    echo "${HIGHLIGHT}Please install chromedriver${NO_COLOR}"
    exit_value=$((exit_value+1))
fi

if [ $exit_value -eq 0 ]; then
    printf "\nRun this to start the venv:\n${HIGHLIGHT}. venv/bin/activate${NO_COLOR}\n"
fi

exit $exit_value
