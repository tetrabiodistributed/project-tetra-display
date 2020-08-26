#!/bin/sh

# This is to install chromedriver on a CI/CD machine.  It might work
# for a normal computer, but it might not.  Who knows.
#
# Please `sudo apt-get update` before running this script

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'

echo "${HIGHLIGHT}Installing chromedriver${NO_COLOR}"

sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f
sudo apt-get install xvfb

sudo apt-get install unzip

wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver

exit 0
