import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGO_DB_CONNECTION_URL"))
db = client[os.getenv("MONGO_DB_NAME")]
results_collection = db["email_results"]