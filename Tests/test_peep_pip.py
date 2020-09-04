import unittest
import math

import numpy as np

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
        actual_data = actual_breathing_data()

        t = np.array([datum[0] for datum in actual_data])
        test_filter = PEEP(0.047)
        to_filter_data = np.array([datum[1] for datum in actual_data])
        filtered_data = np.array([])
        desired_filtered_data = desired_filter_data_lambda(t)
        error = np.array([])
        for i in range(len(to_filter_data)):
            test_filter.append(to_filter_data[i])
            filtered_data = np.append(filtered_data,
                                      test_filter.get_datum())
            error = np.append(error,
                              desired_filtered_data[i] - filtered_data[i])
        rms_error = np.sqrt(np.mean(error**2))
        self.assertLess(rms_error, 0.01,
                        "Fails to correctly calculate PEEP for actual "
                        "data.")


def actual_breathing_data():
    raw_data = (
        ProcessSampleData("Tests/TestData/20200609T2358Z_patrickData.txt"))
    timestamps = raw_data.relative_timestamps()
    pressures = raw_data.pressures
    nonrepeat_timestamp_indices = []
    for i in range(len(timestamps)):
        if (timestamps[i] - timestamps[i-1] > 1):
            nonrepeat_timestamp_indices.append(i)
    return [(timestamps[i]/1000, pressures[i])
            for i in nonrepeat_timestamp_indices]
