#!/bin/sh

. ./env.sh

echo "Behaviour Tests:"
${VENV_BINDIR}/behave
echo $'\nUnit Tests:'
${VENV_BINDIR}/python3 -m unittest
