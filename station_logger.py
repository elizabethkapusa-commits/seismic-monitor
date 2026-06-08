import csv
import os
import time
from datetime import datetime, timezone
import shutil
import json

from config import (
    SAMPLE_RATE,
    STATION_ID,
    DATA_FOLDER,
    LOG_FILE_SECONDS,
    ONEDRIVE_UPLOAD_FOLDER,
    ENABLE_UPLOAD_SIMULATION,
    STATION_LOCATION,
    DATA_SOURCE_NAME,
    USE_GPS_TIME,
    METADATA_FILENAME
)

from data_source import read_seismic_sample


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
                    "source"
                    
                ])

                while time.time() - file_start_time < LOG_FILE_SECONDS:

                    timestamp_utc = get_utc_timestamp()

                    current_time = time.time()

                    raw_value = read_seismic_sample(current_time)

                    csv_writer.writerow([
                        timestamp_utc,
                        STATION_ID,
                        sample_index,
                        raw_value,
                        "SIMULATED"

                    ])

                    csv_file.flush()

                    sample_index += 1

                    time.sleep(sample_interval)

            upload_completed_file(log_filename)        

    except KeyboardInterrupt:

        print("\nStation logger stopped.")


# Run logger

if __name__ == "__main__":
    run_station_logger()