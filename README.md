# Real-Time Seismic Monitoring Dashboard

A Python-based real-time seismic waveform monitoring system designed for live signal acquisition, filtering, event detection, and future ADC hardware integration.

---

# Features

- Real-time waveform visualization
- Live seismic signal simulation
- Event detection using adjustable thresholds
- Automatic event screenshot capture
- Adjustable sample rate and monitoring window
- Digital filtering using SciPy
- ADC-ready architecture for future hardware integration
- Signal calibration structure
- CSV event logging
- Modular project structure

---

# Project Structure

```text
seismic-monitor/
│
├── main.py               # Main dashboard and plotting logic
├── config.py             # Adjustable system settings
├── data_source.py        # Signal acquisition and ADC structure
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── data/                 # CSV logs
├── events/               # Saved event screenshots
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/elizabethkapusa-commits/seismic-monitor.git
```

Enter the project folder:

```bash
cd seismic-monitor
```

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Project

Run the dashboard using:

```bash
python3 main.py
```

---

# Adjustable Settings

Settings can be modified inside `config.py`:

- Sample rate
- Event threshold
- Window size
- Noise level
- Filter settings
- ADC calibration values

---

# Future Hardware Integration

The software is designed to support future ADC hardware integration.

The current architecture includes:
- ADC placeholder structure
- Voltage conversion
- Signal calibration pipeline
- Real/simulated signal switching

Future versions may support:
- USB ADC boards
- Raspberry Pi ADC modules
- SPI/I2C sensor communication
- Real seismic sensor input

---

# Technologies Used

- Python
- NumPy
- Matplotlib
- SciPy

---

# Current Development Phase

Phase 1:
- Real-time visualization
- Event detection
- Filtering
- Logging
- Calibration structure

Upcoming:
- Real ADC integration
- Advanced filtering
- Spectral analysis
- Multi-channel monitoring
- Database integration

---

# Author

Elizabeth Kapusa
MS Computer Engineering
UMass Dartmouth