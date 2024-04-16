from flask import Flask, render_template, request
from joblib import load
import numpy as np
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Corrected model path to point to the correct directory
model_path = '/workspaces/ML-web-app-using-Flask/models/final_rf_model.joblib'
model = load(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    feature_values = [float(x) for x in request.form.values()]
    features = np.array([feature_values])
    prediction = model.predict(features)[0]
    return render_template('result.html', prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
