Feature: Discriptors are drawn to the display

    Scenario: All value read 0.0
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        When I send a JSON packet where the leaf values are all 0.0
        Then all the values in the display will correspond to that JSON packet

    Scenario: All values read 0.0 except patient 1 PEEP
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        When I send a JSON packet where the leave values are all 0.0 except PEEP for patient 1 which is 1.0
        Then all the values in the display will correspond to that JSON packet
