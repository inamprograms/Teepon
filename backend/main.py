from pymongo.mongo_client import MongoClient
from flask import Flask, request, jsonify
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
    """
    Function to connect to the MongoDB cluster.
    """
    uri = os.getenv('connection_uri')
    if not uri:
        raise Exception("No MongoDB connection URL found in environment variables")

    # Create a new client and connect to the server
    client = MongoClient(uri)

    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e

    return client


app = Flask(__name__)


@app.route('/api/get_role', methods=['GET', 'POST'])
def get_role():
    client = None
    try:
        client = connect()
        db = client.Main.users
        req = request.get_json()
        if not req or 'uid' not in req:
            return jsonify({"error": "Invalid request payload"}), 400

        uid = req['uid']
        result = db.find_one({"user_id": uid})
        if not result:
            return jsonify({"error": "User not found"}), 404

        return jsonify({'role': result['role']}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500
    finally:
        if client:
            client.close()


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
