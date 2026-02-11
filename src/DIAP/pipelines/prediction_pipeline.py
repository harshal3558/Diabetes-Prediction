import sys
import os
import pandas as pd
from src.DIAP.exception import CustomException
from src.DIAP.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            # Absolute path inside Docker
            base_path = os.getcwd()

            model_path = os.path.join(base_path, "artifacts", "model.pkl")
            preprocessor_path = os.path.join(base_path, "artifacts", "preprocessor.pkl")

            print("Current Working Directory:", base_path)
            print("Model Path:", model_path)
            print("Preprocessor Path:", preprocessor_path)
            print("Before Loading")

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            print("After Loading")

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)

            return preds

        except Exception as e:
            print("ERROR:", str(e))
            raise CustomException(e, sys)


import pandas as pd
import sys

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
            raise Exception(f"Error creating DataFrame: {e}") from e
