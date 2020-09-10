import unittest
import math

import numpy as np
from scipy.interpolate import interp1d

from peep_pip import PEEP, PIP
from filter_rms_error import filter_rms_error
from process_sample_data import ProcessSampleData


class TestPEEP(unittest.TestCase):

    def test_sin_input(self):
        def desired_filter_data(t): return -np.ones(len(t))
        rms_error = filter_rms_error(PEEP,
                                     np.sin,
                                     desired_filter_data)
        self.assertLess(rms_error, 0.01,
                        "Fails to correctly calculate the PEEP of a "
                        "sine.")

    def test_cos_input(self):
        def desired_filter_data(t): return -np.ones(len(t))
        rms_error = filter_rms_error(PEEP,
                                     np.cos,
                                     desired_filter_data)
        self.assertLess(rms_error, 0.01,
                        "Fails to correctly calculate the PEEP of a "
                        "cosine.")

    def test_sin_greater_than_zero(self):
        def to_filter_data(t):
            return np.array([max(0, datum) for datum in np.sin(t)])

        def desired_filter_data(t): return np.zeros(len(t))
        rms_error = filter_rms_error(PEEP,
                                     to_filter_data,
                                     desired_filter_data)
        self.assertLess(rms_error, 0.01,
                        "Fails to correctly calculate the PEEP of a "
                        "sine where the range is clipped to the reals "
                        "greater than 0.")

    def test_approximate_breathing_data(self):
        def to_filter_data(t):
            if (t % (3*20*math.pi/3/10)) < (20*math.pi/3/10):
                # finds every 4th peak of sin(3t)
                breathing_active = True
            else:
                breathing_active = False
            return (max(20*np.sin(3*t), 0) * 1 if breathing_active else 0) + 4

        def desired_filter_data(t): return np.zeros(len(t))
        rms_error = filter_rms_error(PEEP,
                                     to_filter_data,
                                     desired_filter_data,
                                     dt=0.125,
                                     end_time=20*math.pi/3)
        self.assertLess(rms_error, 0.01,
                        "Fails to calculate PEEP for data that is sort "
                        "of similar to actual breathing data.")

    def test_actual_breathing_data(self):
        rms_error = filter_rms_error(PEEP,
                                     actual_breathing_data,
                                     actual_PEEP_data,
                                     dt=actual_data_dt,
                                     start_time=actual_data_start_time,
                                     end_time=actual_data_end_time)
        self.assertLess(rms_error, 0.01,
                        "Fails to correctly calculate PEEP for actual "
                        "data.")


breathing_data = None
pip_data = None
peep_data = None
actual_data_start_time = 0.0
actual_data_dt = 0.047
actual_data_end_time = 11.504


def get_breathing_data():
    global breathing_data
    if breathing_data is None:
        raw_data = (
            ProcessSampleData("Tests/TestData/20200609T2358Z_patrickData.txt")
        )
        timestamps = raw_data.relative_timestamps()
        pressures = raw_data.pressures
        nonrepeat_timestamp_indices = []
        for i in range(len(timestamps)):
            if (timestamps[i] - timestamps[i-1] > 1):
                nonrepeat_timestamp_indices.append(i)
        breathing_data = interp1d(
            (timestamps[i]/1000 for i in nonrepeat_timestamp_indices),
            (pressures[i] for i in nonrepeat_timestamp_indices))

    return breathing_data


def get_PIP_data():
    global pip_data
    if pip_data is None:
        # PIP data hand-fitted to the pressure waveform
        raw_data = [(0, 8.22), (3.616, 8.22), (3.69, 8.22),
                    (3.91, 7.79), (4.02, 7.71), (9.00, 7.71),
                    (9.06, 7.74), (11.504, 7.74)]
        timestamps = raw_data[:][0]
        pressures = raw_data[:][1]
        breathing_data = interp1d(timestamps, pressures)


def get_PEEP_data():
    global peep_data
    if peep_data is None:
        # PEEP data hand-fitted to the pressure waveform
        raw_data = [(0, 20), (1.44, 20), (1.47, 20.80),
                    (1.54, 22.4), (1.65, 23.7), (1.74, 24.2),
                    (6.7, 24.2), (6.81, 24.3), (11.504, 24.3)]
        timestamps = raw_data[:][0]
        pressures = raw_data[:][1]
        breathing_data = interp1d(timestamps, pressures)


def actual_breathing_data(t):
    """Returns an actual breathing pressure waveform in [cmH2O] as a
    function of time in [s].
    """
    return get_breathing_data()(t)


def actual_PIP_data(t):
    return get_PIP_data()(t)


def actual_PEEP_data(t):
    return get_PEEP_data()(t)
