import csv
import os
import time
from datetime import datetime, timezone
import shutil
import json
import sys
import requests


from config import (
    DATA_FOLDER,
    LOG_FILE_SECONDS,
    ONEDRIVE_UPLOAD_FOLDER,
    ENABLE_UPLOAD_SIMULATION,
    METADATA_FILENAME,
    EVENT_THRESHOLD,
    EVENT_LOG_FILE,
    EVENT_COOLDOWN_SECONDS
)

from data_source import read_seismic_sample

from event_detector import get_event_status

SERVER_UPLOAD_URL = "http://127.0.0.1:5000/upload"

def load_station_config(config_path):

    with open(config_path, mode="r") as station_file:
        return json.load(station_file)

STATION_CONFIG_FILE = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "stations/dion_station.json"
)

station_config = load_station_config(STATION_CONFIG_FILE)

print(f"Loaded station configuration: {STATION_CONFIG_FILE}")

STATION_ID = station_config["station_id"]
STATION_LOCATION = station_config["station_location"]
SAMPLE_RATE = station_config["sample_rate"]
USE_GPS_TIME = station_config["gps_enabled"]
DATA_SOURCE_NAME = station_config["data_source"]

last_logged_event_time = None

# Create data folder

os.makedirs(DATA_FOLDER, exist_ok=True)


# Get UTC timestamp

def get_utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


# Create a new CSV filename

def create_log_filename():
    current_time = datetime.now(timezone.utc)

    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{STATION_ID}_{timestamp}.csv"

    return os.path.join(DATA_FOLDER, filename)

# Copy completed file to upload folder

def upload_completed_file(log_filename):

    if not ENABLE_UPLOAD_SIMULATION:
        return

    os.makedirs(ONEDRIVE_UPLOAD_FOLDER, exist_ok=True)

    upload_path = os.path.join(
        ONEDRIVE_UPLOAD_FOLDER,
        os.path.basename(log_filename)
    )

    shutil.copy(log_filename, upload_path)

    print(f"Copied completed file to {upload_path}")

def upload_file_to_server(log_filename):
    try:
        with open(log_filename, "rb") as file:
            response = requests.post(
                SERVER_UPLOAD_URL,
                files={"file": file}
            )

        if response.status_code == 200:
            print(f"Uploaded to server: {log_filename}")
        else:
            print(f"Server upload failed: {response.text}")

    except Exception as error:
        print(f"Could not upload to server: {error}")

# Create station metadata file

def create_station_metadata():

    metadata = {
        "station_id": STATION_ID,
        "station_location": STATION_LOCATION,
        "sample_rate": SAMPLE_RATE,
        "data_folder": DATA_FOLDER,
        "upload_folder": ONEDRIVE_UPLOAD_FOLDER,
        "data_source": DATA_SOURCE_NAME,
        "gps_time_enabled": USE_GPS_TIME,
        "log_file_seconds": LOG_FILE_SECONDS,
        "created_utc": get_utc_timestamp()
    }

    metadata_path = os.path.join(
        DATA_FOLDER,
        METADATA_FILENAME
    )

    with open(metadata_path, mode="w") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

    print(f"Station metadata saved to {metadata_path}")

def write_event_summary(timestamp_utc, raw_value, event_status):

    global last_logged_event_time

    if event_status != "EVENT_DETECTED":
        return

    current_time = time.time()

    if last_logged_event_time is not None:
        time_since_last_event = current_time - last_logged_event_time

        if time_since_last_event < EVENT_COOLDOWN_SECONDS:
            return

    last_logged_event_time = current_time

    event_log_path = os.path.join(DATA_FOLDER, EVENT_LOG_FILE)

    file_exists = os.path.exists(event_log_path)

    with open(event_log_path, mode="a", newline="") as event_file:

        event_writer = csv.writer(event_file)

        if not file_exists:
            event_writer.writerow([
                "timestamp_utc",
                "station_id",
                "station_location",
                "raw_value",
                "event_status",
                "data_source"
            ])

        event_writer.writerow([
            timestamp_utc,
            STATION_ID,
            STATION_LOCATION,
            raw_value,
            event_status,
            DATA_SOURCE_NAME
        ])

# Main logging function

def run_station_logger():

    sample_interval = 1 / SAMPLE_RATE
    sample_index = 0

    print(f"Starting station logger for {STATION_ID}")
    print(f"Sample rate: {SAMPLE_RATE} samples/second")
    print(f"Creating new file every {LOG_FILE_SECONDS} seconds")
    print("Press Ctrl + C to stop logging.")
    create_station_metadata()

    try:

        while True:

            file_start_time = time.time()
            log_filename = create_log_filename()

            print(f"Writing to {log_filename}")

            with open(log_filename, mode="w", newline="") as csv_file:

                csv_writer = csv.writer(csv_file)

                csv_writer.writerow([
                    "timestamp_utc",
                    "station_id",
                    "sample_index",
                    "raw_value",
                    "source",
                    "event_status"
                    
                ])

                while time.time() - file_start_time < LOG_FILE_SECONDS:

                    timestamp_utc = get_utc_timestamp()

                    current_time = time.time()

                    raw_value = read_seismic_sample(current_time)

                    event_status = get_event_status(raw_value, EVENT_THRESHOLD)

                    write_event_summary(timestamp_utc, raw_value, event_status)

                    csv_writer.writerow([
                        timestamp_utc,
                        STATION_ID,
                        sample_index,
                        raw_value,
                        DATA_SOURCE_NAME,
                        event_status

                    ])

                    csv_file.flush()

                    sample_index += 1

                    time.sleep(sample_interval)

            upload_completed_file(log_filename)
            upload_file_to_server(log_filename)

               

    except KeyboardInterrupt:

        print("\nStation logger stopped.")


# Run logger

if __name__ == "__main__":
    run_station_logger()