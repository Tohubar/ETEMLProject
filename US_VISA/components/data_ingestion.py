import os, sys 
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging
from US_VISA.data_access.usvisa_data import FetchMongoDbData
from US_VISA.entity.config_entity import DataIngestionConfig
import pandas as pd
from US_VISA.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise UsVisaException(e, sys)
    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            logging.info("Exporting MongoDB Data as dataframe")
            usvisa_data = FetchMongoDbData()
            dataframe = usvisa_data.get_collection_as_dataframe(collection_name= self.data_ingestion_config.collection_name)
            
            logging.info(f"Exported: shape of dataframe {dataframe.shape}")
            feature_store_file = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file), exist_ok= True)

            logging.info(f"Saving exported data into feature store file : {feature_store_file}")
            dataframe.to_csv(feature_store_file, index= False, header= True)

            return dataframe
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Starting spliting dataframe into train and test set")
            split_ration = self.data_ingestion_config.train_test_split_ratio
            train_df, test_df = train_test_split(dataframe, test_size= split_ration)
            
            logging.info("Splited dataframe")
            ingested_dir = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(ingested_dir, exist_ok= True)
            
            logging.info("Saving splited data into train and test file")
            train_df.to_csv(self.data_ingestion_config.training_file_path, index= False, header= True)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index= False, header= True)

            logging.info("Completed tha tastk")
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def initiate_data_ingestion(self):
        logging.info("Initiating Data Ingestion Artifact")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got Exported data as dataframe")
            self.split_data_as_train_test(dataframe=dataframe)

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path= self.data_ingestion_config.training_file_path, test_file_path= self.data_ingestion_config.testing_file_path)
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise UsVisaException(e, sys)