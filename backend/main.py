from pymongo.mongo_client import MongoClient
from flask import Flask, request, flash
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from PIL import Image

import numpy as np
import requests
import base64
import json
import os

load_dotenv()


def connect():
    global db, client
    """
    code for connecting to the cluster
    """
    uri = os.getenv('connection_url')

    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    db = client
    return db

app = Flask(__name__)
connect()

@app.route('/api/get_role', methods=['GET', 'POST'])
def getRole():
    db = connect().Main.users
    print(db)
    req = request.get_json()
    uid = req['uid']
    result = db.find({ "userid": uid })
    result = result[0]
    return {
        'role': result['role']
    }

if __name__ == '__main__':
    connect()
    app.run(debug=False, port=5000, host='0.0.0.0')

