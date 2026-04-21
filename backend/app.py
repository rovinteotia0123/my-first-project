import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

from ml.model import predict_cost
from database import init_db, save_cost, get_history

load_dotenv()

app = Flask(__name__)
CORS(app)

init_db()

# simple login
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
        amount = 3000  # realistic base value

        predicted = predict_cost(amount)

        # better recommendation
        if predicted > amount * 1.2:
            rec = "High cost increase expected. Reduce unused resources."
        elif predicted > amount * 1.05:
            rec = "Moderate increase. Monitor usage."
        else:
            rec = "Cost is stable."

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
        "recommendation": "Optimize resources based on usage"
    })


@app.route("/history")
def history():
    return jsonify(get_history())


@app.route("/health")
def health():
    return jsonify({"status": "running"})


if __name__ == "__main__":
    app.run(debug=True)