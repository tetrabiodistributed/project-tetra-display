import os
from abc import ABC, abstractmethod
import warnings

from spl06_007 import PressureSensor
from sfm3300d import FlowSensor
from tca9548a import I2CMux
from process_sample_data import ProcessSampleData
from rpi_check import is_on_raspberry_pi
from tetra_constants import (NUMBER_OF_PATIENTS,
                             PRESSURE_SENSOR,
                             NUMBER_OF_PRESSURE_SENSORS,
                             PRESSURE_SENSOR_MUX_ADDRESS,
                             PRESSURE_OVERSAMPLING,
                             PRESSURE_SAMPLING_RATE,
                             CALIBRATION_PRESSURE_SENSOR_INDEX,
                             TEMPERATURE_OVERSAMPLING,
                             TEMPERATURE_SAMPLING_RATE,
                             FLOW_SENSOR_MUX_ADDRESS,
                             SENSIRION_SENSOR,
                             MASS_AIRFLOW_SENSOR,
                             NUMBER_OF_SENSIRION_SENSORS,
                             NUMBER_OF_MASS_AIRFLOW_SENSORS,
                             SENSOR_QUANTITY,
                             MAX_SENSOR_COUNT,
                             NOT_ENOUGH_SENSORS,
                             TOO_MANY_SENSORS)


class SensorsABC(ABC):
    """A class to collect data from the sensing suit for the Tetra
    Ventillator Splitter.  If this class is not used on a Raspberry Pi,
    Then it will return data recorded from the sensors.
    """

    @abstractmethod
    def __init__(self, dump_communication=False):
        """Initializes self."""
        super().__init__()

    @abstractmethod
    def close(self):
        """Closes ever sensor in the system."""
        pass

    @abstractmethod
    def connected_sensors(self):
        """Returns a tuple of all the sensors connected to the system.

        Returns
        -------
        sensors : tuple
            A tuple of tuples of strings, where a string can be
            "SPL06-007" (representing the pressure sensor), "SFM3300-D"
            (representing the Sensirion sensor), or "Mass Air Flow"
            (representing the automotive sensor).  sensors[i] gives
            a tuple of all the sensors connected to port i of the 
            splitter.  sensors[tetra_constants.NUMBER_OF_PATIENTS + 1] will
            give the sensors connected for calibration of the whole
            system.  The output will look something like this:
                (("SPLO6-007", "SFM3300-D"), ("SPL06-007", "SFM3300-D"),
                 ("SPLO6-007", "SFM3300-D"), ("SPLO6-007", "SFM3300-D"),
                 ("SPLO6-007"))
        """
        pass

    @abstractmethod
    def tubes_with_enough_sensors(self):
        """Returns a list of the ports with both a pressure sensor and
        a flow sensor.

        Returns
        -------
        port_list : list
            A list of ints in range(tetra_constants.NUMBER_OF_PATIENTS)
            representing ports that have enough sensors.
        """


if is_on_raspberry_pi():

    class Sensors(SensorsABC):

        def __init__(self, dump_communication=False):
            self._pressure_mux = I2CMux(
                PRESSURE_SENSOR_MUX_ADDRESS,
                dump_communication=dump_communication)
            self._pressure_sensors = []
            for i in range(NUMBER_OF_PRESSURE_SENSORS):
                self._pressure_mux.select_channel(i)
                self._pressure_sensors.append(
                    PressureSensor(dump_communication=dump_communication))
                self._pressure_sensors[i].set_sampling(
                    pressure_oversample=PRESSURE_OVERSAMPLING,
                    pressure_sampling_rate=PRESSURE_SAMPLING_RATE,
                    temperature_oversample=TEMPERATURE_OVERSAMPLING,
                    temperature_sampling_rate=TEMPERATURE_SAMPLING_RATE
                )
                self._pressure_sensors[i].set_op_mode(
                    PressureSensor.OpMode.command)

            self._flow_mux = I2CMux(FLOW_SENSOR_MUX_ADDRESS,
                                    dump_communication=dump_communication)
            self._flow_sensors = []
            for i in range(NUMBER_OF_SENSIRION_SENSORS):
                self._flow_mux.select_channel(i)
                self._flow_sensors.append(
                    FlowSensor(dump_communication=dump_communication))

            self._mass_airflow_sensors = []
            for i in range(NUMBER_OF_MASS_AIRFLOW_SENSORS):
                pass

        def close(self):
            for i in range(NUMBER_OF_PRESSURE_SENSORS):
                self._pressure_mux.select_channel(i)
                self._pressure_sensors[i].close()
            for i in range(NUMBER_OF_SENSIRION_SENSORS):
                self._flow_mux.select_channel(i)
                self._flow_sensors[i].close()
            for mass_airflow_sensor in self._mass_airflow_sensors:
                pass
            self._pressure_mux.close()
            self._flow_mux.close()

        def connected_sensors(self):
            def sensors_available_on_port(i):
                port_i = []
                self._pressure_mux.select_channel(i)
                if self._pressure_sensors[i].is_present():
                    port_i.append(PRESSURE_SENSOR)
                if i < NUMBER_OF_SENSIRION_SENSORS:
                    self._flow_mux.select_channel(i)
                    if self._flow_sensors[i].is_present():
                        port_i.append(SENSIRION_SENSOR)
                return tuple(port_i)

            return tuple(sensors_available_on_port(i)
                         for i in range(MAX_SENSOR_COUNT))

        def tubes_with_enough_sensors(self):
            tubes = []
            sensors = self.connected_sensors()
            for i in range(len(sensors)):
                if (PRESSURE_SENSOR in sensors[i]
                        and (SENSIRION_SENSOR in sensors[i]
                             or MASS_AIRFLOW_SENSOR in sensors[i])):
                    tubes.append(i)
            if len(tubes) != NUMBER_OF_PATIENTS:
                warnings.warn("Not all tubes have a flow and a "
                              "pressure sensor.",
                              NotEnoughSensors)
            return tubes

        def calibration_pressure_sensor_connected(self):
            if (PRESSURE_SENSOR
                in self.connected_sensors()[
                    CALIBRATION_PRESSURE_SENSOR_INDEX]):
                return True
            else:
                return False

        def poll(self):
            sensors = self.connected_sensors()

            def sensor_data_on_port(i):
                data = []
                if PRESSURE_SENSOR in sensors[i]:
                    data.append(self._pressure_sensors[i].pressure())
                if SENSIRION_SENSOR in sensors[i]:
                    data.append(self._flow_sensors[i].flow())
                if MASS_AIRFLOW_SENSOR in sensors[i]:
                    pass
                return data

            return tuple(sensor_data_on_port(i)
                         for i in range(MAX_SENSOR_COUNT))


else:

    class Sensors(SensorsABC):

        def __init__(self, dump_communication=False):
            self._fake_data = (
                ProcessSampleData("Tests/TestData/"
                                  "20200609T2358Z_patrickData.txt"))
            self._data_index = 0

        def close(self):
            pass

        def connected_sensors(self):
            try:
                if (os.environ[SENSOR_QUANTITY] == NOT_ENOUGH_SENSORS):
                    return tuple(
                        [(PRESSURE_SENSOR,)]
                        + [(PRESSURE_SENSOR, SENSIRION_SENSOR)
                           for _ in range(NUMBER_OF_PATIENTS-1)])

                elif (os.environ[SENSOR_QUANTITY] == TOO_MANY_SENSORS):
                    return tuple(
                        [(PRESSURE_SENSOR,
                          SENSIRION_SENSOR,
                          MASS_AIRFLOW_SENSOR)]
                        + [(PRESSURE_SENSOR, SENSIRION_SENSOR)
                           for _ in range(NUMBER_OF_PATIENTS-1)])
            except KeyError:
                pass
            return tuple((PRESSURE_SENSOR, SENSIRION_SENSOR)
                         for _ in range(NUMBER_OF_PATIENTS))

        def tubes_with_enough_sensors(self):
            tubes = []
            sensors = self.connected_sensors()
            for i in range(NUMBER_OF_PATIENTS):
                if (PRESSURE_SENSOR in sensors[i]
                        and (SENSIRION_SENSOR in sensors[i]
                             or MASS_AIRFLOW_SENSOR in sensors[i])):
                    tubes.append(i)
            if len(tubes) != NUMBER_OF_PATIENTS:
                warnings.warn("Not all tubes have a flow and a "
                              "pressure sensor.",
                              NotEnoughSensors)
            return tubes

        def calibration_pressure_sensor_connected(self, fail=False):
            if fail:
                return False
            else:
                return True

        def poll(self):
            """Pulls data from the pressure and flow sensors"""
            datum = tuple((self._fake_data.pressures[self._data_index],
                           self._fake_data.flow_rates[self._data_index])
                          for _ in range(NUMBER_OF_PATIENTS))
            self._data_index += 1
            return datum


class NotEnoughSensors(Warning):
    pass
