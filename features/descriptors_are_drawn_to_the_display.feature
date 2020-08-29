Feature: Discriptors are drawn to the display

    @fixture.browser.chrome
    Scenario: All values read 0.0
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        And A running Docker image on port 8000
        And that docker image is ready to receive test data
        When a data packet is sent where all the leaf values are 0
        Then all the values in the display will correspond to that data packet

    @fixture.browser.chrome
    Scenario: All values read 0.0 except patient 1 PEEP
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        And A running Docker image on port 8000
        And that docker image is ready to receive test data
        When I send a JSON packet formatted for this display where the leave values are all 0.0 except PEEP for patient 1 which is 1.0
        Then all the values in the display will correspond to that data packet

    @fixture.browser.chrome
    Scenario: One of the data values is a big number
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        And A running Docker image on port 8000
        And that docker image is ready to receive test data
        When I send a JSON packet formatted for this display where the leave values are all 0.0 except PEEP for patient 1 which is 888.88
        Then PEEP for patient 1 doesn't overflow
