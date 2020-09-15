import unittest
import math

import numpy as np
from scipy.interpolate import interp1d

from peep_pip import PEEP, PIP
from filter_rms_error import filter_rms_error
from process_sample_data import ProcessSampleData


# How many times less than the maximum tolerance allowed per
# ISO 80601-2-80:2018 201.12.4.101.1 I would like the filter to be
# accurate to.  Fake data has a higher bar because there's very little
# noise.
fake_data_safety_factor = 8
actual_data_safety_factor = 2


class TestPEEP(unittest.TestCase):

    def test_sin_input(self):
        class PEEPTester(PEEP):
            def __init__(self, dt):
                # maximum_peep == actual PEEP + margin
                super().__init__(dt, maximum_peep=-0.9)

        def desired_filter_data(t):
            return np.full_like(t, -1)
        normalized_error = filter_rms_error(PEEPTester,
                                            np.sin,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PEEP of a "
                        "sine.")

    def test_cos_input(self):
        class PEEPTester(PEEP):
            def __init__(self, dt):
                # maximum_peep == actual PEEP + margin
                super().__init__(dt, maximum_peep=-0.9)

        def desired_filter_data(t): return np.full_like(t, -1)
        normalized_error = filter_rms_error(PEEPTester,
                                            np.cos,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PEEP of a "
                        "cosine.")

    def test_sin_greater_than_zero(self):
        class PEEPTester(PEEP):
            def __init__(self, dt):
                # maximum_peep == actual PEEP + margin
                super().__init__(dt, maximum_peep=0.1)

        def to_filter_data(t):
            return np.maximum(np.sin(t), 0)

        def desired_filter_data(t): return np.zeros_like(t)
        normalized_error = filter_rms_error(PEEPTester,
                                            to_filter_data,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PEEP of a "
                        "sine where the range is clipped to the reals "
                        "greater than 0.")

    def test_approximate_breathing_data(self):
        peep = 4
        pip = 20
        frequency = 3
        length_in_cycles = 10

        def to_filter_data(t):
            # An idealized version of a breathing waveform
            # https://cdn.discordapp.com/attachments/610302955521966100/755223255836524624/unknown.png
            number_of_cycles_skipped = 3
            return np.where(
                ((t % (number_of_cycles_skipped * 2*np.pi / frequency))
                 < (2*np.pi / frequency)),
                np.maximum((pip - peep) * np.sin(frequency * t), 0) + peep,
                peep)

        def desired_filter_data(t): return np.full_like(t, peep)
        normalized_error = filter_rms_error(
            PEEP,
            to_filter_data,
            desired_filter_data,
            dt=0.125,
            end_time=2*np.pi * length_in_cycles / frequency,
            skip_initial=7,
            use_pressure_error=True)
        self.assertLess(normalized_error, 1/actual_data_safety_factor,
                        "Fails to calculate PEEP for data that is sort "
                        "of similar to actual breathing data.")

    def test_actual_breathing_data(self):
        normalized_error = filter_rms_error(PEEP,
                                            actual_breathing_data,
                                            actual_PEEP_data,
                                            dt=actual_data_dt,
                                            start_time=actual_data_start_time,
                                            end_time=actual_data_end_time,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/actual_data_safety_factor,
                        "Fails to correctly calculate PEEP for actual "
                        "data.")


class TestPIP(unittest.TestCase):

    def test_sin_input(self):
        class PIPTester(PIP):
            def __init__(self, dt):
                # minimum_pip == actual PIP - margin
                super().__init__(dt, minimum_pip=0.9)

        def desired_filter_data(t): return np.ones_like(t)
        normalized_error = filter_rms_error(PIPTester,
                                            np.sin,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PIP of a "
                        "sine.")

    def test_cos_input(self):
        class PIPTester(PIP):
            def __init__(self, dt):
                # minimum_pip == actual PIP - margin
                super().__init__(dt, minimum_pip=0.9)

        def desired_filter_data(t): return np.ones_like(t)
        normalized_error = filter_rms_error(PIPTester,
                                            np.cos,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PIP of a "
                        "cosine.")

    def test_sin_greater_than_zero(self):
        class PIPTester(PIP):
            def __init__(self, dt):
                # minimum_pip == actual PIP - margin
                super().__init__(dt, minimum_pip=0.9)

        def to_filter_data(t):
            return np.maximum(np.sin(t), 0)

        def desired_filter_data(t): return np.ones_like(t)
        normalized_error = filter_rms_error(PIPTester,
                                            to_filter_data,
                                            desired_filter_data,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/fake_data_safety_factor,
                        "Fails to correctly calculate the PIP of a "
                        "sine where the range is clipped to the reals "
                        "greater than 0.")

    def test_approximate_breathing_data(self):
        peep = 4
        pip = 20
        frequency = 3
        length_in_cycles = 10

        def to_filter_data(t):
            # An idealized version of a breathing waveform
            # https://cdn.discordapp.com/attachments/610302955521966100/755223255836524624/unknown.png
            number_of_cycles_skipped = 3
            return np.where(
                ((t % (number_of_cycles_skipped * 2*np.pi / frequency))
                 < (2*np.pi / frequency)),
                np.maximum((pip - peep) * np.sin(frequency * t), 0) + peep,
                peep)

        def desired_filter_data(t): return np.full_like(t, pip)
        normalized_error = filter_rms_error(
            PIP,
            to_filter_data,
            desired_filter_data,
            dt=0.125,
            end_time=2*math.pi * length_in_cycles / frequency,
            skip_initial=7,
            use_pressure_error=True)
        self.assertLess(normalized_error, 1/actual_data_safety_factor,
                        "Fails to calculate PIP for data that is sort "
                        "of similar to actual breathing data.")

    def test_actual_breathing_data(self):
        normalized_error = filter_rms_error(PIP,
                                            actual_breathing_data,
                                            actual_PIP_data,
                                            dt=actual_data_dt,
                                            start_time=actual_data_start_time,
                                            end_time=actual_data_end_time,
                                            skip_initial=7,
                                            use_pressure_error=True)
        self.assertLess(normalized_error, 1/actual_data_safety_factor,
                        "Fails to correctly calculate PIP for actual "
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
            [timestamps[i]/1000 for i in nonrepeat_timestamp_indices],
            [pressures[i] for i in nonrepeat_timestamp_indices],
            fill_value="extrapolate")

    return breathing_data


def get_PIP_data():
    global pip_data
    if pip_data is None:
        # PIP data hand-fitted to the pressure waveform
        raw_data = [(0, 17), (1.3, 17), (1.47, 20.80),
                    (1.54, 22.4), (1.65, 23.7), (1.74, 24.2),
                    (6.7, 24.2), (6.81, 24.3), (11.504, 24.3)]
        timestamps = [datum[0] for datum in raw_data]
        pressures = [datum[1] for datum in raw_data]
        pip_data = interp1d(timestamps, pressures,
                            fill_value="extrapolate")

    return pip_data


def get_PEEP_data():
    global peep_data
    if peep_data is None:
        # PEEP data hand-fitted to the pressure waveform
        raw_data = [(0, 8.22), (3.616, 8.22), (3.69, 8.22),
                    (3.91, 7.79), (4.02, 7.71), (9.00, 7.71),
                    (9.06, 7.74), (11.504, 7.74)]
        timestamps = [datum[0] for datum in raw_data]
        pressures = [datum[1] for datum in raw_data]
        peep_data = interp1d(timestamps, pressures,
                             fill_value="extrapolate")

    return peep_data


def actual_breathing_data(t):
    """Returns an actual breathing pressure waveform in [cmH2O] as a
    function of time in [s].
    """
    return get_breathing_data()(t)


def actual_PIP_data(t):
    return get_PIP_data()(t)


def actual_PEEP_data(t):
    return get_PEEP_data()(t)
