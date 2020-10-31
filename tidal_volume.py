import math

from causal_integral_filter import CausalIntegralFilter
import constants


class TidalVolume():

    def __init__(self, initial_time):
        self._integral_filter = CausalIntegralFilter(0, initial_time)

    def append(self, flow_rate, t):
        self._integral_filter.append(flow_rate, t)
        if math.isclose(flow_rate, 0, abs_tol=constants.MINIMUM_TIDAL_VOLUME):
            self._integral_filter.append_integral_value(0)

    def get_datum(self):
        return self._integral_filter.get_datum()
