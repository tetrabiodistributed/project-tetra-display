import math


class PEEP():

    def __init__(self, sampling_period, maximum_pressure=10):
        self._peak_finder = PIP(sampling_period,
                                minimum_pressure=-maximum_pressure)

    def append(self, datum):
        self._peak_finder.append(-datum)

    def get_datum(self):
        return -self._peak_finder.get_datum()


class PIP():

    def __init__(self, sampling_period, minimum_pressure=17):
        self._sampling_period = sampling_period
        self._minimum_pressure = minimum_pressure
        self._current_pip = minimum_pressure
        self._currently_in_pip_range = False

    def append(self, datum):
        if datum > self._minimum_pressure:
            if not self._currently_in_pip_range:
                self._currently_in_pip_range = True
                self._current_pip = datum
            else:
                if datum > self._current_pip:
                    self._current_pip = datum
        else:
            self._currently_in_pip_range = False

    def get_datum(self):
        return self._current_pip
