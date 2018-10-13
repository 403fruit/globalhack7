import sqlalchemy_utils as sau

import arrow

from app.main import db


USER_RESOURCE_TYPES = [
    ('NEED', 'Need'),
    ('HAVE', 'Have'),
]


class TimestampMixin(object):
    created_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow)
    updated_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow, onupdate=arrow.utcnow)


class User(TimestampMixin, db.Model):
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


class UserResource(TimestampMixin, db.Model):
    __tablename__ = 'user_resources'
    id = db.Column(db.BigInteger, primary_key=True)
    resource_id = db.Column(db.BigInteger, db.ForeignKey('resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    resource = db.relationship('Resource', backref='user_resources')
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='resources')
    type = db.Column(sau.ChoiceType(USER_RESOURCE_TYPES), index=True)
    quantity_available = db.Column(db.BigInteger)
    quantity_needed = db.Column(db.BigInteger)
    quantity_fulfilled = db.Column(db.BigInteger)
    fulfills_id = db.Column(db.BigInteger, db.ForeignKey('user_resources.id', onupdate='CASCADE', ondelete='CASCADE'))
    fulfills = db.relationship('UserResource', foreign_keys=[fulfills_id], remote_side=[id], backref='fulfilled_by')

    @property
    def is_fulfilled(self):
        if self.quantity_needed is None:
            return None
        return self.quantity_needed - self.quantity_fulfilled <= 0
