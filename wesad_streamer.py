import pandas as pd
import requests
import time
from datetime import datetime

# Flask API URL
# url = "https://wearable-stress-api.onrender.com/predict"
url = "http://127.0.0.1:5000/predict"

# Load WESAD feature data
df = pd.read_csv("s6_stream_data.csv")

# Simulated device ID
device_id = "ESP32_WESAD_S6"

print("\nStarting WESAD Real Data Stream...\n")

# Stream each row one by one
for index, row in df.iterrows():

    sensor_data = {

        "device_id": device_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "mean_eda": float(row["mean_eda"]),
        "std_eda": float(row["std_eda"]),
        "eda_slope": float(row["eda_slope"]),

        "mean_acc": float(row["mean_acc"]),
        "var_acc": float(row["var_acc"]),

        "heart_rate": float(row["heart_rate"]),
        "hrv": float(row["hrv"])
    }

    try:

        # Send request
        response = requests.post(url, json=sensor_data)

        result = response.json()

        print("========================================")
        print("Row:", index)

        print("Ground Truth:",
              "Stress" if row["label"] == 1 else "Non-Stress")

        print("Predicted:",
              result["label"])

        print("Stress Probability:",
              round(result["stress_probability"], 2))

        print("========================================\n")

    except Exception as e:
        print("Connection Error:", e)

    # Simulate real-time wearable transmission
    time.sleep(2)