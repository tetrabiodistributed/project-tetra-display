#!/bin/sh

. venv/bin/activate
echo "Behaviour Tests:"
behave
echo $'\nUnit Tests:'
python3 -m unittest
deactivate
