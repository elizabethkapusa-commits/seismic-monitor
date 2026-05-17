import numpy as np

from config import (
    USE_REAL_ADC,
    NOISE_LEVEL,
    NORMAL_WAVE_FREQUENCY,
    LOW_FREQUENCY_MOTION,
    EVENT_PROBABILITY,
    EVENT_MIN_MAGNITUDE,
    EVENT_MAX_MAGNITUDE
)


# Simulated seismic signal
# Later this can be replaced by ADC readings

def read_simulated_sample(t):
    normal_vibration = 0.4 * np.sin(2 * np.pi * NORMAL_WAVE_FREQUENCY * t)
    low_frequency_motion = 0.8 * np.sin(2 * np.pi * LOW_FREQUENCY_MOTION * t)
    noise = np.random.normal(0, NOISE_LEVEL)

    event = 0

    if np.random.random() < EVENT_PROBABILITY:
        event = np.random.choice([-1, 1]) * np.random.uniform(
            EVENT_MIN_MAGNITUDE,
            EVENT_MAX_MAGNITUDE
        )

    return normal_vibration + low_frequency_motion + noise + event


# ADC placeholder
# We will update this when we know the real ADC board

def read_adc_sample(t):
    raise NotImplementedError(
        "Real ADC input is not connected yet. "
        "Set USE_REAL_ADC = False in config.py."
    )


# Main sample reader

def read_seismic_sample(t):
    if USE_REAL_ADC:
        return read_adc_sample(t)

    return read_simulated_sample(t)