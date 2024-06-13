from pymongo import MongoClient
from src.config import envs

client = None
db = None

# Function to setup the connection with the database
def connect():
    global client, db
    uri = envs['uri']
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)
        raise e
    db  = client
    return db


