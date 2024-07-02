from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import desc
from uuid import UUID

from .models import User, Outing, FriendList, \
                    Messages, AiMessages, \
                    Message, AiMessage
from .extensions import db


def users_blueprint():
    users = Blueprint('users', __name__, url_prefix='/api')

    @users.route('/add-user', methods=['POST'])
    def add_user():
        if request.method == 'POST':
            try:
                uid = request.json.get('uid')
                display_name = request.json.get('name')
                email = request.json.get('email')
                refresh_token = request.json.get('refresh_token')
                access_token = request.json.get('access_token')

                user = User.query.filter_by(email = email).first()
                if user:
                    return jsonify({'error': f"User with {email} already exists!"}), 400
                user = User(
                    uid = uid,
                    email=email,
                    display_name = display_name,
                    refresh_token= refresh_token,
                    access_token = access_token
                )
                db.session.add(user)
                db.session.commit()
                return jsonify({'user': user.to_dict()}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
    @users.route('/me', methods=['GET', 'DELETE', 'POST'])
    def me():
        # email = request.args.get('email') if request.method == 'GET' else request.form.get('email')
        email = request.json.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400

        if request.method == 'GET':
            try:
                user = User.query.filter_by(email=email).first()
                if user and user.active:
                    return jsonify({'user': user.to_dict()}), 200
                else:
                    return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        elif request.method == 'POST':
            display_name = request.json.get('display_name')
            refresh_token = request.json.get('refresh_token')
            access_token = request.json.get('access_token')
            try:
                user = User.query.filter_by(email=email).first()
                if user and user.active:
                    if display_name:
                        user.display_name = display_name
                    if refresh_token:
                        user.refresh_token = refresh_token
                    if access_token:
                        user.access_token = access_token
                    db.session.commit()
                    return jsonify({'user': user.to_dict()}), 200
                else:
                    db.session.rollback()
                    return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        elif request.method == 'DELETE':
            try:
                user = User.query.filter_by(email=email).first()
                if user and user.active:
                    friend_list = FriendList.query.filter_by(user_id=user.id).all()
                    for friend in friend_list:
                        db.session.delete(friend)
                        db.session.commit()

                    messages = Message.query.filter_by(send_from=user.id).all()
                    if messages:
                        for message in messages:
                            message_in_group = Messages.query.filter_by(message_id=message.id).first()
                            if message_in_group:
                                db.session.delete(message_in_group)
                                db.session.commit()
                            db.session.delete(message)
                            db.session.commit()

                    ai_messages = AiMessage.query.filter_by(send_from=user.id).all()
                    if ai_messages:
                        for ai_message in ai_messages:
                            ai_message_in_group = AiMessages.query.filter_by(ai_message_id=ai_message.id).first()
                            if ai_message_in_group:
                                db.session.delete(ai_message_in_group)
                                db.session.commit()
                            db.session.delete(ai_message)
                            db.session.commit()

                    user.active = False
                    db.session.commit()
                    return jsonify({'message': 'User deleted'}), 200
                else:
                    return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/add-outing', methods=['POST'])
    def add_outing():
        if request.method == 'POST':
            try:
                name = request.json.get('name')
                latest_location = 'NULL'
                outing_topic = 'NULL'
                user_email = request.json.get('email')
                friend_emails = request.json.get('friend_emails')

                emails = [value for key, value in friend_emails.items()]
                print(emails)

                user = User.query.filter_by(email=user_email).first()
                if not user or user.active == False:
                    return jsonify({'error': 'User not found'}), 404

                outing = Outing.query.filter_by(name=name, creator_id=user.id).first()
                if outing:
                    return jsonify({'error': 'Outing already exists'}), 400

                outing = Outing(
                    name=name,
                    created_at=datetime.utcnow(),
                    latest_location=latest_location,
                    outing_topic=outing_topic,
                    creator_id=user.id
                )
                db.session.add(outing)
                db.session.commit()

                for friend_email in emails:
                    friend = User.query.filter_by(email=friend_email).first()
                    if friend:
                        friend_list_entry = FriendList(
                            outing_id=outing.id,
                            user_id=friend.id
                        )
                        db.session.add(friend_list_entry)
                        db.session.commit()

                return jsonify({'outing': outing.to_dict()}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings', methods=['GET'])
    def get_outings():
        if request.method == 'GET':
            email = request.json.get('email')

            try:
                user = User.query.filter_by(email=email).first()
                if not user or user.active == False:
                    return jsonify({'error': 'User not found'}), 404

                outings = (db.session.query(Outing)
                            .join(FriendList)
                            .filter(Outing.id == FriendList.outing_id)
                            .all())
                outings_list = [{"id" : outing.id, "name" : outing.name} for outing in outings]

                return jsonify({'outings': outings_list}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>', methods=['GET', 'POST', 'DELETE'])
    def get_outing(outing_id):
        def retrieve_outing_data(outing):

            messages = (db.session.query(Message.send_from, Message.content).
                        join(Messages).
                        filter(Messages.messages_group_id == outing.id).all())

            ai_messages = (db.session.query(AiMessage.send_from, AiMessage.content).
                        join(AiMessages).
                        filter(AiMessages.ai_messages_group_id == outing.id).all())

            messages_formatted = [
                {
                    'send_from': User.query.filter_by(id=send_from).first().email,
                    'content': content
                }
                for send_from, content in messages
            ]

            ai_messages_formatted = [
                {
                    'send_from': User.query.filter_by(id=send_from).first().email if send_from else "NULL",
                    'content': content
                }
                for send_from, content in ai_messages
            ]



            outing_data = {
                'name': outing.name,
                'location': outing.latest_location,
                'outing_topic': outing.outing_topic,
                'messages': messages_formatted,
                'ai_messages': ai_messages_formatted
            }
            return outing_data

        if request.method == 'GET':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': 'Outing not found'}), 404

                outing_data = retrieve_outing_data(outing)

                return jsonify({"outing": outing_data}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500


        elif request.method == 'POST':
            try:
                location = request.json.get("location")
                outing_topic = request.json.get("outing_topic")
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': 'Outing not found'}), 404

                outing.latest_location = location
                outing.outing_topic = outing_topic

                db.session.commit()

                # outing = Outing.query.filter_by(id=str(outing_id_str)).first() # to get newest data
                outing_data = retrieve_outing_data(outing)
                return jsonify({"outing": outing_data}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

        elif request.method == 'DELETE':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()

                if not outing:
                    return jsonify({'error': 'Outing not found'}), 404

                FriendList.query.filter_by(outing_id=str(outing_id)).delete()
                db.session.commit()

                db.session.delete(outing)
                db.session.commit()

                return jsonify({'message': 'Outing deleted successfully'}), 200

            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>/get-friends', methods=['GET'])
    def get_friend_list(outing_id):
        if request.method == 'GET':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                friend_list = FriendList.query.filter_by(outing_id=str(outing_id)).all()
                if not friend_list:
                    return jsonify({'message': 'No friend list found for this outing ID'}), 404

                friend_list_data = [User.query.filter_by(id = friend.user_id).first().email for friend in friend_list]
                return jsonify({'friend_list': friend_list_data}), 200

            except Exception as e:
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>/add-friend', methods=['POST'])
    def add_friend(outing_id):
        if request.method == 'POST':
            try:
                email = request.json.get('email')
                if not email:
                    return jsonify({'error': 'Email is required'}), 400

                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                user = User.query.filter_by(email=email).first()
                if not user or user.active == False:
                    return jsonify({'error': f'User with email {email} not found'}), 404

                friend = FriendList.query.filter_by(outing_id=str(outing_id), user_id = user.id).first()
                if friend:
                    return jsonify({'friend_email': email}), 200

                friend = FriendList(
                    outing_id=outing_id,
                    user_id=user.id
                )
                db.session.add(friend)
                db.session.commit()

                return jsonify({'error': f'User with email {email} not found'}), 404
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>/delete-friend', methods=['DELETE'])
    def delete_friend(outing_id):
        if request.method == 'DELETE':
            try:
                email = request.json.get('email')
                if not email:
                    return jsonify({'error': 'Email is required'}), 400

                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                user = User.query.filter_by(email=email).first()
                if not user or user.active == False:
                    return jsonify({'error': f'User with email {email} not found'}), 404

                friend = FriendList.query.filter_by(outing_id=str(outing_id), user_id=user.id).first()
                if friend:
                    db.session.delete(friend)
                    db.session.commit()
                    return jsonify({'message': 'Friend deleted successfully'}), 200
                else:
                    return jsonify({'error': 'Friend relation not found'}), 404
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>/chat', methods=['GET'])
    def get_chat(outing_id):
        if request.method == 'GET':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                messages = (db.session.query(Message.send_from, Message.content)
                            .join(Messages)
                            .filter(Messages.messages_group_id == str(outing_id))
                            .order_by(Message.datetime)
                            .all())
                # messages = sorted(messages, key=lambda msg: msg.datetime)
                formatted_messages = [{'send_from': User.query.filter_by(id = send_from).first().email, 'content': content} for send_from, content in messages]

                return jsonify({'messages': formatted_messages}), 200

            except Exception as e:
                return jsonify({'error': f'Error fetching chat messages: {str(e)}'}), 500

    @users.route('/get-outings/<uuid:outing_id>/ai-chat', methods=['GET'])
    def get_ai_chat(outing_id):
        if request.method == 'GET':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                ai_messages = (db.session.query(AiMessage.send_from, AiMessage.content)
                               .join(AiMessages)
                               .filter(AiMessages.ai_messages_group_id == str(outing_id))
                               .order_by(AiMessage.datetime)
                               .all())
                formatted_messages = [{'send_from': User.query.filter_by(id=send_from).first().email if send_from else "NULL", 'content': content} for send_from, content in
                                      ai_messages]

                return jsonify({'messages': formatted_messages}), 200

            except Exception as e:
                return jsonify({'error': f'Error fetching chat messages: {str(e)}'}), 500

    @users.route('/get-outings/<uuid:outing_id>/chat/send', methods=['POST'])
    def send_message(outing_id):
        get_all_messages = False # change this to false if you need only the latest change

        if request.method == 'POST':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                send_from_email = request.json.get('send_from')
                content = request.json.get('content')

                if not send_from_email or not content:
                    return jsonify({'error': 'Send_from_email and content are required to be correct'}), 400

                user = User.query.filter_by(email=send_from_email).first()
                if not user or user.active == False:
                    return jsonify({'error': 'There is no user with the given email'}), 404

                friend_list = FriendList.query.filter_by(outing_id=str(outing_id)).all()
                if not friend_list:
                    return jsonify({'error': 'No friend list found for this outing ID'}), 404

                friend_list_emails = [User.query.filter_by(id=friend.user_id).first().email for friend in friend_list]
                if send_from_email not in friend_list_emails:
                    return jsonify({'error': 'These user cannot send message to this Outing'}), 400

                message = Message(
                    send_from=user.id,
                    datetime=datetime.utcnow(),
                    content=content,
                )
                db.session.add(message)
                db.session.commit()

                message_add_to_group = Messages(
                    messages_group_id = outing_id,
                    message_id=message.id,
                )

                db.session.add(message_add_to_group)
                db.session.commit()

                if get_all_messages:
                    messages = (db.session.query(Message.send_from, Message.content)
                                .filter(Message.id == Messages.messages_group_id)
                                .order_by(Message.datetime)
                                .all())
                    messages = sorted(messages, key=lambda msg: msg.datetime)

                    formatted_messages = [{'send_from': User.query.filter_by(id = send_from).first().email, 'content': content} for send_from, content in
                                          messages]
                    return jsonify({'messages': formatted_messages}), 200

                else:
                    return jsonify({'messages': [{'send_from': send_from_email, 'content': content}]}), 200

            except Exception as e:
                return jsonify({'error': f'Error sending message: {str(e)}'}), 500

    @users.route('/get-outings/<uuid:outing_id>/ai-chat/send', methods=['POST'])
    def send_to_ai_message(outing_id):
        if request.method == 'POST':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                send_from_email = request.json.get('send_from')
                content = request.json.get('content')

                if not send_from_email or not content:
                    return jsonify({'error': 'Send_from and content are required'}), 400

                user = User.query.filter_by(email=send_from_email).first()
                if not user or user.active == False:
                    return jsonify({'error': 'There is no user with the given email'}), 404

                if outing.creator_id != user.id:
                    return jsonify({'error': 'You are not owner of this Outing, you cannot share message to the AI!'}), 400

                ai_message = AiMessage(
                    send_from=user.id,
                    datetime=datetime.utcnow(),
                    content=content,
                )
                db.session.add(ai_message)
                db.session.commit()

                ai_message_add_to_group = AiMessages(
                    ai_messages_group_id = outing_id,
                    ai_message_id=ai_message.id,
                )

                db.session.add(ai_message_add_to_group)
                db.session.commit()

                response_content = "Hard-coded response"

                ai_message_response = AiMessage(
                    content=response_content,
                    datetime=datetime.utcnow(),
                )

                db.session.add(ai_message_response)
                db.session.commit()

                ai_message_add_to_group_response = AiMessages(
                    ai_messages_group_id = outing_id,
                    ai_message_id=ai_message_response.id,
                )

                db.session.add(ai_message_add_to_group_response)
                db.session.commit()

                return jsonify({'messages': [{'send_from': "NULL", 'content': response_content}]}), 200

            except Exception as e:
                return jsonify({'error': f'Error sending AI message: {str(e)}'}), 500

    return users