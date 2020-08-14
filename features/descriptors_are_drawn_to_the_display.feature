@wip
Feature: Discriptors are drawn to the display

    Scenario: All value read 0.0
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        And A running Docker image on port 8000
        When I send a JSON packet where the top-level keys are "0"-number of patients and their values are this dictionary
            | key                  | value |
            | Inspiratory Pressure | 0     |
            | Tidal Volume         | 0     |
            | PEEP                 | 0     |
            | Peak Pressure        | 0     |
            | Flow Rate            | 0     |
        Then all the values in the display will correspond to that JSON packet

    Scenario: All values read 0.0 except patient 1 PEEP
        Given a file named index.html exists in static/
        And a file named style.css exists in static/
        And A running Docker image on port 8000
        When I send a JSON packet formatted for this display where the leave values are all 0.0 except PEEP for patient 1 which is 1.0
        Then all the values in the display will correspond to that JSON packet
