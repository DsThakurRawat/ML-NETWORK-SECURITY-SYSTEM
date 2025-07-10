import os
import sys
import json
import pymongo

from dotenv import load_dotenv

load_dotenv()


MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi

ca = certifi.where() #ca is certificate authority 

import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetwrokSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetwrokSecurityException(e,sys)
    
    def cv_to_json_convertor(self,file_path):
        try:
           data = pd.read_csv(file_path)
           data.reset_index(drop=True,inplace=True)
           records = data.to_dict(orient="records") 
           return records
        except Exception as e:
            raise NetwrokSecurityException(e,sys)
        
    def insert_data_mogodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))

        except Exception as e:
            raise NetwrokSecurityException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "DIVYANSH"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records         =   networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mogodb(records,DATABASE,Collection)
    print(no_of_records)