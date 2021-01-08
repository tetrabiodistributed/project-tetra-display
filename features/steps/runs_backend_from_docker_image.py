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
    time.sleep(1.2)  # give the container a moment to start up


@when("I listen for packets")
def step_impl(context):
    uri = f"ws://localhost:{context.port}/ws"
    context.ws = ws_connect_retry(uri)


@then("there will be a JSON packet sent every {t:f} seconds")
def step_impl(context, t):
    number_of_messages = 5
    start_time = time.time()
    for _ in range(number_of_messages):
        context.message = context.ws.recv()
    end_time = time.time()
    context.json = json.loads(context.message)
    context.client.containers.get(context.container_name).kill()
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
