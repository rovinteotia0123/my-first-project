from flask import Flask, jsonify
from flask_cors import CORS
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from ml.model import predict_cost
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Autonomous Cloud Cost Intelligence Backend Running"


@app.route("/cost")
def get_cost():

    print("Azure cost fetch attempted")   # 👈 WRITE HERE

    try:
        # -------- AZURE COST FETCH LOGIC --------
        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )

        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        cost_client = CostManagementClient(credential)

        query = {
            "type": "ActualCost",
            "timeframe": "MonthToDate",
            "dataset": {
                "granularity": "None",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                }
            }
        }

        scope = f"/subscriptions/{subscription_id}"
        result = cost_client.query.usage(scope, query)

        amount = result.rows[0][0]

        return jsonify({
            "current_cost": round(amount, 2),
            "predicted_cost": round(predict_cost(amount), 2),
            "recommendation": "Monitor high usage resources to reduce cost"
        })

    except Exception:
    simulated_cost = 3500

    return jsonify({
        "current_cost": simulated_cost,
        "predicted_cost": round(predict_cost(simulated_cost), 2),
        "recommendation": "Azure unavailable. Using simulated data for prediction."
    })


@app.route("/auth-test")
def auth_test():
    try:
        credential = ClientSecretCredential(
            tenant_id=os.getenv("AZURE_TENANT_ID"),
            client_id=os.getenv("AZURE_CLIENT_ID"),
            client_secret=os.getenv("AZURE_CLIENT_SECRET")
        )

        credential.get_token("https://management.azure.com/.default")
        return jsonify({"status": "Azure Authentication Successful"})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/predict/<int:usage>")
def predict_usage(usage):

    # validation added
    if usage <= 0:
        return jsonify({"error": "Invalid input value"})

    predicted = predict_cost(usage)

    print("Prediction executed for:", usage)  # logging added

    return jsonify({
        "current_cost": usage,
        "predicted_cost": round(predicted, 2),
        "Optimize resources and monitor unused services"
    })


if __name__ == "__main__":
    app.run(debug=True)
