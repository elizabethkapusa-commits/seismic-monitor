import requests

filename = "../data/DION_001_2026-06-08_16-15-20.csv"

with open(filename, "rb") as f:

    response = requests.post(
        "http://127.0.0.1:5000/upload",
        files={"file": f}
    )

print(response.text)