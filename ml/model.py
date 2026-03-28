import pandas as pd
import os
from sklearn.linear_model import LinearRegression

# correct path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "ml", "cloud_cost.csv")

data = pd.read_csv(file_path)

# use multiple features (better prediction)
X = data[['total_net_cost', 'total_on_demand_cost', 'total_amortized_cost']]
y = data['total_projected_monthly_cost']

model = LinearRegression()
model.fit(X, y)

def predict_cost(new_cost):
    # use same value across features (simple but stable)
    input_df = pd.DataFrame([[new_cost, new_cost, new_cost]],
        columns=['total_net_cost', 'total_on_demand_cost', 'total_amortized_cost'])

    prediction = model.predict(input_df)[0]

    # 🔥 control unrealistic spike
    prediction = min(prediction, new_cost * 1.5)

    return float(prediction)