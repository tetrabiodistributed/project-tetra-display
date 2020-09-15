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
        pass

    def append(self, datum):
        pass

    def get_datum(self):
        return math.nan
