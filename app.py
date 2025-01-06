from flask import Flask, request, render_template
from pickle import load
import os

# Define the Flask app
app = Flask(__name__)

# Get the absolute path to the model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model/pass_or_fail_decision_tree_classifier_random_42.sav")

# Load the model with error handling
try:
    model = load(open(model_path, "rb"))
    print(f"Model loaded successfully from {model_path}")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}")
    exit(1)

# Define class labels
class_dict = {
    '0': 'Fail',
    '1': 'Pass'
}

# Define the main route for GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Numeric inputs
            val1 = float(request.form["val1"])
            val2 = float(request.form["val2"])
            val3 = float(request.form["val3"])
            val4 = float(request.form["val4"])
            
            # Dropdown inputs for Parental Involvement
            parental_involvement = request.form["parental_involvement"]
            if parental_involvement == "high":
                val5, val6, val7 = 1, 0, 0
            elif parental_involvement == "medium":
                val5, val6, val7 = 0, 0, 1
            elif parental_involvement == "low":
                val5, val6, val7 = 0, 1, 0
            
            # Dropdown inputs for Access to Resources
            resources = request.form["resources"]
            if resources == "high":
                val8, val9, val10 = 1, 0, 0
            elif resources == "medium":
                val8, val9, val10 = 0, 0, 1
            elif resources == "low":
                val8, val9, val10 = 0, 1, 0
            
            # Prepare data for prediction
            data = [[val1, val2, val3, val4, val5, val6, val7, val8, val9, val10]]
            prediction = str(model.predict(data)[0])
            pred_class = class_dict[prediction]
        except Exception as e:
            pred_class = f"Error in prediction: {str(e)}"
    else:
        # Handle initial GET request
        pred_class = None

    # Render the template with the prediction result (or None if GET request)
    return render_template("index.html", prediction=pred_class)


if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Set host to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)
