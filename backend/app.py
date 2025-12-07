from flask import Flask, jsonify, send_from_directory, request
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
import os
import joblib

app = Flask(__name__, static_folder="../static")

# ==== File locations ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "../model_files/dnn_cicids2017_model.h5")
scaler_path = os.path.join(BASE_DIR, "../model_files/scaler.gz")
label_path = os.path.join(BASE_DIR, "../model_files/label_mapping.pkl")
data_path = os.path.join(BASE_DIR, "../data/samples.xlsx")

# ==== Load ML Components ====
print("🔄 Loading model...")
model = tf.keras.models.load_model(model_path)

print("🔄 Loading scaler...")
scaler = joblib.load(scaler_path)

print("🔄 Loading label mapping...")
with open(label_path, "rb") as f:
    original_map = pickle.load(f)

# Reverse original dict: {label → id} → {id → label}
label_map = {v: k for k, v in original_map.items()}
print("✔ Label map loaded:", label_map)

# ==== Load samples with OneDrive safety ====
print("🔄 Loading samples...")

# Copy the file to temporary CSV to avoid OneDrive lock issues
temp_csv = os.path.join(BASE_DIR, "../data/samples_temp.csv")

try:
    df_xlsx = pd.read_excel(data_path)
    df_xlsx.to_csv(temp_csv, index=False)
    df = pd.read_csv(temp_csv)
    os.remove(temp_csv)
except PermissionError:
    print("⚠ Excel locked by OneDrive. Attempting to load without copying...")
    df = pd.read_excel(data_path)

df = df.select_dtypes(include=[np.number]).dropna()
print(f"📌 Loaded {len(df)} numeric samples.")

# Store last result for Victim to read
latest_result = {"prediction": "Waiting...", "class_id": -1, "idx": None}


@app.route("/send-sample", methods=["POST"])
def send_sample():
    global latest_result

    data = request.get_json()
    idx = int(data.get("idx", 0))

    if idx < 0 or idx >= len(df):
        return jsonify({"error": "Invalid sample index"}), 400

    # Select sample row
    row = df.iloc[idx]
    X = row.values.reshape(1, -1)
    X_scaled = scaler.transform(X)

    # Predict
    pred = model.predict(X_scaled)
    pred_class = int(np.argmax(pred, axis=1)[0])
    prediction = label_map.get(pred_class, "Unknown")

    # Save result for victim to fetch
    latest_result = {
        "packet": row.to_dict(),
        "prediction": prediction,
        "class_id": pred_class,
        "idx": idx,
        "confidence": float(np.max(pred)),
    }

    return jsonify(latest_result)


@app.route("/get-result", methods=["GET"])
def get_result():
    """Victim fetches latest ML prediction output"""
    return jsonify(latest_result)


@app.route("/")
def serve_victim():
    return send_from_directory("../static", "victim.html")


@app.route("/attacker")
def serve_attacker():
    return send_from_directory("../static", "attacker.html")


if __name__ == "__main__":
    print("🚀 Server running: http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=True)
