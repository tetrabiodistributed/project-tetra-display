import unittest
import math

import numpy as np
from scipy.interpolate import interp1d

from tidal_volume import TidalVolume
from process_sample_data import ProcessSampleData
from filter_rms_error import filter_rms_error


fake_data_error_safety_factor = 8
actual_data_error_safety_factor = 2


class TestTidalVolume(unittest.TestCase):

    def test_sin_greater_than_zero(self):
        def to_filter_data(t):
            return np.maximum(np.sin(t), 0)

        def desired_filter_data(t):
            return np.where(np.sin(t) > 0, np.abs(np.sin(t/2)), 0)

        normalized_error = filter_rms_error(TidalVolume,
                                            to_filter_data,
                                            desired_filter_data)
        self.assertLess(normalized_error, 1/fake_data_error_safety_factor,
                        "Fails to correctly calculate tidal volume of "
                        "sine where the range is clipped to the reals "
                        "greater than 0.")

    def test_approximate_breathing_data(self):
        max_flow_rate = 13.5
        frequency = 3
        length_in_cycles = 10
        number_of_cycles_skipped = 3

        def to_filter_data(t):
            return np.where(
                ((t % (number_of_cycles_skipped * 2*np.pi / frequency))
                 < (2*np.pi / frequency)),
                np.maximum(max_flow_rate * np.sin(frequency * t), 0),
                0)

        def desired_filter_data(t):
            return np.where(
                ((t % (number_of_cycles_skipped * 2*np.pi / frequency))
                 < (2*np.pi / frequency)),
                np.where(np.sin(t) > 0,
                         max_flow_rate * np.abs(np.sin(frequency / 2 * t)),
                         0),
                0)

        normalized_error = filter_rms_error(
            TidalVolume,
            to_filter_data,
            desired_filter_data,
            dt=0.125,
            end_time=2*np.pi * length_in_cycles / frequency)
        self.assertLess(normalized_error, 1/actual_data_error_safety_factor,
                        "Fails to correctly calculate tidal volume of "
                        "data that is sort of similar to actual "
                        "breathing data.")

    def test_actual_breathing_data(self):
        normalized_error = filter_rms_error(TidalVolume,
                                            actual_flow_rates,
                                            actual_tidal_volumes,
                                            dt=actual_data_dt,
                                            start_time=actual_data_start_time,
                                            end_time=actual_data_end_time)
        self.assertLess(normalized_error, 1/actual_data_error_safety_factor,
                        "Fails to correctly calculate tidal volume for "
                        "actual data")


flow_rate_data = None
tidal_volume_data = None
actual_data_start_time = 0.0
actual_data_dt = 0.047
actual_data_end_time = 11.504


def get_breathing_data():
    global flow_rate_data
    global tidal_volume_data
    if flow_rate_data is None or tidal_volume_data is None:
        raw_data = (
            ProcessSampleData("Tests/TestData/20200609T2358Z_patrickData.txt")
        )
        timestamps_in_seconds = [
            t/100 for t in raw_data.relative_timestamps()]
        flow_rate_data = interp1d(
            timestamps_in_seconds,
            raw_data.flow_rates)
        tidal_volume_data = interp1d(
            timestamps_in_seconds,
            raw_data.tidal_volumes)


def actual_flow_rates(t):
    get_breathing_data()
    return flow_rate_data(t)


def actual_tidal_volumes(t):
    get_breathing_data()
    return tidal_volume_data(t)
