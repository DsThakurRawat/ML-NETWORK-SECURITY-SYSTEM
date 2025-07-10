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

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
db = client["test"]