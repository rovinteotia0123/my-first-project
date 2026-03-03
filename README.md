Autonomous Cloud Cost Intelligence

This project is developed to predict future cloud cost using Machine Learning and display the results in a dashboard format.

The system takes current cloud cost as input and predicts next month’s expected cost using a Linear Regression model. Based on the percentage increase, it also shows the risk level (Stable, Moderate or High).

Project Objective

The main aim of this project is to:

Predict upcoming cloud expenses

Identify possible cost increase

Provide simple optimization suggestions

Display results in a clean dashboard

This helps in better cloud budget planning.

Technologies Used

Python

Flask

Scikit-learn (Linear Regression)

NumPy

HTML, CSS, JavaScript

Chart.js

Azure SDK (for cost management API)

Project Structure
backend/
    app.py
    requirements.txt

frontend/
    index.html

ml/
    model.py
    __init__.py
How It Works

The frontend takes current cost as input.

The request is sent to Flask backend.

The backend uses a trained Linear Regression model.

The model predicts the next cost.

Risk percentage is calculated.

Result is displayed with chart and recommendation.

API Endpoints

Home:

/

Prediction:

/predict/<usage>

Example: http://127.0.0.1:5000/predict/500

How To Run The Project
Install required libraries:

pip install -r backend/requirements.txt

Run backend:

python -m backend.app

Open frontend:
Open frontend/index.html in browser.

Features

Cloud cost prediction

Risk analysis (Stable / Moderate / High)

Interactive chart

Dark mode

Loading animation

Azure API support (with fallback simulation)

Future Improvements

Use real cloud dataset

Deploy on cloud platform

Improve ML model accuracy

Add database for storing past records
