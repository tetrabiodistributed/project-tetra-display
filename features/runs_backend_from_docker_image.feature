@wip
Feature: Runs backend from a Docker image

@slow
Scenario:
    Given A running Docker image on port 8000
    When I listen for packets
    Then there will be a JSON packet sent every 1.0 seconds
    And that JSON packet will have several keys named with 'patient-{0-index}'
    And those keys will refer to the descriptors
