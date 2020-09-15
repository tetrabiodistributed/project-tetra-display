import math

from scipy import signal

from ringbuffer import RingBuffer
import constants


class PEEP():
    """A filter that takes a pressure waveform and gives the
    Positive-End Expiratory Pressure (PEEP).
    """

    def __init__(self,
                 sampling_period,
                 maximum_peep=constants.MAXIMUM_PEEP,
                 window_length=5,
                 polynomial_order=3,
                 buffer_length=10):
        """
        Parameters
        ----------
        sampling_period : float
            The amount of time between data samples.
        maximum_peep=constants.MAXIMUM_PEEP : float
            The maximum pressure considered to be PEEP.
        window_length=5 : int
            The number of points sampled for a low-pass filter of the
            data.  It must be odd.
        polynomial_order=3 : int
            The order of the Savitsky-Golay filter used to smooth the
            data.  It must be less than window_length.
        buffer_length=10 : int
            The number of data points considered when smoothing.
        """
        self._peak_finder = PIP(sampling_period,
                                minimum_pip=-maximum_peep,
                                window_length=window_length,
                                polynomial_order=polynomial_order,
                                buffer_length=buffer_length)

    def append(self, datum):
        """Adds a datum to the data buffer."""
        self._peak_finder.append(-datum)

    def get_datum(self):
        """Returns the current PEEP value."""
        return -self._peak_finder.get_datum()


class PIP():
    """A filter that takes a pressure waveform and gives the
    Peak Inspiratory Pressure (PIP).
    """

    def __init__(self,
                 sampling_period,
                 minimum_pip=constants.MINIMUM_PIP,
                 window_length=5,
                 polynomial_order=3,
                 buffer_length=10):
        """
        Parameters
        ----------
        sampling_period : float
            The amount of time between data samples.
        minimum_pip=constants.MINIMUM_PIP : float
            The maximum pressure considered to be PIP.
        window_length=5 : int
            The number of points sampled for a low-pass filter of the
            data.  It must be odd.
        polynomial_order=3 : int
            The order of the Savitsky-Golay filter used to smooth the
            data.  It must be less than window_length.
        buffer_length=10 : int
            The number of data points considered when smoothing.
        """
        if (window_length > buffer_length):
            raise ValueError("window_length must be <= buffer_length")
        if (window_length % 2 != 1):
            raise ValueError("window_length must be odd")
        if (buffer_length <= window_length):
            raise ValueError("buffer_length must be greater in length "
                             "than window_length")

        self._sampling_period = sampling_period
        self._minimum_pip = minimum_pip
        self._currently_in_pip_range = False
        self._current_pip = minimum_pip
        self._window_length = window_length
        self._polynomial_order = polynomial_order
        self._buffer_length = buffer_length
        self._data_buffer = RingBuffer(
            buffer_length,
            initial_state=[minimum_pip]*buffer_length)

    def append(self, datum):
        """Adds a datum to the data buffer."""
        if datum > self._minimum_pip:
            self._currently_in_pip_range = True
            if datum > self._data_buffer[-1]:
                self._update_pip(datum)
            else:
                self._update_pip(self._current_pip)
        else:
            self._currently_in_pip_range = False

    def get_datum(self):
        """Returns the current PIP value."""
        return self._current_pip

    def _update_pip(self, datum):
        self._data_buffer.append(datum)
        self._current_pip = (
            signal.savgol_filter(self._data_buffer,
                                 self._window_length,
                                 self._polynomial_order,
                                 mode="interp")[-1])
