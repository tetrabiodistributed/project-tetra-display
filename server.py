import time
import json

import zmq

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator
from sensors import Sensors
from tetra_constants import NUMBER_OF_PATIENTS


class Calculator():

    def __init__(self):

        self._calculators = (
            tuple(PatientTubingDescriptorCalculator(time.time())
                  for _ in range(NUMBER_OF_PATIENTS)))

    def add_datum(self, datum):
        for i in range(len(self._calculators)):
            self._calculators[i].add_pressure_datum(datum[i][0])
            if len(datum[i]) > 1:
                self._calculators[i].add_flow_rate_datum(datum[i][1],
                                                         time.time())

    def get_datum(self):
        return {f"patient-{i}": self._calculators[i].descriptors
                for i in range(len(self._calculators))}


class Communicator():

    def __init__(self, port=5000):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.bind(f"tcp://*:{port}")
        self._closed = False

    def close(self):
        if not self._closed:
            self._socket.close()
            self._context.term()
            self._closed = True

    def close(self):
        self._socket.close()
        self._context.term()

    def publish_message(self, message):
        self._socket.send_multipart([b"",
                                     json.dumps(message).encode("ascii")])


def main():
    sensors = Sensors()
    calculator = Calculator()
    communicator = Communicator()
    try:
        while True:
            start_time = time.time()
            data = sensors.poll()
            calculator.add_datum(data)
            datum = calculator.get_datum()
            communicator.publish_message(datum)
            while (time.time() - start_time < 1.0):
                time.sleep(0.1)
        except KeyboardInterrupt:
            running = False
            sensors.close()
            communicator.close()


if "__main__" == __name__:
    main()
