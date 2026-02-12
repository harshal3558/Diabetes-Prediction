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

    try:
        # 🔥 Convert form inputs to correct numeric types
        data = CustomData(
            pregnancies=int(request.form.get("pregnancies")),
            glucose=int(request.form.get("glucose")),
            blood_pressure=int(request.form.get("blood_pressure")),
            skin_thickness=int(request.form.get("skin_thickness")),
            insulin=int(request.form.get("insulin")),
            bmi=float(request.form.get("bmi")),
            diabetes_pedigree_function=float(request.form.get("diabetes_pedigree_function")),
            age=int(request.form.get("age")),
        )

        pred_df = data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(pred_df)

        # Return only result HTML for iframe
        if result[0] == 1:
            return "<span style='color:red;'>Diabetes Positive</span>"
        else:
            return "<span style='color:green;'>Diabetes Negative</span>"

    except Exception as e:
        print("Prediction Error:", str(e))
        return f"<span style='color:red;'>Error: {str(e)}</span>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
