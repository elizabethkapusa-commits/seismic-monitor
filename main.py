import time
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import os


# Base settings

SAMPLE_RATE = 100          # samples per second
WINDOW_SECONDS = 10        # show last 10 seconds
MAX_POINTS = SAMPLE_RATE * WINDOW_SECONDS
EVENT_THRESHOLD = 2.0      # event detection threshold

times = deque(maxlen=MAX_POINTS)
signals = deque(maxlen=MAX_POINTS)
event_times = deque(maxlen=20)

start_time = time.time()
event_count = 0
last_event_time = None


# Create data folders and CSV log files

os.makedirs("data", exist_ok=True)
os.makedirs("events", exist_ok=True)

csv_file = open("data/seismic_log.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "time_seconds",
    "amplitude",
    "status"
])

event_file = open("data/event_log.csv", mode="w", newline="")
event_writer = csv.writer(event_file)

event_writer.writerow([
    "event_number",
    "time_seconds",
    "amplitude",
    "status"
])


# Simulated seismic signal
# Later we will replace this by ADC readings

def read_seismic_sample(t):
    normal_vibration = 0.4 * np.sin(2 * np.pi * 1.2 * t)
    low_frequency_motion = 0.8 * np.sin(2 * np.pi * 0.25 * t)
    noise = np.random.normal(0, 0.15)

    # Simulated seismic event spike sometimes

    event = 0

    if np.random.random() < 0.015:
        event = np.random.choice([-1, 1]) * np.random.uniform(1.5, 3.0)

    return normal_vibration + low_frequency_motion + noise + event


# Create waveform

fig, ax = plt.subplots(figsize=(10, 5))

fig.canvas.manager.set_window_title("Live Seismic Monitoring Dashboard")

line, = ax.plot([], [], color="black", linewidth=1.5)

ax.set_title("Real-Time Seismic Waveform")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.set_ylim(-4, 4)
ax.grid(True)

status_text = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    verticalalignment="top"
)


# Animation update

def update(frame):

    global event_count
    global last_event_time

    current_time = time.time() - start_time

    sample = read_seismic_sample(current_time)

    # Event detection

    status = (
        "EVENT DETECTED"
        if abs(sample) > EVENT_THRESHOLD
        else "Normal monitoring"
    )

    # Save all data to CSV

    csv_writer.writerow([
        round(current_time, 4),
        round(sample, 6),
        status
    ])

    csv_file.flush()

    # Store live data

    times.append(current_time)
    signals.append(sample)

    # Event actions

    if status == "EVENT DETECTED":

        event_count += 1
        last_event_time = current_time
        event_times.append(current_time)

        event_writer.writerow([
            event_count,
            round(current_time, 4),
            round(sample, 6),
            status
        ])

        event_file.flush()

        # Save event screenshot

        event_image_path = f"events/event_{event_count}.png"
        fig.savefig(event_image_path)

    # Update waveform

    if len(times) > 1:

        line.set_data(times, signals)

        ax.set_xlim(
            max(0, current_time - WINDOW_SECONDS),
            current_time
        )

    # Change waveform color during events

    if status == "EVENT DETECTED":
        line.set_color("red")
    else:
        line.set_color("black")

    # Add event markers

    for event_time in list(event_times):

        if event_time >= current_time - WINDOW_SECONDS:

            ax.axvline(
                x=event_time,
                color="red",
                linestyle="--",
                alpha=0.4
            )

    # Calculate rolling statistics

    max_amplitude = max(abs(value) for value in signals) if signals else 0
    average_amplitude = (
        sum(abs(value) for value in signals) / len(signals)
        if signals
        else 0
    )

    last_event_display = (
        f"{last_event_time:.2f} s"
        if last_event_time is not None
        else "None"
    )

    # Update dashboard text

    status_text.set_text(
        f"Status: {status}\n"
        f"Sample Rate: {SAMPLE_RATE} Hz\n"
        f"Threshold: {EVENT_THRESHOLD}\n"
        f"Latest Amplitude: {sample:.3f}\n"
        f"Max Amplitude: {max_amplitude:.3f}\n"
        f"Average Amplitude: {average_amplitude:.3f}\n"
        f"Samples Collected: {len(signals)}\n"
        f"Events Detected: {event_count}\n"
        f"Last Event Time: {last_event_display}"
    )

    return line, status_text


# Create animation

ani = FuncAnimation(
    fig,
    update,
    interval=1000 / SAMPLE_RATE,
    blit=False,
    cache_frame_data=False
)


# Display dashboard

plt.tight_layout()

try:
    plt.show()

finally:
    csv_file.close()
    event_file.close()

    print("Seismic data saved to data/seismic_log.csv")
    print("Event data saved to data/event_log.csv")
    print("Event screenshots saved to events/")