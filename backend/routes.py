from flask import Blueprint, jsonify, request
from datetime import datetime

from .models import User, Outing, \
                    FriendList, GroupChat, \
                    Messages, AiMessages, \
                    Message, AiMessage, \
                    GroupChatAI
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
                user = User(
                    uid = uid,
                    email=email,
                    display_name = display_name,
                    refresh_token= refresh_token
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
                if user:
                    return jsonify({'user': user.to_dict()}), 200
                else:
                    return jsonify({'error': 'User not found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        elif request.method == 'POST':
            display_name = request.json.get('display_name')
            refresh_token = request.json.get('refresh_token')
            try:
                user = User.query.filter_by(email=email).first()
                if user:
                    if display_name:
                        user.display_name = display_name
                    if refresh_token:
                        user.refresh_token = refresh_token
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
                if user:
                    db.session.delete(user)
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

                user = User.query.filter_by(email=user_email).first()
                if not user:
                    return jsonify({'error': 'User not found'}), 404

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

                # max_message_id = db.session.query(db.func.max(Messages.id)).scalar() or 0
                # max_ai_message_id = db.session.query(db.func.max(AiMessages.id)).scalar() or 0
                #
                # new_message_id = max_message_id + 1
                # new_ai_message_id = max_ai_message_id + 1
                #
                # group_chat = GroupChat(
                #     outing_id=outing.id,
                #     messages_id=new_message_id,
                #     ai_messages_id=new_ai_message_id
                # )
                # db.session.add(group_chat)

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
                if not user:
                    return jsonify({'error': 'User not found'}), 404

                outings = Outing.query.filter_by(creator_id=user.id).all()
                outings_list = [{"id" : outing.id, "name" : outing.name} for outing in outings]

                return jsonify({'outings': outings_list}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>', methods=['GET', 'POST', 'DELETE'])
    def get_outing(outing_id):
        def retrieve_outing_data(outing):
            group_chat = GroupChat.query.filter_by(outing_id=outing.id).first()
            group_chat_ai = GroupChatAI.query.filter_by(outing_id=outing.id).first()

            if group_chat:
                messages = (db.session.query(Message).
                            join(Messages).
                            filter(Messages.id == group_chat.messages_id).all())
            else:
                messages = []
            if group_chat_ai:
                ai_messages = (db.session.query(AiMessage).
                               join(AiMessages).
                               filter(AiMessages.id == group_chat_ai.ai_messages_id).all())
            else:
                ai_messages = []

            outing_data = {
                'name': outing.name,
                'location': outing.latest_location,
                'outing_topic': outing.outing_topic,
                'messages': [message.to_dict() for message in messages],
                'ai_messages': [ai_message.to_dict() for ai_message in ai_messages]
            }
            return outing_data

        if request.method == 'GET':
            try:
                outing = Outing.query.filter_by(id=outing_id).first()
                if not outing:
                    return jsonify({'error': 'Outing not found'}), 404

                outing_data = retrieve_outing_data(outing)

                return jsonify({"outing": outing_data}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500


        elif request.method == 'POST':
            try:
                data = request.get_json()
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': 'Outing not found'}), 404

                if 'location' in data:
                    outing.latest_location = data['location']

                if 'outing_topic' in data:
                    outing.outing_topic = data['outing_topic']

                db.session.commit()

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

                friend_list = FriendList.query.filter_by(outing_id=str(outing_id)).first()
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
                email = request.form.get('email')
                if not email:
                    return jsonify({'error': 'Email is required'}), 400

                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                user = User.query.filter_by(email=email).first()
                if not user:
                    return jsonify({'error': f'User with email {email} not found'}), 404

                friend = FriendList(
                    outing_id=outing_id,
                    user_id=user.id
                )
                db.session.add(friend)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    @users.route('/get-outings/<uuid:outing_id>/delete-friend', methods=['DELETE'])
    def delete_friend(outing_id):
        if request.method == 'DELETE':
            try:
                email = request.form.get('email')
                if not email:
                    return jsonify({'error': 'Email is required'}), 400

                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                user = User.query.filter_by(email=email).first()
                if not user:
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

                group_chat = GroupChat.query.filter_by(outing_id=outing.id).first()
                if not group_chat:
                    return jsonify({'messages': []}), 200

                messages = (db.session.query(Message.send_from, Message.content)
                            .filter(Message.id == group_chat.messages_id)
                            .order_by(Message.datetime)
                            .all())
                messages = sorted(messages, key=lambda msg: msg.datetime)
                formatted_messages = [{'send_from': send_from, 'content': content} for send_from, content in messages]

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

                group_chat = GroupChat.query.filter_by(outing_id=outing.id).first()
                if not group_chat:
                    return jsonify({'messages': []}), 200

                ai_messages = (db.session.query(AiMessage.send_from, AiMessage.content)
                            .filter(AiMessage.id == group_chat.messages_id)
                            .order_by(AiMessage.datetime)
                            .all())
                ai_messages = sorted(ai_messages, key=lambda msg: msg.datetime)
                formatted_messages = [{'send_from': send_from, 'content': content} for send_from, content in
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

                group_chat = GroupChat.query.filter_by(outing_id=outing.id).first()

                send_from = request.json.get('send_from')
                content = request.json.get('content')

                if not send_from or not content:
                    return jsonify({'error': 'Send_from and content are required'}), 400

                message = Message(
                    send_from=send_from,
                    datetime=datetime.utcnow(),
                    content=content,
                )
                db.session.add(message)
                db.session.commit()

                message_add_to_group = Messages(
                    message_id=message.id,
                )

                db.session.add(message_add_to_group)

                if not group_chat:
                    group_chat  = GroupChat(
                        outing_id=outing.id,
                        message_id = message_add_to_group.message_id
                    )

                    db.session.add(group_chat)
                    db.session.commit()

                if get_all_messages:
                    messages = (db.session.query(Message.send_from, Message.content)
                                .filter(Message.id == group_chat.messages_id)
                                .order_by(Message.datetime)
                                .all())
                    messages = sorted(messages, key=lambda msg: msg.datetime)

                    formatted_messages = [{'send_from': send_from, 'content': content} for send_from, content in
                                          messages]
                    return jsonify({'messages': formatted_messages}), 200

                else:
                    return jsonify({'messages': message}), 200

                return jsonify({'message': content}), 200

            except Exception as e:
                return jsonify({'error': f'Error sending message: {str(e)}'}), 500

    @users.route('/get-outings/<uuid:outing_id>/ai-chat/send', methods=['POST'])
    def send_to_ai_message(outing_id):
        if request.method == 'POST':
            try:
                outing = Outing.query.filter_by(id=str(outing_id)).first()
                if not outing:
                    return jsonify({'error': f'Outing with ID {outing_id} not found'}), 404

                group_chat = GroupChatAI.query.filter_by(outing_id=outing.id).first()

                send_from = request.json.get('send_from')
                content = request.json.get('content')

                if not send_from or not content:
                    return jsonify({'error': 'Send_from and content are required'}), 400

                ai_message = AiMessage(
                    send_from=send_from,
                    datetime=datetime.utcnow(),
                    content=content,
                )
                db.session.add(ai_message)
                db.session.commit()

                ai_message_add_to_group = AiMessages(
                    ai_message_id=ai_message.id,
                )

                db.session.add(ai_message_add_to_group)
                db.session.commit()

                if not group_chat:
                    group_chat_ai  = GroupChatAI(
                        outing_id=outing.id,
                        ai_message_id = ai_message_add_to_group.message_id
                    )

                    db.session.add(group_chat_ai)
                    db.session.commit()

                response_content = "Hard-coded response"

                ai_message_response = AiMessage(
                    send_from="NULL",
                    content=response_content,
                    datetime=datetime.utcnow(),
                )

                db.session.add(ai_message_response)
                db.session.commit()

                ai_message_add_to_group_response = AiMessages(
                    ai_message_id=ai_message_response.id,
                )

                db.session.add(ai_message_add_to_group_response)
                db.session.commit()

                return jsonify({'message': content}), 200

            except Exception as e:
                return jsonify({'error': f'Error sending AI message: {str(e)}'}), 500

    return users