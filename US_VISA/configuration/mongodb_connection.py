import sys
from US_VISA.exception import UsVisaException
from US_VISA.logger import logging
from US_VISA.constants import MONGODB_URL_KEY, DATABASE_NAME
import certifi

import pymongo

class MongodbClient:
    client = None 
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:

            if MongodbClient.client == None:
                mongo_url = MONGODB_URL_KEY
                if mongo_url == None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set")
                MongodbClient.client = pymongo.MongoClient(mongo_url, tlsCAFile = certifi.where())
            self.client = MongodbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection is successful")
        except Exception as e:
            raise UsVisaException(e, sys)
    
    def get_client(self):
        return self.client
    def get_database(self):
        return self.database
    def get_collection(self, collection_name: str):
        return self.database[collection_name]