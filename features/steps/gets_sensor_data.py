import os
from behave import given, when, then
import warnings

from sensors import NotEnoughSensors
import server
from tetra_constants import (SENSOR_QUANTITY,
                             ENOUGH_SENSORS,
                             NOT_ENOUGH_SENSORS,
                             NUMBER_OF_PATIENTS)


@given("there is an object that represent the total sensing package")
def step_impl(context):
    os.environ[SENSOR_QUANTITY] = ENOUGH_SENSORS
    context.sensors = server.Sensors()


@when("these sensors are initialized")
def step_impl(context):
    pass


@then("the software will calibrate the sensors")
def step_impl(context):
    # context.sensors.calibrate()
    pass


@then("the software will determine which tubes have both pressure and "
      "airflow sensing")
def step_impl(context):
    number_of_good_tubes = len(context.sensors.tubes_with_enough_sensors())
    assert (number_of_good_tubes == NUMBER_OF_PATIENTS), \
           ("Incorrect number of tubes.  "
            f"{NUMBER_OF_PATIENTS} expected, "
            f"{number_of_good_tubes} received")


@then("the software will return the state of the sensor to the user.")
def step_impl(context):
    datum = context.sensors.poll()
    assert len(datum) == NUMBER_OF_PATIENTS, \
        ("Not the correct number of data.  "
         f"{NUMBER_OF_PATIENTS} expected, {len(datum)} received.")


@given("any tube doesn't have a complete set of working sensors")
def step_impl(context):
    os.environ[SENSOR_QUANTITY] = NOT_ENOUGH_SENSORS


@when("the software diagnostic is run")
def step_impl(context):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        print("bar")
        context.sensors.tubes_with_enough_sensors()
        context.warnings = w


@then("{quantity:d} warning {warning} will be raised")
def step_impl(context, quantity, warning):
    assert len(context.warnings) == quantity, \
        (f"{quantity} warnings expected, {len(context.warnings)} "
         "warnings received.")
    assert issubclass(context.warnings[-1].category, eval(warning)), \
        (f"Recieved warning {context.warnings[-1].category} is not the "
         f"expected warning {warning}")


@given("{sensor} sensor on a tube")
def step_impl(context, sensor):
    pass


@when("data is read")
def step_impl(context):
    pass


@then("the data from {sensor} will be used")
def step_impl(context, sensor):
    pass
