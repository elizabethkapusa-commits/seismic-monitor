from flask import Flask, request, send_from_directory
import os
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = "data"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_station_id_from_filename(filename):
    parts = filename.split("_")

    if len(parts) >= 2:
        return f"{parts[0]}_{parts[1]}"

    return "UNKNOWN_STATION"

def get_file_stats(filename):

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    sample_count = 0
    last_timestamp = "N/A"
    last_value = "N/A"
    last_status = "N/A"

    try:
        with open(filepath, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                sample_count += 1
                last_timestamp = row.get("timestamp_utc", "N/A")
                last_value = row.get("raw_value", "N/A")
                last_status = row.get("event_status", "N/A")

    except Exception as error:
        return {
            "sample_count": "Error",
            "last_timestamp": str(error),
            "last_value": "N/A",
            "last_status": "N/A"
        }

    return {
        "sample_count": sample_count,
        "last_timestamp": last_timestamp,
        "last_value": last_value,
        "last_status": last_status
    }

@app.route("/")
def home():
    return "Seismic Server Running"


@app.route("/upload", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return "No file provided", 400

    file = request.files["file"]

    station_id = get_station_id_from_filename(file.filename)

    station_folder = os.path.join(
        UPLOAD_FOLDER,
        station_id
    )

    os.makedirs(station_folder, exist_ok=True)

    filepath = os.path.join(
        station_folder,
        file.filename
    )

    file.save(filepath)

    return f"Uploaded {file.filename} to {station_id}", 200


# ADD THIS NEW ROUTE HERE
@app.route("/files")
def list_files():

    files = os.listdir(UPLOAD_FOLDER)

    html = "<h1>Uploaded Files</h1><ul>"

    for file in files:
        html += f'<li><a href="/files/{file}">{file}</a></li>'

    html += "</ul>"

    return html


@app.route("/files/<filename>")
def view_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/dashboard")
def dashboard():

    files = os.listdir(UPLOAD_FOLDER)

    station_summary = {}

    for file in files:
        if not file.endswith(".csv"):
            continue

        station_id = file.split("_2026")[0]

        if station_id not in station_summary:
            station_summary[station_id] = {
                "count": 0,
                "latest_file": file
            }

        station_summary[station_id]["count"] += 1

        if file > station_summary[station_id]["latest_file"]:
            station_summary[station_id]["latest_file"] = file

    html = "<h1>Seismic Monitoring Dashboard</h1>"

    for station_id, info in station_summary.items():
        latest_file = info["latest_file"]
        stats = get_file_stats(latest_file)

        html += f"""
        <h2>{station_id}</h2>

        <p><strong>Total Files:</strong>
        <a href="/station/{station_id}">{info["count"]}</a></p>

        <p><strong>Latest File:</strong>
        <a href="/files/{latest_file}">{latest_file}</a></p>

        <p><a href="/station/{station_id}/plot">View Latest Waveform</a></p>

        <p><strong>Latest Sample Count:</strong> {stats["sample_count"]}</p>
        <p><strong>Last Update Time:</strong> {stats["last_timestamp"]}</p>
        <p><strong>Last Value:</strong> {stats["last_value"]}</p>
        <p><strong>Last Status:</strong> {stats["last_status"]}</p>

        <hr>
        """

    return html

@app.route("/station/<station_id>")
def station_files(station_id):

    files = []

    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith(station_id):
            files.append(file)

    files.sort(reverse=True)

    html = f"<h1>{station_id} Files</h1><ul>"

    for file in files:
        html += f'<li><a href="/files/{file}">{file}</a></li>'

    html += "</ul>"

    html += '<p><a href="/dashboard">Back to Dashboard</a></p>'

    return html

@app.route("/station/<station_id>/plot")
def station_plot(station_id):

    station_files = []

    for file in os.listdir(UPLOAD_FOLDER):
        if file.startswith(station_id) and file.endswith(".csv"):
            station_files.append(file)

    if not station_files:
        return f"No files found for {station_id}"

    station_files.sort(reverse=True)
    latest_file = station_files[0]

    filepath = os.path.join(UPLOAD_FOLDER, latest_file)

    times = []
    values = []

    with open(filepath, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            times.append(len(times))
            values.append(float(row["raw_value"]))

    plot_filename = f"{station_id}_latest_plot.png"
    plot_path = os.path.join(UPLOAD_FOLDER, plot_filename)

    plt.figure(figsize=(10, 4))
    plt.plot(times, values)
    plt.title(f"Latest Waveform for {station_id}")
    plt.xlabel("Sample Number")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    html = f"""
    <h1>Latest Waveform for {station_id}</h1>
    <p><strong>Source File:</strong> {latest_file}</p>
    <img src="/files/{plot_filename}" width="900">
    <p><a href="/dashboard">Back to Dashboard</a></p>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)