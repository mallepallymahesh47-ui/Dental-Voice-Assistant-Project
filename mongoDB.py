from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["Dental_clinic"]

appointments_collection = db["appointments"]
doctors_collection = db["Doctors"]