from behave import given, when, then

import server
from tetra_constants import DESCRIPTORS, NUMBER_OF_PATIENTS


@given("there are sensors connected")
def step_impl(context):
    context.sensors = server.Sensors()


@given("there is a calculator to parse sensor data")
def step_impl(context):
    context.calculator = server.Calculator()


@when("data is requested from the sensors")
def step_impl(context):
    context.sensor_data = context.sensors.poll()


@then("the sensors yield all of the descriptors")
def step_impl(context):
    context.calculator.add_datum(context.sensor_data)
    assert all(descriptor
               in context.calculator.get_datum()[f"patient-{patient_number}"]
               for descriptor in DESCRIPTORS
               for patient_number in range(NUMBER_OF_PATIENTS))
