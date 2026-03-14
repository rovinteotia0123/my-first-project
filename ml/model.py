import pandas as pd
from sklearn.linear_model import LinearRegression

# load dataset
data = pd.read_csv("ml/cloud_cost.csv")

# use columns (monthly dataset works like this)
X = data[['UsageQuantity']]
y = data['Cost']

model = LinearRegression()
model.fit(X, y)

def predict_cost(new_cost):

    if new_cost <= 0:
        return 0

    prediction = model.predict([[new_cost]])

    return float(prediction[0])
