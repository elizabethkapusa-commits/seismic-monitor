# Monitoring settings

SAMPLE_RATE = 100                 # samples per second
WINDOW_SECONDS = 10               # graph window size
EVENT_THRESHOLD = 1.2            # event detection threshold

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
FILTER_WINDOW = 5

# ADC settings

USE_REAL_ADC = False
ADC_PORT = "/dev/ttyUSB0"
ADC_BAUDRATE = 115200