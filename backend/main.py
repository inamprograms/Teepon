from flask import Flask, request, flash
import numpy as np
from datetime import datetime
from pymongo.mongo_client import MongoClient
import pymongo
from __init__ import envs
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

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
    except Exception as e:
        print(e)
    db = client
    return db

@app.route('/api/get_role', methods=['GET', 'POST'])
def getRole():
    db = connect().Main.users
    req = request.get_json()
    uid = req['uid']
    result = db.find({ "user_id": uid })[0]
    return {
        'role': result['role']
    }


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')