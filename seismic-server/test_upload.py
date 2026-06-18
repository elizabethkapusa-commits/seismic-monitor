import requests

filename = "DION_001_test_station.mseed"

with open(filename, "rb") as file:
    response = requests.post(
        "http://127.0.0.1:5000/upload",
        files={"file": file}
    )

print(response.text)
