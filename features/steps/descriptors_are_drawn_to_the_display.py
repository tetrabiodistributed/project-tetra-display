from behave import given, when, then
import json

import constants
from basic_websocket import ws_connect_retry


@given("a file named {file} exists in {static_directory}")
def step_impl(context, file, static_directory):
    try:
        with open(static_directory + file):
            pass
    except FileNotFoundError:
        raise


@given("a connection is established to draw to the webpage")
def step_impl(context):
    pass


@when("I send a JSON packet where the top-level keys are "0"-number of "
      "patients and their values are this dictionary")
def step_impl(context):
    context.json = json.dumps({str(i): {row["key"]: row["value"]
                                        for row in context.table}})


@then("all the values in the display will correspond to that JSON packet")
def step_impl(context):
    pass


@when("I send a JSON packet formatted for this display where the leave "
      "values are all {value:f} except {descriptor} for patient "
      "{patient_number:d} which is {special_value:f}")
def step_impl(context, value, descriptor, patient_number, special_value):
    pass
