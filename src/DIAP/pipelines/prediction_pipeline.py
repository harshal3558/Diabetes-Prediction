import sys
import pandas as pd
from src.DIAP.exception import CustomException
from src.DIAP.utils import load_object
import os


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)



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
