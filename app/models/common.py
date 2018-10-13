from app.main import db
import sqlalchemy_utils as sau


USER_RESOURCE_TYPES = [
    ('NEED', 'Need'),
    ('HAVE', 'Have'),
]


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.UnicodeText, nullable=False)
    name = db.Column(db.UnicodeText, nullable=False)
    country = db.Column(db.String(2))


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(500), index=True)


class UserResource(db.Model):
    __tablename__ = 'user_resources'
    id = db.Column(db.BigInteger, primary_key=True)
    type = db.Column(sau.ChoiceType(USER_RESOURCE_TYPES), index=True)
    quantity = db.Column(db.BigInteger)
    fulfilled = db.Column(db.Boolean, default=False, index=True)
