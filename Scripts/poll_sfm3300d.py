import time

from tca9548a import I2CMux
from sfm3300d import FlowSensor
import constants


if "__main__" == __name__:
    mux = I2CMux(constants.FLOW_SENSOR_MUX_ADDRESS)
    mux.select_channel(1)
    sensor = FlowSensor(dump_communication=False)

    running = True
    while running:
        try:
            print(f"{time.time()}\t{sensor.flow()}")
            time.sleep(1.0)
        except KeyboardInterrupt:
            running = False
            sensor.close()
            mux.close()
