from behave import given, when, then
import json
import os

import selenium
import docker

import constants
import server
from basic_websocket import ws_connect_retry


@given("a file named {file} exists in {static_directory}")
def step_impl(context, file, static_directory):
    try:
        with open(static_directory + file):
            pass
    except FileNotFoundError:
        raise Exception(f"{file} doesn't exist in {static_directory}")


@given("that docker image is ready to receive test data")
def step_impl(context):
    context.client \
           .containers \
           .get(context.container_name) \
           .exec_run("supervisorctl stop publish_server")


@when("I send a JSON packet where the top-level keys are '0'-number of "
      "patients and their values are this dictionary")
def step_impl(context):
    context.json = json.dumps({str(i): {row["key"]: row["value"]
                                        for row in context.table}
                               for i in range(constants.NUMBER_OF_PATIENTS)})
    context.client \
           .containers \
           .get(context.container_name) \
           .exec_run(f"python3 zmq_test_server {str(context.json)}")


@then("all the values in the display will correspond to that JSON packet")
def step_impl(context):
    pass


@when("I send a JSON packet formatted for this display where the leave "
      "values are all {value:f} except {descriptor} for patient "
      "{patient_number:d} which is {special_value:f}")
def step_impl(context, value, descriptor, patient_number, special_value):
    pass
