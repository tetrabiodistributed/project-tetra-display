from datetime import datetime
from pytz import timezone, utc
import math


class ProcessSampleData():
    """Parses a file with flow rate, tidal volume, and optionally
    pressure data.  The expected formats are

    `%f\tSLMx10:%f.2\tTidalVol:%f.2\n`
    with the first number being the floating-point milliseconds since
    Epoch, the second being ten times the flow rate in mL/s, and the
    last being the tidal volume in mL, and

    `%H:%M:%S.%f -> SLMx10:%f.2\tTidalVol:%f.2\tPressurex10:%f.2`
    with the first 11 character representing the time the datum was
    recorded as if on a digital clock (assuming the date as 2020-06-09
    and timezone as US/Pacific), the %f.2 after `SLMx10:` representing
    ten times the flow rate, the following %f.2 representing the tidal
    volume, and the last representing ten times the pressure.
    """

    def __init__(self, path_to_data):
        with open(path_to_data, "r") as flow_data_file:
            self._parse_data(flow_data_file)

    def __len__(self):
        return len(self.timestamps)

    @property
    def timestamps(self):
        """Gives the list of timestamps data were taken at in
        milliseconds since Epoch
        """

        return self._timestamps

    def relative_timestamps(self):
        """Gives the list of timestamps data were taken at in
        milliseconds since the first data point
        """

        return [timestamp - self.timestamps[0]
                for timestamp in self.timestamps]

    @property
    def flow_rates(self):
        """Gives the list of flow rates in mL/s"""
        return self._flow_rates

    @property
    def tidal_volumes(self):
        """Gives the list of tidal volumes in mL"""
        return self._tidal_volumes

    @property
    def pressures(self):
        """Gives the list of pressures in cmH2O"""
        return self._pressures

    def _parse_data(self, flow_data_file):
        self._timestamps = []
        self._flow_rates = []
        self._tidal_volumes = []
        self._pressures = []
        FLOW_RATE_MARKER = "SLMx10:"
        TIDAL_VOLUME_MARKER = "TidalVol:"
        PRESSURE_MARKER = "Pressurex10:"

        previous_data = [None, None, math.inf]
        for datum in flow_data_file:
            splitDatum = datum.replace(" -> ", "\t").split("\t")
            try:
                current_timestamp = float(splitDatum[0])
            except ValueError:
                current_timestamp = (
                    timezone("US/Pacific")
                    .localize(datetime
                              .strptime(splitDatum[0],
                                        "%H:%M:%S.%f")
                              .replace(year=2020,
                                       month=6,
                                       day=9))
                    .astimezone(utc)
                    .timestamp() * 1000.0)

            current_flow_rate = float(splitDatum[1]
                                      .replace(FLOW_RATE_MARKER, "")
                                      .strip("\n")) / 10
            current_tidal_volume = float(splitDatum[2]
                                         .replace(TIDAL_VOLUME_MARKER, "")
                                         .strip("\n"))

            if (PRESSURE_MARKER in datum):
                current_pressure = float(splitDatum[3]
                                         .replace(PRESSURE_MARKER, "")
                                         .strip("\n")) / 10
            else:
                current_pressure = math.inf

            if ([current_flow_rate, current_tidal_volume, current_pressure]
                    != previous_data):
                self._timestamps.append(current_timestamp)
                self._flow_rates.append(current_flow_rate)
                self._tidal_volumes.append(current_tidal_volume)
                if current_pressure != math.inf:
                    self.pressures.append(current_pressure)
                previous_data = [current_flow_rate,
                                 current_tidal_volume,
                                 current_pressure]
