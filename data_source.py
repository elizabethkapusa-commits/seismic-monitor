import numpy as np

from config import (
    USE_REAL_ADC,
    NOISE_LEVEL,
    NORMAL_WAVE_FREQUENCY,
    LOW_FREQUENCY_MOTION,
    EVENT_PROBABILITY,
    EVENT_MIN_MAGNITUDE,
    EVENT_MAX_MAGNITUDE,
    ADC_REFERENCE_VOLTAGE,
    ADC_RESOLUTION_BITS,
    SENSOR_GAIN,
    AMPLIFIER_GAIN,
    SIGNAL_OFFSET
)


# Convert raw ADC value to voltage

def convert_adc_to_voltage(raw_adc_value):
    max_adc_value = (2 ** ADC_RESOLUTION_BITS) - 1

    voltage = (
        raw_adc_value / max_adc_value
    ) * ADC_REFERENCE_VOLTAGE

    return voltage


# Apply calibration to voltage signal

def apply_calibration(voltage):
    calibrated_signal = (
        (voltage - SIGNAL_OFFSET)
        / (SENSOR_GAIN * AMPLIFIER_GAIN)
    )

    return calibrated_signal


# Simulated seismic signal
# Used before real hardware is connected

def read_simulated_sample(t):
    normal_vibration = 0.4 * np.sin(
        2 * np.pi * NORMAL_WAVE_FREQUENCY * t
    )

    low_frequency_motion = 0.8 * np.sin(
        2 * np.pi * LOW_FREQUENCY_MOTION * t
    )

    noise = np.random.normal(0, NOISE_LEVEL)

    event = 0

    if np.random.random() < EVENT_PROBABILITY:
        event = np.random.choice([-1, 1]) * np.random.uniform(
            EVENT_MIN_MAGNITUDE,
            EVENT_MAX_MAGNITUDE
        )

    sample = (
        normal_vibration
        + low_frequency_motion
        + noise
        + event
    )

    return sample


# Real ADC placeholder
# This will be replaced when the ADC hardware is selected and connected

def read_raw_adc_value():
    raise NotImplementedError(
        "Real ADC input is not connected yet. "
        "Set USE_REAL_ADC = False in config.py."
    )


# Read real ADC sample
# Raw ADC value -> voltage -> calibrated seismic signal

def read_adc_sample():
    raw_adc_value = read_raw_adc_value()

    voltage = convert_adc_to_voltage(raw_adc_value)

    calibrated_signal = apply_calibration(voltage)

    return calibrated_signal


# Main sample reader
# The logger calls only this function

def read_seismic_sample(t):
    if USE_REAL_ADC:
        return read_adc_sample()

    return read_simulated_sample(t)


# Report current data source

def get_data_source_name():
    if USE_REAL_ADC:
        return "ADC"

    return "SIMULATED"