import pandas as pd
import os
import random

from sklearn.linear_model import LinearRegression


# ------------------ LOAD DATASET ------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, "ml", "cloud_cost.csv")

data = pd.read_csv(file_path)


# ------------------ FEATURES ------------------

X = data[
    [
        'total_net_cost',
        'total_on_demand_cost',
        'total_amortized_cost'
    ]
]

y = data['total_projected_monthly_cost']


# ------------------ TRAIN MODEL ------------------

model = LinearRegression()

model.fit(X, y)


# ------------------ PREDICT FUNCTION ------------------

def predict_cost(new_cost):

    # use same value across features
    input_df = pd.DataFrame(
        [[new_cost, new_cost, new_cost]],
        columns=[
            'total_net_cost',
            'total_on_demand_cost',
            'total_amortized_cost'
        ]
    )

    prediction = model.predict(input_df)[0]

    # small realistic fluctuation
    variation = random.uniform(0.95, 1.10)

    prediction = prediction * variation

    # prevent unrealistic spikes
    prediction = min(prediction, new_cost * 1.5)

    # prevent negative prediction
    prediction = max(prediction, new_cost * 0.9)

    return round(float(prediction), 2)