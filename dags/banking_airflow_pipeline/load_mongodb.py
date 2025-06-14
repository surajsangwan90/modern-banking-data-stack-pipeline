from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
# Load environment variables from .env file
load_dotenv()
# Connect to MongoDB using environment variables
host=os.getenv('mongo_host')
port=int(os.getenv('mongo_port', 27017))  # Default port is 27017
client= MongoClient(host,port)


db=os.getenv('mongo_db') # Database name from environment variable
audit_collection=os.getenv('audit_mongo_collection') 
signin_collection=os.getenv('signin_mongo_collection')
db = client[db]  # Access the specified database
audit_collection = db[audit_collection]  # Access the audit collection
signin_collection = db[signin_collection]  # Access the signin collection

def load_data_into_mongodb():
    """
    Load data from JSON files into MongoDB collections.
    """
    # Load JSON data from local files
    local_path = os.getenv('host_path_local')  # Path to the local directory containing JSON files
    # local_path = os.getenv('host_local_path')  # Path to the local directory containing JSON file
    folders = [f for f in os.listdir(local_path) 
           if os.path.isdir(os.path.join(local_path, f)) and f.startswith("run_")]
    latest_folder = sorted(folders)[-1]
    LATEST_PATH = os.path.join(local_path, latest_folder)
    with open(os.path.join(LATEST_PATH , 'audit_logs.json')) as file:
        audit_data = json.load(file)
    with open(os.path.join(LATEST_PATH , 'signin_logs.json')) as file:
        signin_data = json.load(file)
    
    # Insert data into MongoDB collections
    audit_collection.insert_many(audit_data)
    signin_collection.insert_many(signin_data)
    print(f"Audit Collection Count: {audit_collection.count_documents({})}")
    print(f"Signin Collection Count: {signin_collection.count_documents({})}")
    return " Data loaded into MongoDB successfully."

