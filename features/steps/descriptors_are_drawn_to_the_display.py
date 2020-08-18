from behave import given, when, then
import json
import math

import constants


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
    context.expected_values = {i: {row["key"]: row["value"]
                                   for row in context.table}
                               for i in range(constants.NUMBER_OF_PATIENTS)}
    context.client \
           .containers \
           .get(context.container_name) \
           .exec_run("python3 zmq_test_server "
                     f"{str(json.dumps(context.expected_values))}")


@then("all the values in the display will correspond to that JSON packet")
def step_impl(context):
    context.browser.get("http://localhost:8000")
    classes_and_descriptors = {"dP": "Inspiratory Pressure",
                               "PEEP": "PEEP",
                               "PIP": "PIP",
                               "Tv": "Tidal Volume"}
    for i in range(constants.NUMBER_OF_PATIENTS):
        for class_label, descriptor in classes_and_descriptors.items():
            context.element = (
                context.browser
                   .find_element_by_xpath("//div[@class='_dataCell "
                                          f"patient-{i} "
                                          f"{class_label}']"))
            data_value = float(context.element.text)
            expected_value = float(context.expected_values[i][descriptor])
            assert math.isclose(data_value, expected_value), \
                f"patient-{i} {class_label} is {data_value} when " \
                f"{expected_value} is expected."


@when("I send a JSON packet formatted for this display where the leave "
      "values are all {value:f} except {diff_descriptor} for patient "
      "{patient_number:d} which is {special_value:f}")
def step_impl(context, value, diff_descriptor, patient_number, special_value):
    descriptors = ("Inspiratory Pressure", "PEEP", "PIP", "Tidal Volume")
    context.expected_values = {i: {descriptor: value
                                   for descriptor in descriptors}
                               for i in range(constants.NUMBER_OF_PATIENTS)}
    context.expected_values[patient_number][diff_descriptor] = special_value
    context.client \
           .containers \
           .get(context.container_name) \
           .exec_run("python3 zmq_test_server "
                     f"{str(json.dumps(context.expected_values))}")


@then("{descriptor} for patient {patient_number:d} doesn't overflow")
def step_impl(context, descriptor, patient_number):
    context.browser.get("http://localhost:8000")
    text_element = context.browser.find_element_by_xpath(
        f"//div[@class='_dataCell patient-{patient_number} {descriptor}']")
    client_width = text_element.get_property("clientWidth")
    scroll_width = text_element.get_property("scrollWidth")
    client_height = text_element.get_property("clientHeight")
    scroll_height = text_element.get_property("scrollHeight")
    assert ((client_width >= scroll_width)
            and (client_height >= scroll_height)), \
        (f"patient-{patient_number} {descriptor} is overflowing with "
         f"text {text_element.text}")
