#!/bin/sh

. venv/bin/activate
echo "Behaviour Tests:"
behave
behave_exit_code=$?
echo $'\nUnit Tests:'
python3 -m unittest
unittest_exit_code=$?
deactivate

if [ $behave_exit_code -ne 0 ]; then
    echo "behave tests failed!"
fi
if [ $unittest_exit_code -ne 0 ]; then
    echo "unittests tests failed!"
fi
exit $(($behave_exit_code + $unittest_exit_code))
