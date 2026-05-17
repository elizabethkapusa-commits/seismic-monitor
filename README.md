# Live Seismic Monitoring Dashboard

A real-time seismic waveform monitoring dashboard built in Python.

This project simulates seismic activity, performs event detection, applies digital filtering, logs waveform data, and visualizes live seismic signals in real time.


# Features

- Real-time waveform plotting
- Simulated seismic signal generation
- Event detection system
- Configurable detection threshold
- Signal filtering and smoothing
- Event cooldown protection
- CSV data logging
- Event screenshot capture
- Event timeline markers
- ADC-ready architecture
- Configurable system settings
- Rolling dashboard statistics


# Technologies Used

- Python
- NumPy
- Matplotlib
- SciPy


# Project Structure

```text
seismic-monitor/
│
├── main.py
├── config.py
├── data_source.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── seismic_log.csv
│   └── event_log.csv
│
├── events/
│   └── event screenshots
│
└── .venv/