#!/bin/sh

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'
VENV_NAME=venv

VENV_BINDIR=${VENV_NAME}/bin

if ! [ -f ${VENV_BINDIR}/pip3 ]; then
    python3 -m venv ${VENV_NAME}
fi

${VENV_BINDIR}/pip3 install pip --upgrade
${VENV_BINDIR}/pip3 install -r requirements.txt

if ! command -v docker &> /dev/null; then
    printf "\n${HIGHLIGHT}Please install Docker${NO_COLOR}"
fi
