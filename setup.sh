#!/bin/sh

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'

. ./env.sh
if ! [ -f ${VENV_BINDIR}/pip3 ]; then
    python3 -m venv ${VENV_NAME} || echo "Cannot create virtualenv ${VENV_NAME}" 1>&2
fi

${VENV_BINDIR}/pip3 install pip --upgrade
${VENV_BINDIR}/pip3 install -r requirements.txt

if ! command -v docker &> /dev/null; then
    printf "\n${HIGHLIGHT}Please install Docker${NO_COLOR}"
fi

echo $'\nRun this to start the virtual environment'
printf "${HIGHLIGHT}. venv/bin/activate${NO_COLOR}\n"
