from flask import Flask, request, render_template
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from src.DIAP.pipelines.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            pregnancies=request.form.get('pregnancies'),
            glucose=request.form.get('glucose'),
            blood_pressure=request.form.get('blood_pressure'),
            skin_thickness=request.form.get('skin_thickness'),
            insulin=request.form.get('insulin'),
            bmi=request.form.get('bmi'),
            diabetes_pedigree_function=request.form.get('diabetes_pedigree_function'),
            age=request.form.get('age')
        )

        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Model Prediction")
        results=predict_pipeline.predict(pred_df)
        print("After Prediction")
        return render_template("home.html",results=results[0])
        

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)














## app.py

# from src.DIAP.logger import logging
# from src.DIAP.exception import CustomException
# from src.DIAP.components.data_ingestion import DataIngestion
# from src.DIAP.components.data_ingestion import DataIngestionConfig
# from src.DIAP.components.data_transformation import DataTransformation
# from src.DIAP.components.data_transformation import DataTransformationConfig
# from src.DIAP.components.model_tranier import ModelTrainerConfig
# from src.DIAP.components.model_tranier import ModelTrainer

# import sys

# if __name__ == "__main__":
#     logging.info("the execution has started")


#     try:
#         # data_ingestion_config=DataIngestionConfig()
#         data_ingestion=DataIngestion() 
#         # data_ingestion.initiate_data_ingestion()
#         train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()

#         # data_transformation_config=DataIngestionConfig()
#         data_transformation=DataTransformation()
#         # data_transformation.initiate_data_transformation(train_data_path,test_data_path)
#         train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data_path,test_data_path)
        
#         ## Model Training

#         model_trainer=ModelTrainer()
#         print(model_trainer.initiate_model_trainer(train_arr,test_arr))




#     except Exception as e:
#         logging.info("Custom Exception")
#         raise CustomException(e,sys)