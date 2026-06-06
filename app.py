from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import sqlite3

recent_hr = []
recent_gsr = []
recent_stress = []

# Store latest dashboard data
latest_data = {}

# IMPORTANT:
# Feature order MUST match training order exactly
FEATURE_ORDER = [
    "mean_eda",
    "std_eda",
    "eda_slope",
    "mean_acc",
    "var_acc",
    "heart_rate",
    "hrv"
]

# Initialize Flask app
app = Flask(__name__)

def init_db():

    conn = sqlite3.connect("stress_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stress_records (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        device_id TEXT,

        mean_eda REAL,
        std_eda REAL,
        eda_slope REAL,

        mean_acc REAL,
        var_acc REAL,

        heart_rate REAL,
        hrv REAL,

        prediction INTEGER,
        label TEXT,

        stress_probability REAL,
        nonstress_probability REAL
    )
    """)

    conn.commit()
    conn.close()

# Load trained model
model = joblib.load("stress_model.pkl")

init_db()

# Homepage route
@app.route("/")
def home():
    return "Stress Detection API Running"

# Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        data=latest_data
    )
@app.route("/history")
def history():

    conn = sqlite3.connect("stress_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM stress_records
    ORDER BY id DESC
    LIMIT 20
    """)

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    global latest_data

    try:
        # Get JSON data
        data = request.get_json()
        # Required features
        required_fields = FEATURE_ORDER

        # Check for missing fields
        for field in required_fields:

            if field not in data:

                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        # Extract features in EXACT training order
        features = [data[field] for field in FEATURE_ORDER]

        # Convert to numpy array
        features = np.array(features).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)[0]

        # Prediction probabilities
        probability = model.predict_proba(features)[0]

        stress_probability = float(probability[1])
        nonstress_probability = float(probability[0])

        # Convert label
        if prediction == 1:
            result = "Stress"
        else:
            result = "Non-Stress"

        # Update dashboard data
        latest_data = {
            "device_id": data.get("device_id", "Unknown"),
            "timestamp": data.get("timestamp", "N/A"),

            "heart_rate": data["heart_rate"],
            "hrv": data["hrv"],
            "gsr": data["mean_eda"],

            "label": result,

            "stress_probability": round(stress_probability, 2),
            "nonstress_probability": round(nonstress_probability, 2)
        }

        # Store recent chart data
        recent_hr.append(data["heart_rate"])
        recent_gsr.append(data["mean_eda"])
        recent_stress.append(round(stress_probability, 2))

        # Keep only latest 20 values
        if len(recent_hr) > 20:
            recent_hr.pop(0)

        if len(recent_gsr) > 20:
            recent_gsr.pop(0)

        if len(recent_stress) > 20:
            recent_stress.pop(0)
        

        # Save to database
        conn = sqlite3.connect("stress_data.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO stress_records (

            timestamp,
            device_id,

            mean_eda,
            std_eda,
            eda_slope,

            mean_acc,
            var_acc,

            heart_rate,
            hrv,

            prediction,
            label,

            stress_probability,
            nonstress_probability

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """, (

        data.get("timestamp", "N/A"),
        data.get("device_id", "Unknown"),

        data["mean_eda"],
        data["std_eda"],
        data["eda_slope"],

        data["mean_acc"],
        data["var_acc"],

        data["heart_rate"],
        data["hrv"],

        int(prediction),
        result,

        stress_probability,
        nonstress_probability
        ))

        conn.commit()
        conn.close()

        # Return API response
        return jsonify({
            "prediction": int(prediction),
            "label": result,
            "stress_probability": stress_probability,
            "nonstress_probability": nonstress_probability
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

@app.route("/latest")
def latest():
    return jsonify(latest_data)

@app.route("/recent")
def recent():
    return jsonify({
        "heart_rate_history": recent_hr,
        "gsr_history": recent_gsr,
        "hrv_history": recent_hrv,
        "stress_probability_history": recent_stress
    })

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

