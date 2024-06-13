import os 
from dotenv import load_dotenv

load_dotenv()

envs = {
    'uri': os.getenv('connection_uri')
}