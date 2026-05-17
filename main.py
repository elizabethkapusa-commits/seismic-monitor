import time
from collections import deque

import csv
import os

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from config import (
    SAMPLE_RATE,
    WINDOW_SECONDS,
    EVENT_THRESHOLD,
    GRAPH_TITLE,
    LINE_COLOR,
    BACKGROUND_COLOR,
    ENABLE_FILTER,
    FILTER_WINDOW,
    EVENT_COOLDOWN_SECONDS
)

from data_source import read_seismic_sample


# Base settings

MAX_POINTS = SAMPLE_RATE * WINDOW_SECONDS

times = deque(maxlen=MAX_POINTS)
raw_signals = deque(maxlen=MAX_POINTS)
filtered_signals = deque(maxlen=MAX_POINTS)
event_times = deque(maxlen=20)

start_time = time.time()
event_count = 0
last_event_time = None
last_detected_event_time = -999
event_marker_lines = []


# Create data folders and CSV log files

os.makedirs("data", exist_ok=True)
os.makedirs("events", exist_ok=True)

csv_file = open("data/seismic_log.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "time_seconds",
    "raw_amplitude",
    "filtered_amplitude",
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


# Digital filtering
# This smooths noisy signal values

def apply_filter():

    if not ENABLE_FILTER:
        return raw_signals[-1]

    if len(raw_signals) < FILTER_WINDOW:
        return raw_signals[-1]

    recent_values = list(raw_signals)[-FILTER_WINDOW:]

    return sum(recent_values) / len(recent_values)


# Create waveform

fig, ax = plt.subplots(figsize=(10, 5))

fig.canvas.manager.set_window_title("Live Seismic Monitoring Dashboard")

fig.patch.set_facecolor(BACKGROUND_COLOR)
ax.set_facecolor(BACKGROUND_COLOR)

line, = ax.plot([], [], color=LINE_COLOR, linewidth=1.5)

ax.set_title(GRAPH_TITLE)
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


# Clean event markers

def update_event_markers(current_time):

    global event_marker_lines

    for marker in event_marker_lines:
        marker.remove()

    event_marker_lines = []

    for event_time in list(event_times):

        if event_time >= current_time - WINDOW_SECONDS:

            marker = ax.axvline(
                x=event_time,
                color="red",
                linestyle="--",
                alpha=0.4
            )

            event_marker_lines.append(marker)


# Animation update

def update(frame):

    global event_count
    global last_event_time
    global last_detected_event_time

    current_time = time.time() - start_time

    raw_sample = read_seismic_sample(current_time)

    raw_signals.append(raw_sample)

    filtered_sample = apply_filter()

    filtered_signals.append(filtered_sample)

    times.append(current_time)

    # Event detection

    status = (
        "EVENT DETECTED"
        if abs(filtered_sample) > EVENT_THRESHOLD
        else "Normal monitoring"
    )

    # Save all data to CSV

    csv_writer.writerow([
        round(current_time, 4),
        round(raw_sample, 6),
        round(filtered_sample, 6),
        status
    ])

    csv_file.flush()

    if status == "EVENT DETECTED":

        time_since_last_event = (
            current_time - last_detected_event_time
        )

        if time_since_last_event >= EVENT_COOLDOWN_SECONDS:

            event_count += 1

            last_event_time = current_time
            last_detected_event_time = current_time

            event_times.append(current_time)

            event_writer.writerow([
                event_count,
                round(current_time, 4),
                round(filtered_sample, 6),
                status
            ])

            event_file.flush()

            event_image_path = (
                f"events/event_{event_count}.png"
            )

            fig.savefig(event_image_path)

    # Update waveform

    if len(times) > 1:

        line.set_data(list(times), list(filtered_signals))

        ax.set_xlim(
            max(0, current_time - WINDOW_SECONDS),
            current_time
        )

    # Change waveform color during events

    if status == "EVENT DETECTED":
        line.set_color("red")
    else:
        line.set_color(LINE_COLOR)

    # Update clean event markers

    update_event_markers(current_time)

    # Calculate rolling statistics

    max_amplitude = (
        max(abs(value) for value in filtered_signals)
        if filtered_signals
        else 0
    )

    average_amplitude = (
        sum(abs(value) for value in filtered_signals) / len(filtered_signals)
        if filtered_signals
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
        f"Window: {WINDOW_SECONDS} s\n"
        f"Threshold: {EVENT_THRESHOLD}\n"
        f"Filter Enabled: {ENABLE_FILTER}\n"
        f"Latest Amplitude: {filtered_sample:.3f}\n"
        f"Max Amplitude: {max_amplitude:.3f}\n"
        f"Average Amplitude: {average_amplitude:.3f}\n"
        f"Samples Collected: {len(filtered_signals)}\n"
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