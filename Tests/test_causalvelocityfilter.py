import math
import unittest

import numpy as np

from causal_velocity_filter import CausalVelocityFilter


class TestCausalVelocityFilter(unittest.TestCase):

    def testInit_nominal(self):
        velocity_filter = CausalVelocityFilter(0.01)
        self.assertIsNotNone(filter,
                             "Fails to initialize a velocity filter")

    def test_differentiates(self):
        dt = 0.01
        t = np.arange(0, 10, dt)
        velocity_filter = CausalVelocityFilter(dt)
        to_filter_data = np.sin(t)
        filtered_data = np.array([])
        desired_filtered_data = np.cos(t)
        error = np.array([])
        for i in range(len(to_filter_data)):
            velocity_filter.append(to_filter_data[i])
            filtered_data = np.append(
                filtered_data, velocity_filter.get_datum())
            error = np.append(
                error, desired_filtered_data[i] - filtered_data[i])
        rms_error = np.sqrt(np.mean(error[7:]**2))
        self.assertLess(rms_error, 0.01,
                        "Fails to differentiate a data series "
                        "approximating sin(x) within <0.01 rms error")

    def test_rejectsHighFrequency(self):
        dt = 0.01
        t = np.arange(0, 10, dt)
        velocity_filter = CausalVelocityFilter(dt)
        to_filter_data = np.sin(t) + 0.001*np.sin(100*t)
        filtered_data = np.array([])
        desired_filtered_data = np.cos(np.arange(0, 10, dt))
        error = np.array([])
        for i in range(len(to_filter_data)):
            velocity_filter.append(to_filter_data[i])
            filtered_data = np.append(
                filtered_data, velocity_filter.get_datum())
            error = np.append(
                error, desired_filtered_data[i] - filtered_data[i])
        rms_error = np.sqrt(np.mean(error[7:]**2))
        self.assertLess(rms_error, 0.01,
                        "Fails to differentiate a data series while "
                        "rejecting high-frequency noise within "
                        "<0.01 rms error")
