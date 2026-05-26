import sys
import os
import pandas as pd
from src.DIAP.exception import CustomException
from src.DIAP.utils import load_object


class PredictPipeline:
    def __init__(self):
        try:
            # ==============================
            # Find Project Root Dynamically
            # ==============================
            current_path = os.path.abspath(__file__)

            # prediction_pipeline.py
            # -> pipelines
            # -> DIAP
            # -> src
            # -> project root
            project_root = os.path.abspath(
                os.path.join(current_path, "../../../../")
            )

            self.model_path = os.path.join(project_root, "artifacts", "model.pkl")
            self.preprocessor_path = os.path.join(project_root, "artifacts", "preprocessor.pkl")

            print("Project Root:", project_root)
            print("Model Path:", self.model_path)
            print("Preprocessor Path:", self.preprocessor_path)

            # ==============================
            # Check if files exist
            # ==============================
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}")

            if not os.path.exists(self.preprocessor_path):
                raise FileNotFoundError(f"Preprocessor file not found at {self.preprocessor_path}")

            # ==============================
            # Load Model & Preprocessor
            # ==============================
            print("Loading model and preprocessor...")
            self.model = load_object(self.model_path)
            self.preprocessor = load_object(self.preprocessor_path)
            print("Model and Preprocessor Loaded Successfully")

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, features):
        try:
            print("Starting prediction...")

            # Replace zero values with NaN for columns with implausible zero values so they get imputed properly
            import numpy as np
            columns_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
            features[columns_with_zero] = features[columns_with_zero].replace(0, np.nan)

            data_scaled = self.preprocessor.transform(features)
            preds = self.model.predict(data_scaled)

            print("Prediction completed.")
            return preds

        except Exception as e:
            raise CustomException(e, sys)


# ======================================================
# Custom Data Class
# ======================================================

class CustomData:
    def __init__(
        self,
        pregnancies: int,
        glucose: int,
        blood_pressure: int,
        skin_thickness: int,
        insulin: int,
        bmi: float,
        diabetes_pedigree_function: float,
        age: int,
    ):
        self.pregnancies = pregnancies
        self.glucose = glucose
        self.blood_pressure = blood_pressure
        self.skin_thickness = skin_thickness
        self.insulin = insulin
        self.bmi = bmi
        self.diabetes_pedigree_function = diabetes_pedigree_function
        self.age = age

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "Pregnancies": [self.pregnancies],
                "Glucose": [self.glucose],
                "BloodPressure": [self.blood_pressure],
                "SkinThickness": [self.skin_thickness],
                "Insulin": [self.insulin],
                "BMI": [self.bmi],
                "DiabetesPedigreeFunction": [self.diabetes_pedigree_function],
                "Age": [self.age],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
