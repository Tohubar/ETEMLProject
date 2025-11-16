import sys 
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging
from US_VISA.components.data_ingestion import DataIngestion

from US_VISA.entity.config_entity import DataIngestionConfig

from US_VISA.entity.artifact_entity import DataIngestionArtifact


class TrainingPipline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self):
        try:
            logging.info("Initaiting Data Ingestion Pipline")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train set and test set of data. exciting ingestion pipline!!!!")

            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def run_pipline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise UsVisaException(e, sys)