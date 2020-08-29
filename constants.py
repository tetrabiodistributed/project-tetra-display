# Constants for the display software for the
# Tetra Biodistributed Ventillator Splitter

DESCRIPTORS = ("Inspiratory Pressure", "Tidal Volume", "PEEP", "PIP")
DESCRIPTORS_HTML = ("dP", "Tv", "PEEP", "PIP")

NUMBER_OF_PATIENTS = 4
PRESSURE_SENSOR = "SPL06_007"
SENSIRION_SENSOR = "SFM3300"
MASS_AIRFLOW_SENSOR = "Mass Air Flow"  # TODO: find part no.

PRESSURE_SENSOR_MUX_ADDRESS = 0x70
FLOW_SENSOR_MUX_ADDRESS = 0x74

NUMBER_OF_PRESSURE_SENSORS = NUMBER_OF_PATIENTS + 1
NUMBER_OF_SENSIRION_SENSORS = NUMBER_OF_PATIENTS
NUMBER_OF_MASS_AIRFLOW_SENSORS = NUMBER_OF_PATIENTS
MAX_SENSOR_COUNT = max(NUMBER_OF_PRESSURE_SENSORS,
                       NUMBER_OF_SENSIRION_SENSORS,
                       NUMBER_OF_MASS_AIRFLOW_SENSORS)
CALIBRATION_PRESSURE_SENSOR_INDEX = NUMBER_OF_PRESSURE_SENSORS - 1

# These must be from the set {1, 2, 4, 8, 16, 32, 64, 128}
PRESSURE_SAMPLING_RATE = 1  # Hz
PRESSURE_OVERSAMPLING = 16
TEMPERATURE_SAMPLING_RATE = 1  # Hz
TEMPERATURE_OVERSAMPLING = 1

# Environment variables for testing off of hardware
SENSOR_QUANTITY = "SENSOR_QUANTITY"
ENOUGH_SENSORS = "ENOUGH_SENSORS"
TOO_MANY_SENSORS = "TOO_MANY_SENSORS"
NOT_ENOUGH_SENSORS = "NOT_ENOUGH_SENSORS"
