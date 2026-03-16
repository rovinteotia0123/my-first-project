import pandas as pd
from sklearn.linear_model import LinearRegression

# load dataset
data = pd.read_csv("ml/cloud_cost.csv")

# use dataset columns
X = data[['total_net_cost']]
y = data['total_projected_monthly_cost']

model = LinearRegression()
model.fit(X, y)

def predict_cost(new_cost):
    prediction = model.predict([[new_cost]])
    return float(prediction[0])