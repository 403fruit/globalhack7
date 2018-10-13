from app.main import db
import sqlalchemy_utils as sau


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


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.UnicodeText, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.BigInteger(), nullable=True)
    secondary_phone = db.Column(db.BigInteger(), nullable=True)
    bio = db.Column(db.Text(), nullable=False)
    immigration_status = db.Column(sau.ChoiceType(IMMIGRATION_STATUS))
    primary_role = db.Column(sau.ChoiceType(PRIMARY_ROLE))
    languages = db.relationship('Language', backref='users')
    country = db.relationship('Country', backref='users')
    country_id = db.Column(
        db.BigInteger,
        db.ForeignKey(
            'country.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.BigInteger, primary_key=True)
    display_name = db.Column(db.String(255), nullable=False, unique=True)
    cole = db.Column(db.String(8), nullable=False, unique=True)


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


class UserLanguage(db.Model):
    __tablename__ = 'user_languages'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(
        db.BigInteger,
        db.ForeignKey(
            'user.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )
    language_id = db.Column(
        db.BigInteger,
        db.ForeignKey(
            'language.id',
            onupdate='CASCADE',
            ondelete='CASCADE'
        )
    )


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.BigInteger, primary_key=True)
    display_name = db.Column(db.String(128), nullable=False, unique=True)
    code = db.Column(db.String(3), nullable=False, unique=True)
