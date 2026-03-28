import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# FIXED PATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "ml", "cloud_cost.csv")

data = pd.read_csv(file_path)

X = data[['total_net_cost']]
y = data['total_projected_monthly_cost']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

def predict_cost(new_cost):
    input_df = pd.DataFrame([[new_cost]], columns=['total_net_cost'])
    prediction = model.predict(input_df)[0]

    # 🎯 Add realistic variation
    import random

    variation = random.uniform(-0.08, 0.12)  # -8% to +12%
    adjusted_prediction = prediction + (new_cost * variation)

    return float(adjusted_prediction)