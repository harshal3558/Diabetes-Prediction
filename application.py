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
        # Validation rules and robust inputs parsing
        errors = []
        
        # Helper to get and validate numeric fields
        def get_and_validate(field_name, field_label, is_float=False, min_val=None, max_val=None, allow_zero=True):
            val_str = request.form.get(field_name)
            if val_str is None or val_str.strip() == "":
                errors.append(f"{field_label} is required.")
                return 0 if not is_float else 0.0
            try:
                val = float(val_str) if is_float else int(float(val_str))
                if min_val is not None and val < min_val:
                    if not (allow_zero and val == 0):
                        errors.append(f"{field_label} must be at least {min_val}.")
                if max_val is not None and val > max_val:
                    errors.append(f"{field_label} cannot exceed {max_val}.")
                return val
            except ValueError:
                errors.append(f"{field_label} must be a valid number.")
                return 0 if not is_float else 0.0

        pregnancies = get_and_validate("pregnancies", "Pregnancies", is_float=False, min_val=0, max_val=20)
        glucose = get_and_validate("glucose", "Glucose", is_float=False, min_val=30, max_val=300, allow_zero=True)
        blood_pressure = get_and_validate("blood_pressure", "Blood Pressure", is_float=False, min_val=30, max_val=200, allow_zero=True)
        skin_thickness = get_and_validate("skin_thickness", "Skin Thickness", is_float=False, min_val=2, max_val=100, allow_zero=True)
        insulin = get_and_validate("insulin", "Insulin", is_float=False, min_val=5, max_val=900, allow_zero=True)
        bmi = get_and_validate("bmi", "BMI", is_float=True, min_val=10.0, max_val=70.0, allow_zero=True)
        diabetes_pedigree_function = get_and_validate("diabetes_pedigree_function", "Diabetes Pedigree Function", is_float=True, min_val=0.01, max_val=2.5)
        age = get_and_validate("age", "Age", is_float=False, min_val=1, max_val=120)

        if errors:
            return jsonify({"error": " | ".join(errors)}), 400

        data = CustomData(
            pregnancies=pregnancies,
            glucose=glucose,
            blood_pressure=blood_pressure,
            skin_thickness=skin_thickness,
            insulin=insulin,
            bmi=bmi,
            diabetes_pedigree_function=diabetes_pedigree_function,
            age=age,
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
