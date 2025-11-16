import os, sys
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging
from US_VISA.configuration.mongodb_connection import MongodbClient
from US_VISA.constants import COLLECTION_NAME, DATABASE_NAME
import pandas as pd
import numpy as np



class FetchMongoDbData:
    def __init__(self):
        try:
            mongodb_client = MongodbClient(database_name= DATABASE_NAME)
            self.database = mongodb_client.get_database()
        except Exception as e:
            raise UsVisaException(e, sys)
    def get_collection_as_dataframe(self, collection_name) -> pd.DataFrame:
        try:
            collection = self.database[collection_name]
            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df.drop('_id', inplace= True, axis= 1)
            df.replace({'na': np.nan}, inplace= True)
            logging.info("Collections are exorted as DataFrame")
            return df
    
        except Exception as e:
            raise UsVisaException(e, sys)