from behave import given, when, then
import math
import json
import time

from basic_websocket import ws_connect_retry
from tetra_constants import NUMBER_OF_PATIENTS, DESCRIPTORS


@given("A running Docker image on port {port}")
def step_impl(context, port):
    context.port = port
    context.client.containers.run(context.container_tag,
                                  name=context.container_name,
                                  detach=True,
                                  auto_remove=True,
                                  ports={f"{context.port}": context.port})
    time.sleep(2.0)  # give the container a moment to start up.
    # Has a bad code smell, but it takes a second or two for things to start.
    # Even so, further listening is done in the "I listen for packets" step to
    # make sure we have good timing once everything's running


@when("I listen for packets")
def step_impl(context):
    uri = f"ws://localhost:{context.port}/ws"
    context.ws = ws_connect_retry(uri)
    context.first_message = context.ws.recv()  # triggers waiting for the first
    # message to appear, rather than sleeping for it


@then("there will be a JSON packet sent every {t:f} seconds")
def step_impl(context, t):
    number_of_messages = 5
    start_time = time.time()
    print(start_time)  # leaving in print statements for later debugging if necessary
    for _ in range(number_of_messages):
        context.message = context.ws.recv()
        print(context.message, time.time())
    end_time = time.time()
    print(end_time)
    context.json = json.loads(context.message)
    context.client.containers.get(context.container_name).kill()
    print ((end_time-start_time)/number_of_messages)
    assert math.isclose((end_time - start_time)/number_of_messages, t,
                        rel_tol=0.15), \
        "Fails to send packets at 1 Hz"


@then("that JSON packet will have several keys named with "
      "'patient-{0-index}'")
def step_impl(context):
    for i in range(NUMBER_OF_PATIENTS):
        assert f"patient-{i}" in context.json, \
            ("JSON packet doesn't have top-level keys formatted as "
             "expected.")


@then("those keys will refer to the descriptors")
def step_impl(context):
    assert all(descriptor in context.json[f"patient-{i}"]
               for i in range(NUMBER_OF_PATIENTS)
               for descriptor in DESCRIPTORS), \
        "Patient descriptors aren't formatted as expected."
