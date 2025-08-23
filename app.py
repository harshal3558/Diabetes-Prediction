from src.DIAP.logger import logging
from src.DIAP.exception import CustomException
from src.DIAP.components.data_ingestion import DataIngestion
from src.DIAP.components.data_ingestion import DataIngestionConfig
from src.DIAP.components.data_transformation import DataTransformation
from src.DIAP.components.data_transformation import DataTransformationConfig

import sys

if __name__ == "__main__":
    logging.info("the execution has started")

    try:
        data_ingestion = DataIngestion()
        # data_ingestion = data_ingestion.initiate_data_ingestion()
        train_data_path,test_data_path = data_ingestion.initiate_data_ingestion()


        # data_transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path,test_data_path)


    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)