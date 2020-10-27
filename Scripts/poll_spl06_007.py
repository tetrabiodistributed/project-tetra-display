import time

from spl06_007 import PressureSensor, Calibrator, Communicator
from tca9548a import I2CMux
import constants


if "__main__" == __name__:
    print("--Initialization")
    mux = I2CMux(constants.PRESSURE_SENSOR_MUX_ADDRESS)
    mux.select_channel(0)
    comms = Communicator(dump_communication=False)
    print("--Set Op Mode")
    comms.set_op_mode(PressureSensor.OpMode.command)
    print("--Set Pressure Sampling")
    comms.set_pressure_sampling()
    print("--Set Temperature Sampling")
    comms.set_temperature_sampling()

    calibrator = Calibrator(comms.calibration_coefficients,
                            comms.pressure_scale_factor,
                            comms.temperature_scale_factor)

    try:
        while True:
            print("--Get Pressure")
            raw_pressure = comms.raw_pressure()
            print("--Get Temperature")
            raw_temperature = comms.raw_temperature()
            pressure = calibrator.pressure(raw_pressure, raw_temperature)
            temperature = calibrator.temperature(raw_temperature)
            print(f"Time:\t\t{time.time()*1000}\n"
                  f"Pressure:\t{pressure}\n"
                  f"Temperature:\t{temperature}")
            time.sleep(1.0)
    finally:
        mux.close()
        comms.close()
