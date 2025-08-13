from src.DIAP.logger import logging
from src.DIAP.exception import CustomException
from src.DIAP.components.data_ingestion import DataIngestion
from src.DIAP.components.data_ingestion import DataIngestionConfig

import sys

if __name__ == "__main__":
    logging.info("the execution has started")

    try:
        data_ingestion = DataIngestion()
        data_ingestion = initiate_data_ingestion()
    except Exception as e:
        logging.info("Custom Exception")
        raise CustomException(e,sys)