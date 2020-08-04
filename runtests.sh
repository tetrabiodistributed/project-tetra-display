#!/bin/sh

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'

docker ps >/dev/null 2>&1 || {
   printf "${HIGHLIGHT}An error was encountered in running the behave tests.\nThe docker daemon is not running.${NO_COLOR}"
   exit 1
}


echo "Behaviour Tests:"
behave
echo $'\nUnit Tests:'
python3 -m unittest
