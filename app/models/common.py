import sqlalchemy_utils as sau

import arrow

from app.main import db


USER_RESOURCE_TYPES = [
    ('NEED', 'Need'),
    ('HAVE', 'Have'),
]

IMMIGRATION_STATUS = [
    ('ASYLEE', 'Asylee'),
    ('REFUGEE', 'Refugee'),
    ('NONIMMIGRANT', 'Nonimmigrant'),
    ('QUALIFIED_IMMIGRANT', 'Qualified Immigrant'),
    ('UNQUALIFIED_IMMIGRANT', 'Unqualified Immigrant'),
    ('SPONSOR', 'sponsor'),
    ('PUBLIC_CHARGE', 'Public Charge'),
    ('NATIVE_BORN_CITIZEN', 'Native Born Citizen'),
    ('NATURALIZED_CITIZEN', 'Naturalized Citizen')
]

PRIMARY_ROLE = [
    ('IN_NEED_OF_AIDE', 'In Need Of Aide'),
    ('INDIVIDUAL_HELPER', 'Individual Helper'),
    ('CORPORATE_SPONSOR', 'Corporate Sponsor')
]


class TimestampMixin(object):
    created_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow)
    updated_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow, onupdate=arrow.utcnow)


class User(TimestampMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    username = db.Column(db.Unicode(64), unique=True, nullable=False)
    password = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.UnicodeText(), nullable=True)
    phone = db.Column(db.BigInteger(), nullable=True)
    secondary_phone = db.Column(db.BigInteger(), nullable=True)
    bio = db.Column(db.UnicodeText, nullable=False)
    immigration_status = db.Column(sau.ChoiceType(IMMIGRATION_STATUS), index=True)
    primary_role = db.Column(sau.ChoiceType(PRIMARY_ROLE))
    language = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(2), nullable=False)


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.UnicodeText())


class UserResource(TimestampMixin, db.Model):
    __tablename__ = 'user_resources'
    id = db.Column(db.BigInteger, primary_key=True)
    resource_id = db.Column(db.BigInteger, db.ForeignKey('resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    resource = db.relationship('Resource', backref='user_resources')
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='resources')
    type = db.Column(sau.ChoiceType(USER_RESOURCE_TYPES), index=True)
    quantity_available = db.Column(db.BigInteger)
    quantity_needed = db.Column(db.BigInteger)
    fulfilled = db.Column(db.Boolean, nullable=False, default=False, server_default='0')

    @property
    def quantity_remaining(self):
        if self.type != 'HAVE':
            return None

        fulfillment = UserResourceFulfillment.query.filter(
            UserResourceFulfillment.fulfilling_resource == self,
            UserResourceFulfillment.confirmed_by_recipient == True,
        )
        return self.quantity_available - sum([f.fulfilled_quantity for f in fulfillment])

    @property
    def quantity_fulfilled(self):
        if self.type != 'NEED':
            return None

        fulfillment = UserResourceFulfillment.query.filter(
            UserResourceFulfillment.fulfilled_resource == self,
            UserResourceFulfillment.confirmed_by_recipient == True,
        )
        return self.quantity_needed - sum([f.fulfilled_quantity for f in fulfillment])


class UserResourceFulfillment(TimestampMixin, db.Model):
    __tablename__ = 'user_resource_fulfillment'
    id = db.Column(db.BigInteger, primary_key=True)
    fulfilling_resource_id = db.Column(db.BigInteger, db.ForeignKey('user_resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    fulfilling_resource = db.relationship('UserResource', foreign_keys=[fulfilling_resource_id])
    fulfilled_resource_id = db.Column(db.BigInteger, db.ForeignKey('user_resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    fulfilled_resource = db.relationship('UserResource', foreign_keys=[fulfilled_resource_id])
    fulfilled_quantity = db.Column(db.BigInteger, nullable=False)
    confirmed_by_recipient = db.Column(db.Boolean, nullable=False, default=False, server_default='0')


UserResource.fulfilled_by = db.relationship(
    'UserResource',
    secondary=UserResourceFulfillment.__table__,
    primaryjoin=UserResource.id == UserResourceFulfillment.fulfilled_resource_id,
    secondaryjoin=UserResourceFulfillment.fulfilling_resource_id == UserResource.id,
    backref='fulfills'
)
