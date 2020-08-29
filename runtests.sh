#!/bin/sh

. $(dirname "$0")/env.sh

exit_code=0

echo "Behaviour Tests:"
${VENV_BINDIR}/behave
exit_code=$(($exit_code + $?))
echo $'\nUnit Tests:'
${VENV_BINDIR}/python3 -m unittest
exit_code=$(($exit_code + $?))

exit $exit_code
