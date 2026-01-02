from flask import Flask, request, render_template
import pandas as pd
import numpy as np

from src.DIAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Welcome to Diabetes Prediction System"

@app.route("/indexing")
def index():
    return render_template("index.html")

@app.route("/predictdata", methods=["GET", "POST"])
def predict_datapoint():

    # Load form page
    if request.method == "GET":
        return render_template("home.html")

    # Handle prediction (iframe POST)
    data = CustomData(
        pregnancies=request.form.get("pregnancies"),
        glucose=request.form.get("glucose"),
        blood_pressure=request.form.get("blood_pressure"),
        skin_thickness=request.form.get("skin_thickness"),
        insulin=request.form.get("insulin"),
        bmi=request.form.get("bmi"),
        diabetes_pedigree_function=request.form.get("diabetes_pedigree_function"),
        age=request.form.get("age"),
    )

    pred_df = data.get_data_as_data_frame()
    predict_pipeline = PredictPipeline()
    result = predict_pipeline.predict(pred_df)

    # Return only result HTML for iframe
    if result[0] == 1:
        return "<span style='color:red;'>Diabetes Positive</span>"
    else:
        return "<span style='color:green;'>Diabetes Negative</span>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
