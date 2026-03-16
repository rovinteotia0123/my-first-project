import pandas as pd
from sklearn.linear_model import LinearRegression

# load dataset
data = pd.read_csv("ml/cloud_cost.csv")

# scale small values better
X = data[['total_net_cost']]
y = data['total_projected_monthly_cost']

model = LinearRegression()
model.fit(X, y)

def predict_cost(new_cost):

    # 👉 adjust small demo inputs
    if new_cost < 500:
        new_cost = new_cost * 5

    prediction = model.predict([[new_cost]])

    return float(prediction[0])