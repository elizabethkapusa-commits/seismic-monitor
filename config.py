# Monitoring settings

SAMPLE_RATE = 100                 # samples per second
WINDOW_SECONDS = 10               # graph window size
EVENT_THRESHOLD = 2.0           # event detection threshold

# Signal settings

NOISE_LEVEL = 0.15
NORMAL_WAVE_FREQUENCY = 1.2
LOW_FREQUENCY_MOTION = 0.25

# Event settings

EVENT_PROBABILITY = 0.015
EVENT_MIN_MAGNITUDE = 1.5
EVENT_MAX_MAGNITUDE = 3.0
EVENT_COOLDOWN_SECONDS = 2.0

# Dashboard settings

GRAPH_TITLE = "Real-Time Seismic Waveform"
LINE_COLOR = "black"
BACKGROUND_COLOR = "white"

# Filtering settings

ENABLE_FILTER = True
FILTER_WINDOW = 3

# ADC settings

USE_REAL_ADC = False
ADC_PORT = "/dev/ttyUSB0"
ADC_BAUDRATE = 115200

# Calibration settings

ADC_REFERENCE_VOLTAGE = 3.3
ADC_RESOLUTION_BITS = 16
SENSOR_GAIN = 1.0
AMPLIFIER_GAIN = 1.0
SIGNAL_OFFSET = 0.0

# Frequency analysis settings

ENABLE_FFT = True
FFT_MIN_POINTS = 64
FFT_UPDATE_INTERVAL = 10

# Station settings

STATION_ID = "DION_001"
DATA_FOLDER = "data"
LOG_FILE_SECONDS = 60
USE_UTC_TIME = True
STATION_LOCATION = "DION 310"
DATA_SOURCE_NAME = "SIMULATED"
USE_GPS_TIME = False
METADATA_FILENAME = "station_metadata.json"

# Upload settings

ONEDRIVE_UPLOAD_FOLDER = "onedrive_uploads"
ENABLE_UPLOAD_SIMULATION = True
EVENT_LOG_FILE = "event_log.csv"
