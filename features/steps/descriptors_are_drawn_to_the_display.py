from behave import given, when, then


@given("a file named {file} exists in {static_directory}")
def step_impl(context, file, static_directory):
    with open(static_directory + file):
        pass


@when("I send a JSON packet where the leaf values are all {value:f}")
def step_impl(context, value):
    pass


@then("all the values in the display will correspond to that JSON packet")
def step_impl(context):
    pass


@when("I send a JSON packet where the leave values are all {value:f} "
      "except {descriptor} for patient {patient_number:d} which is"
      "{special_value:f}")
def step_impl(context, value, descriptor, patient_number, special_value):
    pass
