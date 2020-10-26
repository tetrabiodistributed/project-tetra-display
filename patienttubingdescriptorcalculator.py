import random

from numpy_ringbuffer import RingBuffer

from causal_integral_filter import CausalIntegralFilter
from peep_pip import PEEP, PIP


class PatientTubingDescriptorCalculator():

    def __init__(self, current_time):
        self._flow_rate_sample_times = RingBuffer(2)
        self._flow_rate_sample_times.append(current_time)

        self._tidal_volume_filter = CausalIntegralFilter(0, current_time)
        self._peep_filter = PEEP(0.1)
        self._pip_filter = PIP(0.1)
        self._most_recent_pressure = 0.0
        self._most_recent_flow_rate = 0.0

    def add_flow_rate_datum(self, datum, current_time):
        self._tidal_volume_filter.append(datum, current_time)
        self._most_recent_flow_rate = datum

    def add_pressure_datum(self, datum):
        self._peep_filter.append(datum)
        self._pip_filter.append(datum)
        self._most_recent_pressure = datum

    def add_tidal_volume_value(self, tidal_volume):
        self._tidal_volume_filter.append_integral_value(tidal_volume)

    def _PEEP(self):
        return self._peep_filter.get_datum()

    def _PIP(self):
        return self._pip_filter.get_datum()

    def _tidal_volume(self):
        return self._tidal_volume_filter.get_datum()

    @property
    def descriptors(self):
        return {"Inspiratory Pressure": self._most_recent_flow_rate,
                "PEEP": self._PEEP(),
                "PIP": self._PIP(),
                "Tidal Volume": self._tidal_volume(),
                "Flow Rate": self._most_recent_flow_rate}
