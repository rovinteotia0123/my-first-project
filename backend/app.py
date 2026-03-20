import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

from ml.model import predict_cost
from database import init_db, save_cost, get_history

# setup
load_dotenv()
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# init DB
init_db()

# dummy user
users = {"admin": "1234"}

@app.route("/")
def home():
    return "Backend Running"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if users.get(data.get("username")) == data.get("password"):
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401

@app.route("/cost")
def get_cost():
    try:
        amount = 3500  # simulated (replace with Azure if needed)
        predicted = predict_cost(amount)

        # recommendation logic
        if amount > 5000:
            rec = "High cost detected. Reduce unused resources."
        elif amount > 2000:
            rec = "Moderate usage. Monitor closely."
        else:
            rec = "Cost is optimized."

        save_cost(amount, predicted)

        return jsonify({
            "current_cost": amount,
            "predicted_cost": round(predicted, 2),
            "recommendation": rec
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict/<int:usage>")
def predict_usage(usage):
    if usage <= 0:
        return jsonify({"error": "Invalid input"}), 400

    predicted = predict_cost(usage)
    save_cost(usage, predicted)

    return jsonify({
        "current_cost": usage,
        "predicted_cost": round(predicted, 2),
        "recommendation": "Optimize resources"
    })

@app.route("/history")
def history():
    return jsonify(get_history())

@app.route("/health")
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(debug=True)