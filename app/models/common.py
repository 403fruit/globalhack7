import re

import sqlalchemy_utils as sau
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_babel import lazy_gettext
from app.main import login_manager

import arrow

from app.main import db


USER_RESOURCE_TYPES = [
    ('NEED', lazy_gettext('Need')),
    ('HAVE', lazy_gettext('Have')),
]

IMMIGRATION_STATUS = [
    ('ASYLEE', lazy_gettext("Asylee")),
    ('REFUGEE', lazy_gettext("Refugee")),
    ('NONIMMIGRANT', lazy_gettext("Nonimmigrant")),
    ('QUALIFIED_IMMIGRANT', lazy_gettext("Qualified Immigrant")),
    ('UNQUALIFIED_IMMIGRANT', lazy_gettext("Unqualified Immigrant")),
    ('SPONSOR', lazy_gettext("sponsor")),
    ('PUBLIC_CHARGE', lazy_gettext("Public Charge")),
    ('NATIVE_BORN_CITIZEN', lazy_gettext("Native Born Citizen")),
    ('NATURALIZED_CITIZEN', lazy_gettext("Naturalized Citizen"))
]

PRIMARY_ROLE = [
    ('IN_NEED_OF_AIDE', lazy_gettext('In Need Of Aide')),
    ('INDIVIDUAL_HELPER', lazy_gettext('Individual Helper')),
    ('CORPORATE_SPONSOR', lazy_gettext('Corporate Sponsor'))
]


class TimestampMixin(object):
    created_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow)
    updated_at = db.Column(sau.ArrowType(), nullable=False, index=True, default=arrow.utcnow, onupdate=arrow.utcnow)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    username = db.Column(db.Unicode(64), unique=True, nullable=False)
    password = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.UnicodeText(), nullable=True)
    phone = db.Column(db.BigInteger(), nullable=True)
    secondary_phone = db.Column(db.BigInteger(), nullable=True)
    bio = db.Column(db.UnicodeText, nullable=False)
    association = db.Column(db.Unicode(64), nullable=True)
    immigration_status = db.Column(sau.ChoiceType(IMMIGRATION_STATUS), index=True)
    primary_role = db.Column(sau.ChoiceType(PRIMARY_ROLE))
    language = db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(2), nullable=False)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def resources_needed(self):
        resources_needed = []
        for resource in Resource.query.filter(Resource.user_id==self.id, Resource.type=='NEEDED'):
            resources_needed.append(resource.name)
        return ", ".join(resources_needed)



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='CASCADE'))
    parent = db.relationship('Category', foreign_keys=[parent_id], remote_side=[id], backref='children')
    name = db.Column(db.UnicodeText(), nullable=False)
    fontawesome_icon = db.Column(db.UnicodeText())

    @property
    def fontawesome_icons(self):
        if self.fontawesome_icon is None:
            return ''

        return list(re.split(r',\s*', self.fontawesome_icon))

    @property
    def fontawesome_icon_classes(self):
        if self.fontawesome_icon is None:
            return ''

        return ['fas fa-' + i for i in re.split(r',\s*', self.fontawesome_icon)]


class Resource(TimestampMixin, db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.BigInteger, primary_key=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    category = db.relationship('Category', backref='resources')
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref='resources')
    type = db.Column(sau.ChoiceType(USER_RESOURCE_TYPES), index=True)
    quantity_available = db.Column(db.BigInteger)
    quantity_needed = db.Column(db.BigInteger)
    fulfilled = db.Column(db.Boolean, nullable=False, default=False, server_default='0')
    name = db.Column(db.UnicodeText(), nullable=False)

    @property
    def quantity_remaining(self):
        if self.type != 'HAVE':
            return None

        fulfillment = ResourceFulfillment.query.filter(
            ResourceFulfillment.fulfilling_resource == self,
            ResourceFulfillment.confirmed_by_recipient == True,
        )
        return self.quantity_available - sum([f.fulfilled_quantity for f in fulfillment])

    @property
    def quantity_fulfilled(self):
        if self.type != 'NEED':
            return None

        fulfillment = ResourceFulfillment.query.filter(
            ResourceFulfillment.fulfilled_resource == self,
            ResourceFulfillment.confirmed_by_recipient == True,
        )
        return self.quantity_needed - sum([f.fulfilled_quantity for f in fulfillment])

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.name,
            'user_id': self.user.id,
            'type': self.type.code,
            'quantity_available': self.quantity_available,
            'quantity_needed': self.quantity_needed,
            'fulfilled': self.fulfilled,
        }


class ResourceFulfillment(TimestampMixin, db.Model):
    __tablename__ = 'user_resource_fulfillment'
    id = db.Column(db.BigInteger, primary_key=True)
    fulfilling_resource_id = db.Column(db.BigInteger, db.ForeignKey('resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    fulfilling_resource = db.relationship('Resource', foreign_keys=[fulfilling_resource_id])
    fulfilled_resource_id = db.Column(db.BigInteger, db.ForeignKey('resources.id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    fulfilled_resource = db.relationship('Resource', foreign_keys=[fulfilled_resource_id])
    fulfilled_quantity = db.Column(db.BigInteger, nullable=False)
    confirmed_by_recipient = db.Column(db.Boolean, nullable=False, default=False, server_default='0')


Resource.fulfilled_by = db.relationship(
    'Resource',
    secondary=ResourceFulfillment.__table__,
    primaryjoin=Resource.id == ResourceFulfillment.fulfilled_resource_id,
    secondaryjoin=ResourceFulfillment.fulfilling_resource_id == Resource.id,
    backref='fulfills'
)
