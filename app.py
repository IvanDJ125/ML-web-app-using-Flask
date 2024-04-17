from flask import Flask, request, render_template
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('/workspaces/ML-web-app-using-Flask/models/final_rf_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Mapping form inputs to model features
    data = {
        'Store_id': request.form['store_id'],
        'Holiday': 1 if request.form['holiday'] == 'Yes' else 0,
        '#Order': request.form['order'],
        'Day_of_Week': request.form['day_of_week'],
        'Month': request.form['month'],
        'Store_Type_S1': 1 if request.form['store_type'] == 'S1' else 0,
        'Store_Type_S2': 1 if request.form['store_type'] == 'S2' else 0,
        'Store_Type_S3': 1 if request.form['store_type'] == 'S3' else 0,
        'Store_Type_S4': 1 if request.form['store_type'] == 'S4' else 0,
        'Location_Type_L1': 1 if request.form['location_type'] == 'L1' else 0,
        'Location_Type_L2': 1 if request.form['location_type'] == 'L2' else 0,
        'Location_Type_L3': 1 if request.form['location_type'] == 'L3' else 0,
        'Location_Type_L4': 1 if request.form['location_type'] == 'L4' else 0,
        'Location_Type_L5': 1 if request.form['location_type'] == 'L5' else 0,
        'Region_Code_R1': 1 if request.form['region_code'] == 'R1' else 0,
        'Region_Code_R2': 1 if request.form['region_code'] == 'R2' else 0,
        'Region_Code_R3': 1 if request.form['region_code'] == 'R3' else 0,
        'Region_Code_R4': 1 if request.form['region_code'] == 'R4' else 0,
        'Discount_No': 1 if request.form['discount'] == 'No' else 0,
        'Discount_Yes': 1 if request.form['discount'] == 'Yes' else 0
    }

    # Convert data into DataFrame for prediction
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text=f'Predicted Store Sales: ${output}')

if __name__ == "__main__":
    app.run(debug=True)