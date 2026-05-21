import requests
import time
import random

# Flask API URL
url = "http://127.0.0.1:5000/predict"

print("Starting real-time stress monitoring...\n")

while True:

    # Simulated wearable sensor features
    data = {
        "mean_eda": round(random.uniform(0.5, 1.2), 2),
        "std_eda": round(random.uniform(0.05, 0.2), 2),
        "eda_slope": round(random.uniform(0.01, 0.08), 2),
        "mean_acc": round(random.uniform(0.1, 0.5), 2),
        "var_acc": round(random.uniform(0.01, 0.05), 2),
        "heart_rate": random.randint(65, 110),
        "hrv": round(random.uniform(0.1, 0.4), 2)
    }

    try:
        # Send POST request
        response = requests.post(url, json=data)

        # Convert response to JSON
        result = response.json()

        # Display output
        print("Sensor Data:", data)
        print("Prediction:", result["label"])
        print("Stress Probability:", round(result["stress_probability"], 2))
        print("-" * 50)

    except Exception as e:
        print("Error:", e)

    # Wait 2 seconds
    time.sleep(2)