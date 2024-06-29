from .extensions import db
import uuid


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}, Associate {self.associate_user}>'

    def to_dict(self):
        return {
            'id': self.id,
            'associate_user': self.associate_user
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


class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    google_api_key = db.Column(db.String(512), nullable=False)

    user = db.relationship('User', backref=db.backref('credentials', lazy=True))

    def __repr__(self):
        return f'<Credentials {self.id}, User {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'google_api_key': self.google_api_key
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
