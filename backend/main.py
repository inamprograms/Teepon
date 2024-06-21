from flask import Flask, request, flash
import numpy as np
from datetime import datetime
from pymongo.mongo_client import MongoClient
from __init__ import envs
from io import BytesIO
import base64
from PIL import Image
import json
from bson.objectid import ObjectId
import requests



def connect():
    global db, client
    """
    code for connecting to the cluster
    """
    uri = envs['uri']

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

