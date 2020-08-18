Ventilator Splitter Display
===========================

![testing badge](https://github.com/tetrabiodistributed/project-tetra-display/workflows/tests/badge.svg)

A system to take pressure and flow data from sensors on a ventilator splitter, calculate descriptive parameters based on these data like PEEP or Tidal Volume, and display them for medical professionals to monitor.  This is for use against COVID-19.

To set up the display program for tests, first make sure you have `chromedriver` installed (macOS: `brew install chromedriver`, linux: `sudo apt install chromedriver`).  `chromedriver` makes it possible to validate the display output.  Then run `./setup.sh` to build the virtual environment and then `. venv/bin/activate` to activate the virtual environment.

To do the tests, run `./runtests.sh`.  Running this script will first show the results of the behaviour tests and then the unit tests.  When you're done, you can shut down the venv with `deactivate`.

To run the display, first make sure Docker is installed, then run these commands.

```bash
docker build -t zmq_proxy:latest .
docker run --rm -p 8000:8000 zmq_proxy:latest
```

Then open http://localhost:8000 in a browser.  With this, you'll see a webpage which every second updates a table with the current state of the descriptors for each patient (if this is run off of hardware, the data will be random numbers except for Tidal Volume which will be 0.0).  The display ought to look like this.

![display showing inspiratory pressure, tidal volume, PEEP, and PIP for 4 patients](https://cdn.discordapp.com/attachments/610302955521966100/745137321518825523/unknown.png)
