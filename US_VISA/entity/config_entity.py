import os
from US_VISA.constants import *
from datetime import datetime
from dataclasses import dataclass

TIMESTAMP = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

@dataclass
class TrainingPiplineConfig:
    pipline_name = PIPLINE_NAME
    artifact_dir = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp = TIMESTAMP

training_pipline_config = TrainingPiplineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir = os.path.join(training_pipline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    feature_store_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, DATA_FILE_NAME)
    training_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    testing_file_path = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name = DATA_INGESTION_COLLECTION_NAME


