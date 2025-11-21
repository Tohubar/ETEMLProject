import os, sys, json
from US_VISA.logger import logging
from US_VISA.exception import UsVisaException
from US_VISA.entity.config_entity import DataValidationConfig
from US_VISA.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from evidently.dashboard import Dashboard
from evidently.tabs  import DataDriftTab
from evidently.profile_sections import DataDriftProfileSection
from evidently.model_profile  import Profile
from US_VISA.utils.main_utils import read_yaml, write_yaml
from US_VISA.constants import SCHEMA_FILE_NAME
from pandas import DataFrame
import pandas as pd 
import numpy as np

if not hasattr(np, "float_"):
    np.float_ = np.float64
if not hasattr(np, "int_"):
    np.int_ = np.int64



class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self._schema_config = read_yaml(SCHEMA_FILE_NAME)

    def validate_number_of_columns(self, df: DataFrame) -> bool:
        try:
            # status = len(df.columns.to_list()) == len(self._schema_config['columns'])
            # logging.info(f"Is required columns exist: {status}")

            actual_columns = len(df.columns.to_list())
            expected_columns = len(self._schema_config['columns'])
            status = actual_columns == expected_columns
            
            logging.info(f"Expected columns: {expected_columns}")
            logging.info(f"Actual columns: {actual_columns}")
            logging.info(f"Actual column names: {df.columns.to_list()}")
            logging.info(f"Expected column names: {self._schema_config['columns']}")
            logging.info(f"Is required columns exist: {status}")

            return status
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_cols = []
            missing_categorical_cols = []
            for col in self._schema_config["numerical_columns"]:
                if col not in dataframe_columns:
                    missing_numerical_cols.append(col)
            if len(missing_numerical_cols) > 0:
                logging.info(f"Missing numerical Columns: {missing_numerical_cols}")

            for col in self._schema_config["categorical_columns"]:
                if col not in dataframe_columns:
                    missing_categorical_cols.append(col)
            if len(missing_categorical_cols) > 0:
                logging.info(f"Missing numerical Columns: {missing_categorical_cols}")

            return False if len(missing_categorical_cols) > 0 or len(missing_numerical_cols) > 0 else True
            
        except Exception as e:
            raise UsVisaException(e, sys)

    def detect_dataset_drift(self, ref_df: DataFrame, cur_df: DataFrame) -> bool:
        try:

            data_drift_profile = Profile(sections= [DataDriftProfileSection()])
            data_drift_profile.calculate(ref_df, cur_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)
            write_yaml(filepath= self.data_validation_config.data_drift_report_file_path, content= json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift occured")
            status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"] 
            return status 
        except Exception as e:
            raise UsVisaException(e, sys)
        
    def initiate_data_validation(self):
        try:
            validation_error_msg = []
            logging.info("Starting Data Validation process")
            train_df = pd.read_csv(self.data_ingestion_artifact.trained_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            status = self.validate_number_of_columns(df= train_df)
            logging.info(f"All columns are available in the training set: {status}")
            if not status:
                validation_error_msg.append("Columns are missing in Training Dataset")

            status = self.validate_number_of_columns(df= test_df)
            logging.info(f"All columns are available in the testing set: {status}")
            if not status:
                validation_error_msg.append("Columns are missing in Testing Dataset")

            status = self.is_column_exist(df= train_df)
            if not status:
                validation_error_msg.append("Columns are missing in Training Dataset")

            status = self.is_column_exist(df= test_df)
            if not status:
                validation_error_msg.append("Columns are missing in Testomg Dataset")

            validation_status = len(validation_error_msg) == 0
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    validation_error_msg.append("Data Drift Detected")
                else:
                    validation_error_msg.append("Data Drift not Detected")
            else:
                logging.info(f"Validation errors: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status= validation_status,
                message= validation_error_msg,
                drift_report_file_path= self.data_validation_config.data_drift_report_file_path
            )
            logging.info(f"Data Validation Artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise UsVisaException(e, sys)
        
    
        
    