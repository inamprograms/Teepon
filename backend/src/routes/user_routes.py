from flask import Blueprint, request
from src.database.db import connect

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/get_role', methods=['GET', 'POST'])
def get_role():
    db = connect().Main.users
    req = request.get_json()
    uid = req['uid']
    result = db.find({ "user_id": uid })[0]
    return {
        'role': result['role']
    }
   

