from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np

# Custom modules
from src.DIAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Welcome to Diabetes Prediction System"

@app.route("/indexing")
def index():
    return render_template("index.html")

# This endpoint both serves the form (GET) and processes the prediction (POST)
@app.route("/predictdata", methods=["GET", "POST"]) 
def predict_datapoint():
    if request.method == "GET":
        # Render the form page
        return render_template("home.html")
    try:
        # Convert form inputs to appropriate Python types with safe casting
        def safe_int(val):
            return int(float(val)) if val is not None and val != "" else 0
        def safe_float(val):
            return float(val) if val is not None and val != "" else 0.0
        data = CustomData(
            pregnancies=safe_int(request.form.get("pregnancies")),
            glucose=safe_int(request.form.get("glucose")),
            blood_pressure=safe_int(request.form.get("blood_pressure")),
            skin_thickness=safe_int(request.form.get("skin_thickness")),
            insulin=safe_int(request.form.get("insulin")),
            bmi=safe_float(request.form.get("bmi")),
            diabetes_pedigree_function=safe_float(request.form.get("diabetes_pedigree_function")),
            age=safe_int(request.form.get("age")),
        )
        # Prepare DataFrame for the model
        pred_df = data.get_data_as_data_frame()
        # Run prediction
        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)
        # Build a friendly response
        if result[0] == 1:
            label = "Diabetes Positive"
            colour = "red"
        else:
            label = "Diabetes Negative"
            colour = "green"
        # Return JSON – the front‑end JavaScript will consume this
        return jsonify({"label": label, "colour": colour})
    except Exception as e:
        # Log the error server‑side and send a JSON error payload
        print("Prediction Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run on all interfaces for easy testing
    app.run(host="0.0.0.0", port=5000, debug=True)
