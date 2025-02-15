from .extensions import db
import uuid
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=False)
    refresh_token = db.Column(db.String(512), nullable=True)
    access_token = db.Column(db.String(512), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<User {self.display_name} with following id {self.id} and following firebase id {self.uid} is associated with this email : {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'associate_user': self.uid,
            "display_name": self.display_name,
            'email': self.email,
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Outing(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    latest_location = db.Column(db.String(240), nullable=True)
    outing_topic = db.Column(db.String(120), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    creator = db.relationship('User', backref=db.backref('outings', lazy=True))

    def __repr__(self):
        return f'<Outing {self.name} with following id {self.id}> is created from user with id: {self.creator_id} at {self.created_at}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'latest_location': self.latest_location,
            'outing_topic': self.outing_topic,
            'creator_id': self.creator_id
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, outing_id):
        return cls.query.get(outing_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

class FriendList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    outing_id = db.Column(db.String(36), db.ForeignKey('outing.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    outing = db.relationship('Outing', backref=db.backref('friend_list', lazy=True))
    user = db.relationship('User', backref=db.backref('friend_list', lazy=True))

    def __repr__(self):
        return f'<FriendList Outing {self.outing_id}, User {self.user_id}>'

    def to_dict(self):
        return {
            'outing_id': self.outing_id,
            'user_id': self.user_id
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_outing_id(cls, outing_id):
        return cls.query.filter_by(outing_id=outing_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    send_from = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    sender = db.relationship('User', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.id}, Send From {self.send_from}>'

    def to_dict(self):
        return {
            'id': self.id,
            'send_from': self.send_from,
            'datetime': self.datetime,
            'content': self.content
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, message_id):
        return cls.query.get(message_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

class AiMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    send_from = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # is_ai = db.Column(db.Boolean, nullable=False, default=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    sender = db.relationship('User', backref=db.backref('ai_messages', lazy=True))

    def __repr__(self):
        return f'<AiMessage {self.id}, Send From {self.send_from}, Is AI {self.is_ai}>'

    def to_dict(self):
        return {
            'id': self.id,
            'send_from': self.send_from,
            'is_ai': self.is_ai,
            'datetime': self.datetime,
            'content': self.content
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, ai_message_id):
        return cls.query.get(ai_message_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Messages(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    messages_group_id = db.Column(db.String(36), db.ForeignKey('outing.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)

    outing = db.relationship('Outing', backref=db.backref('messages', lazy=True))
    message = db.relationship('Message', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Messages {self.messages_group_id}, Message {self.message_id}>'

    def to_dict(self):
        return {
            'group_id': self.messages_group_id,
            'message_id': self.message_id
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_message_id(cls, message_id):
        return cls.query.filter_by(message_id=message_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

class AiMessages(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ai_messages_group_id = db.Column(db.String(36), db.ForeignKey('outing.id'))
    ai_message_id = db.Column(db.Integer, db.ForeignKey('ai_message.id'), nullable=False)

    outing = db.relationship('Outing', backref=db.backref('ai_messages', lazy=True))
    ai_message = db.relationship('AiMessage', backref=db.backref('ai_messages', lazy=True))

    def __repr__(self):
        return f'<Outing {self.ai_messages_group_id}, AI Message {self.ai_message_id}>'

    def to_dict(self):
        return {
            'group_id': self.ai_messages_group_id,
            'ai_message_id': self.ai_message_id
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_ai_message_id(cls, ai_message_id):
        return cls.query.filter_by(ai_message_id=ai_message_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

# class GroupChat(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     outing_id = db.Column(db.String(36), db.ForeignKey('outing.id'), primary_key=True)
#     messages_id = db.Column(db.Integer, db.ForeignKey('messages.messages_group_id'), nullable=False)
#
#     outing = db.relationship('Outing', backref=db.backref('group_chat', lazy=True))
#     messages = db.relationship('Messages', backref=db.backref('group_chat', lazy=True))
#
#     def __repr__(self):
#         return f'<GroupChat Outing {self.outing_id}, Messages {self.messages_id}>'
#
#     def to_dict(self):
#         return {
#             'outing_id': self.outing_id,
#             'messages_id': self.messages_id
#         }
#
#     @classmethod
#     def get_all(cls):
#         return cls.query.all()
#
#     @classmethod
#     def get_by_outing_id(cls, outing_id):
#         return cls.query.filter_by(outing_id=outing_id).first()
#
#     def save(self):
#         db.session.add(self)
#         db.session.commit()
#
# class GroupChatAI(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     outing_id = db.Column(db.String(36), db.ForeignKey('outing.id'))
#     ai_messages_id = db.Column(db.Integer, db.ForeignKey('ai_messages.ai_messages_group_id'), nullable=False)
#
#     outing = db.relationship('Outing', backref=db.backref('group_chat_ai', lazy=True))
#     ai_messages = db.relationship('AiMessages', backref=db.backref('group_chat_ai', lazy=True))
#
#     def __repr__(self):
#         return f'<GroupChat Outing {self.outing_id}, AI Messages {self.ai_messages_id}>'
#
#     def to_dict(self):
#         return {
#             'outing_id': self.outing_id,
#             'ai_messages_id': self.ai_messages_id
#         }
#
#     @classmethod
#     def get_all(cls):
#         return cls.query.all()
#
#     @classmethod
#     def get_by_outing_id(cls, outing_id):
#         return cls.query.filter_by(outing_id=outing_id).first()
#
#     def save(self):
#         db.session.add(self)
#         db.session.commit()