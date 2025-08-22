import os
import sys
from src.DIAP.logger import logging
from src.DIAP.exception import CustomException
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# for reading sql data
from src.DIAP.utils import read_sql_data

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts','train.csv')
    test_data_path:str = os.path.join('artifacts','test.csv')
    raw_data_path:str = os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            # reading from mysql
            df=read_sql_data()
            # df=pd.read_csv(r'data\raw\diabetes.csv')
            logging.info('Reading completed mysql database')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            train_set,test_set=train_test_split(df,test_size=0.2,random_state=True)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info('Data Ingestion is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
if __name__ == "__main":
    obj = DataIngestion()
    obj.initiate_data_ingestion()

# # app.py
# from src.CCDP.logger import logging
# from src.CCDP.exception import CustomException
# from src.CCDP.components.data_ingestion import DataIngestion
# from src.CCDP.components.data_ingestion import DataIngestionConfig
# from src.CCDP.components.data_transformation import DataTransformation
# from src.CCDP.components.data_transformation import DataTransformationConfig
# from src.CCDP.components.model_tranier import ModelTrainerConfig
# from src.CCDP.components.model_tranier import ModelTrainer

# import sys

# if __name__ == "__main__":
#     logging.info("The execution has started")

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