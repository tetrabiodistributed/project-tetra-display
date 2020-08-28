#!/bin/sh

# This is to install chromedriver on a CI/CD machine.  It might work
# for a normal computer, but it might not.  Who knows.
#
# Please `sudo apt-get update` before running this script

HIGHLIGHT='\033[0;33m'
NO_COLOR='\033[0m'

echo "${HIGHLIGHT}Installing chromedriver${NO_COLOR}"

set -xe \
  && curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable \
  && rm -rf /var/lib/apt/lists/* \
  && CD_VER=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(google-chrome --version | awk '{print $3}' | sed -r 's/\.[0-9]*$//'))
  && wget https://chromedriver.storage.googleapis.com/$cd_ver/chromedriver_linux64.zip \
  && unzip chromedriver_linux64.zip \
  && mv /chromedriver /usr/bin/; \

exit 0
