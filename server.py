import sys
import time
import json
import random

import zmq

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator
from sensors import Sensors
import constants


class Calculator():

    def __init__(self):

        self._calculators = (
            tuple(PatientTubingDescriptorCalculator(time.time())
                  for _ in range(constants.NUMBER_OF_PATIENTS)))

    def add_datum(self, datum):
        for i in range(len(self._calculators)):
            self._calculators[i].add_pressure_datum(datum[i][0])
            if len(datum[i]) > 1:
                self._calculators[i].add_flow_rate_datum(datum[i][1],
                                                         time.time())

    def get_datum(self):
        datum = {}
        for i in range(len(self._calculators)):
            datum.update({f"patient-{i}": self._calculators[i].descriptors})
        return datum


class Communicator():

    def __init__(self, port=5000):
        self._socket = zmq.Context().socket(zmq.PUB)
        self._socket.bind(f"tcp://*:{port}")

    def publish_message(self, message):
        self._socket.send_multipart([b"",
                                     json.dumps(message).encode("ascii")])


def main():
    sensors = Sensors()
    sensor_data = sensors.poll()
    calculator = Calculator()
    communicator = Communicator()
    running = True
    while running:
        try:
            start_time = time.time()
            calculator.add_datum(sensor_data)

            communicator.publish_message(calculator.get_datum())
            while (time.time() - start_time < 1.0):
                time.sleep(0.1)
        except:
            running = False
            raise


if "__main__" == __name__:
    main()
