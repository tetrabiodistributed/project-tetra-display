import math

from scipy import signal

from ringbuffer import RingBuffer


class PEEP():

    def __init__(self,
                 sampling_period,
                 maximum_pressure=8.23,
                 window_length=5,
                 polynomial_order=3,
                 buffer_length=10):
        self._peak_finder = PIP(sampling_period,
                                minimum_pressure=-maximum_pressure,
                                window_length=window_length,
                                polynomial_order=polynomial_order,
                                buffer_length=buffer_length)

    def append(self, datum):
        self._peak_finder.append(-datum)

    def get_datum(self):
        return -self._peak_finder.get_datum()


class PIP():

    def __init__(self,
                 sampling_period,
                 minimum_pressure=17,
                 window_length=5,
                 polynomial_order=3,
                 buffer_length=10):
        self._sampling_period = sampling_period
        self._minimum_pressure = minimum_pressure
        self._currently_in_pip_range = False
        self._current_pip = minimum_pressure
        self._window_length = window_length
        self._polynomial_order = polynomial_order
        self._buffer_length = buffer_length
        self._data_buffer = RingBuffer(
            buffer_length,
            initial_state=[minimum_pressure]*buffer_length)

    def append(self, datum):
        if datum > self._minimum_pressure:
            self._currently_in_pip_range = True
            if datum > self._data_buffer[-1]:
                self._update_pip(datum)
            else:
                self._update_pip(self._current_pip)
        else:
            self._currently_in_pip_range = False

    def get_datum(self):
        return self._current_pip

    def _update_pip(self, datum):
        self._data_buffer.append(datum)
        self._current_pip = (
            signal.savgol_filter(self._data_buffer,
                                 self._window_length,
                                 self._polynomial_order,
                                 mode="interp")[-1])
