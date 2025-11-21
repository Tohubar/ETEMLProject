import os  
from datetime import date 
import dotenv
dotenv.load_dotenv()

DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "visa_data"
MONGODB_URL_KEY = os.getenv("MONGODB_URL")

PIPLINE_NAME = "usvisa"
ARTIFACT_DIR = "artifact"
MODEL_NAME = "model.pkl"

TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"

DATA_FILE_NAME = "usvisa.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
SCHEMA_FILE_NAME = os.path.join('config', 'schema.yaml')

"""
Data Ingestion related constant start with DATA_INGESTION  VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"


