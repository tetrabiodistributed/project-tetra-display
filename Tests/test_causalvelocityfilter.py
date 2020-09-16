import math
import unittest

import numpy as np

from causal_velocity_filter import CausalVelocityFilter
from filter_rms_error import filter_rms_error


class TestCausalVelocityFilter(unittest.TestCase):

    def testInit_nominal(self):
        velocity_filter = CausalVelocityFilter(0.01)
        self.assertIsNotNone(filter,
                             "Fails to initialize a velocity filter")

    def test_differentiates(self):
        rms_error = filter_rms_error(CausalVelocityFilter,
                                     np.sin,
                                     np.cos,
                                     skip_initial=7)
        self.assertLess(rms_error, 0.01,
                        "Fails to differentiate a data series "
                        "approximating sin(x) within <0.01 rms error")

    def test_rejectsHighFrequency(self):
        def to_filter_data_lambda(t): return np.sin(t) + 0.001*np.sin(100*t)
        rms_error = filter_rms_error(CausalVelocityFilter,
                                     to_filter_data_lambda,
                                     np.cos,
                                     skip_initial=7)
        self.assertLess(rms_error, 0.01,
                        "Fails to differentiate a data series while "
                        "rejecting high-frequency noise within "
                        "<0.01 rms error")
