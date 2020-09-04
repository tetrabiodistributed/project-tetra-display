import numpy as np
from scipy import signal
from ringbuffer import RingBuffer


class CausalVelocityFilter():
    """Calculates the derivative of data that's appended to the
    internal buffer and allows you to get a moving average of the
    derivative with window size defined by the init.
    """

    def __init__(self,
                 sampling_period,
                 window_length=99,
                 polynomial_order=5,
                 buffer_length=100):
        """Initializes self.
        windowSize defines the width of the moving average buffer.
        Too narrow and it doesn't do much filtering, too wide and it
        lags behind the acutal derivative
        """
        if (window_length > buffer_length):
            raise ValueError("window_length must be <= buffer_length")
        if (window_length % 2 != 1):
            raise ValueError("window_length must be odd")
        if (buffer_length <= window_length):
            raise ValueError("buffer_length must be greater in length "
                             "than window_length")

        self._buffer_size = buffer_length
        self._data_buffer = RingBuffer(buffer_length)
        self._sampling_period = sampling_period
        self._polynomial_order = polynomial_order
        self._window_length = window_length
        self._buffer_size_diff = buffer_length - window_length

    def get_datum(self):
        """Get the present rate of change of the incomimg data.  For the
        first few data points, there might be large error, but that will
        dissapear after the data buffer fills up.
        """
        if len(self._data_buffer) >= self._window_length:
            return signal.savgol_filter(
                self._data_buffer,
                self._window_length,
                self._polynomial_order,
                deriv=1,
                delta=self._sampling_period,
                mode="interp")[-1]
        elif len(self._data_buffer) == 1:
            return self._data_buffer[-1]
        else:
            derivatives = [(self._data_buffer[i] - self._data_buffer[i-1])
                           / self._sampling_period
                           for i in range(-min(5,
                                               len(self._data_buffer)-1),
                                          0)]
            return np.mean(derivatives)

    def append(self, datum):
        """Add a measurement and an elapsed time to the filter's
        internal buffer to be able to find the rate of change.
        """
        self._data_buffer.append(datum)
