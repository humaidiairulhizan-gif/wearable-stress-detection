import requests

# Flask API URL
url = "http://127.0.0.1:5000/predict"

# Sample feature data
data = {
    "mean_eda": 0.82,
    "std_eda": 0.11,
    "eda_slope": 0.03,
    "mean_acc": 0.22,
    "var_acc": 0.01,
    "heart_rate": 84,
    "hrv": 0.19
}

# Send POST request
response = requests.post(url, json=data)

# Print response
print("Status Code:", response.status_code)
print("Prediction Result:")
print(response.json())