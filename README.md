# Ventilator Splitter Display

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![testing badge](https://github.com/tetrabiodistributed/project-tetra-display/workflows/tests/badge.svg)

A system to take pressure and flow data from sensors on a ventilator splitter, calculate descriptive parameters based on these data like PEEP or Tidal Volume, and display them for medical professionals to monitor.  This is for use against COVID-19.

To set up the display program for tests, first install the dependencies.  You can skip the chromedriver steps if you don't plan on testing.

Linux
```bash
curl -sSL https://get.docker.com | sh
sudo apt install libatlas-base-dev python3-numpy
sudo ./chromedriverinstall.sh
./setup.sh
```

macOS
```bash
brew install chromedriver docker
./setup.sh
```

To run tests, activate the virtual environment and then run the test script.

```bash
. venv/bin/activate
./runtests.sh
deactivate
```

To run the display, run these commands.

```bash
docker build -t zmq_proxy:latest .
docker run --rm -p 8000:8000 zmq_proxy:latest
```

Then open http://localhost:8000 in a browser (Safari and Chrome both work well, Firefox does not).  With this, you'll see a webpage which every second updates a table with the current state of the descriptors for each patient (if this is run off of hardware, the data will be random numbers).  The display ought to look like this.

![display showing inspiratory pressure, tidal volume, PEEP, and PIP for 4 patients](https://cdn.discordapp.com/attachments/610302955521966100/745137321518825523/unknown.png)
