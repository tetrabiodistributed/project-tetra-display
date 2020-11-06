import unittest

import numpy as np

from patienttubingdescriptorcalculator \
    import PatientTubingDescriptorCalculator


class TestPatientTubingDescriptorCalculator(unittest.TestCase):

    def setUp(self):
        self._calculator = PatientTubingDescriptorCalculator(0)
