from flask import Blueprint, jsonify, request
from .extensions import db
from .models import User

def users_blueprint():
    users = Blueprint('users', __name__, url_prefix='/api')

    @users.route('/users', methods=['GET', 'POST'])
    def users_route():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201

        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200

    @users.route('/users/<int:user_id>')
    def user_detail_route(user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    return users
