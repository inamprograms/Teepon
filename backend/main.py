from pymongo.mongo_client import MongoClient
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from PIL import Image
import numpy as np
import requests
import base64
import json
import os
from routes import routes_bp

load_dotenv()


def connect():
    """
    Function to connect to the MongoDB cluster.
    """
    uri = os.getenv('MONGO_URI')
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
client = connect()


# User Routes

@app.route('/api/users', methods=['GET'])
def get_users():
    db = client.test.users
    result = db.find()
    return loads(json.dumps(list(result), default=str))

@app.route('/api/user/add', methods=['POST'])
def add_user():
    db = client.test.users
    req = request.get_json()
    if not req or 'uid' not in req:
        return jsonify({"error": "Invalid request payload"}), 400

    uid = req['uid']
    name = req['name']
    token = req['token']
    
    result = db.find_one({"user_id": uid})
    if result:
        return jsonify({"error": "User already exists"}), 409

    db.insert_one({"user_id": uid, "name" : name, "token" : token})
    return jsonify({"message": "User added successfully"}), 201


# Chat Routes
@app.route('/api/chats', methods=['POST'])
def get_chats():
    db = client.test.chats
    
    req = request.get_json()
    # if not req or 'oid' not in req:
    #     return jsonify({"error": "Invalid request payload"}), 400

    oid = req['oid']
    # token = req['token']
    
    result = db.find({"oid":oid})
    if not result:
        return jsonify({"error": "Chat not found"}), 404
    # if result.token != token:
    #     return jsonify({"error": "Unauthorized access"}), 401
    
    return loads(json.dumps(list(result), default=str))

@app.route('/api/chat/add', methods=['POST'])
def add_chat():
    db = client.test.chats
    req = request.get_json()
    if not req or 'oid' not in req or 'token' not in req or 'message' not in req:
        return jsonify({"error": "Invalid request payload"}), 400

    oid = req['oid']
    token = req['token']
    message = req['message']

    result = db.find_one({"oid": oid})
    
    # if result and result.token != token:
    #     return jsonify({"error": "Unauthorized access"}), 401

    if not result:
        messages = []
        messages.append(message)
        db.insert_one({"oid": oid, "token": token, "messages": messages})
    else:
        result['messages'].append(message)
        db.update_one({"oid": oid}, {"$set": {"messages": result['messages']}})

    return jsonify({"message": "Chat added successfully"}), 201


@app.route('/api/get_role', methods=['GET', 'POST'])
def get_role():
    # client = None
    try:
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
    app.run(debug=True, port=os.getenv('PORT'), host='0.0.0.0')
