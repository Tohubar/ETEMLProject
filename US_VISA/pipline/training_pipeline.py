import sys 
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging
from US_VISA.components.data_ingestion import DataIngestion
from US_VISA.components.data_validation import DataValidation

from US_VISA.entity.config_entity import DataIngestionConfig, DataValidationConfig

from US_VISA.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class TrainingPipline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validatin_config = DataValidationConfig()

    def start_data_ingestion(self):
        try:
            logging.info("Initaiting Data Ingestion Pipline")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got the train set and test set of data. exciting ingestion pipline!!!!")

            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info("Staring Data Validatin Pipline")
            data_validation = DataValidation(data_validation_config= self.data_validatin_config, data_ingestion_artifact= data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("data validation artifact gotted")
            logging.info("Exiting Data validatin pipline")
            return data_validation_artifact
        
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def run_pipline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact= data_ingestion_artifact)
        except Exception as e:
            raise UsVisaException(e, sys)