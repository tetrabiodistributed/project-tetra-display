Feature: Calculating tubing descriptors

    Scenario: Calculating descriptors
        Given there are sensors connected
        And there is a calculator to parse sensor data
        When data is requested from the sensors
        Then the sensors yield all of the descriptors
