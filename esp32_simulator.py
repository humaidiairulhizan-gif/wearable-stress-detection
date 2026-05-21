import requests
import time
import random
from datetime import datetime

# Flask API URL
url = "https://wearable-stress-api.onrender.com/predict"

# Simulated device ID
device_id = "ESP32_WRIST_01"

# -----------------------------------
# CHANGE MODE HERE
# -----------------------------------

# mode = random.choice(["relaxed", "stress"])

# mode = "relaxed" # change this 
# mode = "stress" # or change this manually

# -----------------------------------

print("\nStarting ESP32 Simulator...\n")

while True:
    mode = random.choice(["relaxed", "stress"]) # if want random, only change this
    print(f"\nCurrent Mode: {mode.upper()}")

    # RELAXED MODE
    if mode == "relaxed":

        sensor_data = {

            "device_id": device_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "mean_eda": round(random.uniform(0.4, 0.9), 2),
            "std_eda": round(random.uniform(0.03, 0.10), 2),
            "eda_slope": round(random.uniform(0.01, 0.04), 2),

            "mean_acc": round(random.uniform(0.05, 0.25), 2),
            "var_acc": round(random.uniform(0.005, 0.02), 2),

            "heart_rate": random.randint(60, 80),

            "hrv": round(random.uniform(0.20, 0.45), 2)
        }

    # STRESS MODE
    elif mode == "stress":

        sensor_data = {

            "device_id": device_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "mean_eda": round(random.uniform(1.2, 2.5), 2),
            "std_eda": round(random.uniform(0.15, 0.40), 2),
            "eda_slope": round(random.uniform(0.05, 0.15), 2),

            "mean_acc": round(random.uniform(0.30, 0.80), 2),
            "var_acc": round(random.uniform(0.03, 0.08), 2),

            "heart_rate": random.randint(95, 130),

            "hrv": round(random.uniform(0.01, 0.10), 2)
        }

    try:

        # Send request to Flask
        response = requests.post(url, json=sensor_data)

        # Get response
        result = response.json()

        print("========================================")
        print("MODE:", mode.upper())

        print("Device ID:", sensor_data["device_id"])
        print("Timestamp:", sensor_data["timestamp"])

        print("\nSensor Features:")
        print(sensor_data)

        print("\nPrediction Result:")
        print("Status:", result["label"])
        print("Stress Probability:",
              round(result["stress_probability"], 2))

        print("========================================\n")

    except Exception as e:
        print("Connection Error:", e)

    # Wait before next transmission
    time.sleep(3)