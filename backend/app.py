import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from werkzeug.security import generate_password_hash, check_password_hash

from ml.model import predict_cost
from database import (
    init_db,
    save_cost,
    get_history,
    save_user
)

# ------------------ SETUP ------------------
load_dotenv()

app = Flask(__name__)

CORS(app)

logging.basicConfig(level=logging.INFO)

init_db()


# ------------------ AUTH ------------------
users = {
    "hitesh123": generate_password_hash("hitesh123")
}


@app.route("/")
def home():
    return "Backend Running"


# ------------------ NORMAL LOGIN ------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data.get("username")

    password = data.get("password")

    if username in users and check_password_hash(users[username], password):

        return jsonify({
            "status": "success"
        })

    return jsonify({
        "status": "fail"
    }), 401


# ------------------ GOOGLE LOGIN SAVE ------------------
@app.route("/save-user", methods=["POST"])
def save_google_user():

    try:

        data = request.json

        email = data.get("email")

        if not email:

            return jsonify({
                "error": "Email required"
            }), 400

        save_user(email)

        logging.info(f"Google user saved: {email}")

        return jsonify({
            "status": "success"
        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


# ------------------ COST ------------------
@app.route("/cost")
def get_cost():

    try:

        amount = 3000

        predicted = predict_cost(amount)

        # Recommendation logic
        if predicted > amount * 1.2:

            rec = "High cost increase expected. Reduce unused resources."

        elif predicted > amount * 1.05:

            rec = "Moderate increase. Monitor usage."

        else:

            rec = "Cost is stable."

        save_cost(amount, predicted)

        logging.info(f"Cost fetched: {amount}, Predicted: {predicted}")

        return jsonify({
            "current_cost": amount,
            "predicted_cost": round(predicted, 2),
            "recommendation": rec
        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


# ------------------ PREDICT ------------------
@app.route("/predict/<int:usage>")
def predict_usage(usage):

    # Input validation
    if usage <= 0 or usage > 100000:

        return jsonify({
            "error": "Invalid input"
        }), 400

    try:

        predicted = predict_cost(usage)

        save_cost(usage, predicted)

        # Recommendation
        if predicted > usage * 1.2:

            rec = "High cost increase expected. Optimize resources."

        elif predicted > usage * 1.05:

            rec = "Moderate increase. Monitor usage."

        else:

            rec = "Cost is stable."

        logging.info(f"Prediction: {usage} -> {predicted}")

        return jsonify({
            "current_cost": usage,
            "predicted_cost": round(predicted, 2),
            "recommendation": rec
        })

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": str(e)
        }), 500


# ------------------ HISTORY ------------------
@app.route("/history")
def history():

    try:

        return jsonify(get_history())

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "error": "History error"
        }), 500


# ------------------ HEALTH ------------------
@app.route("/health")
def health():

    return jsonify({
        "status": "running"
    })


# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)