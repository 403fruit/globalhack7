import random
from collections import namedtuple

import requests

from app.main import manager, db
from app.models.common import Category, User, Resource
from app.models.common import USER_RESOURCE_TYPES, PRIMARY_ROLE


ASSOCIATIONS = [
    'Washington University Foreign Language Professor',
    'International Institute Associate',
]
LOCALES = [
    ("en", 'US'),
    ("es", 'MX'),
    ("zh", 'CN'),
    ("fr", 'FR'),
    ("ar", 'SY'),
    ("vi", 'VN'),
]

def rchance(pc, next):
    if random.random() <= pc:
        return next()
    return None

class FileWrapper(object):
    def __init__(self, url):
        self.filename = url.split('/')[-1]
        self.url = url
        self.res = requests.get(url, stream=True)

    def read(self, bytes=None):
        return self.res.raw.read()

    def save(self, filename):
        with open(filename, 'wb') as fp:
            while True:
                data = self.read()
                if len(data) == 0:
                    break
                fp.write(data)


def get_or_create(query_props, upd_props):
    obj = Category.query.filter_by(**query_props).first()
    if not obj:
        obj = Category(**dict(query_props, **upd_props))
    for k, v in upd_props.items():
        setattr(obj, k, v)
    return obj


@manager.command
def seed_categories():
    furnishings = get_or_create({'name': "Furnishings"}, {'fontawesome_icon': "couch, bed, chair"})
    financial = get_or_create({'name': "Financial Assistance"}, {'fontawesome_icon': "yen-sign, dollar-sign, credit-card"})
    jobs = get_or_create({'name': "One Time Jobs"}, {'fontawesome_icon': "building, hammer, people-carry"})

    db.session.add_all([
        furnishings,
        financial,
        jobs,

        get_or_create({'name': "Bed", 'parent': furnishings}, {'fontawesome_icon': "bed"}),
        get_or_create({'name': "Couch", 'parent': furnishings}, {'fontawesome_icon': "couch"}),
        get_or_create({'name': "Chair", 'parent': furnishings}, {'fontawesome_icon': "chair"}),
        get_or_create({'name': "Lamp", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Dining Table", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Table", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Refrigerator", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Microwave", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Stove or Oven", 'parent': furnishings}, {'fontawesome_icon': None}),
        get_or_create({'name': "Clothes Washer or Dryer", 'parent': furnishings}, {'fontawesome_icon': None}),

        get_or_create({'name': "Lawn Mowing", 'parent': jobs}, {'fontawesome_icon': None}),
        get_or_create({'name': "Moving", 'parent': jobs}, {'fontawesome_icon': "people-carry"}),
        get_or_create({'name': "Car Repair", 'parent': jobs}, {'fontawesome_icon': "car"}),
        get_or_create({'name': "Painting", 'parent': jobs}, {'fontawesome_icon': "paint-brush"}),
        get_or_create({'name': "Minor Construction", 'parent': jobs}, {'fontawesome_icon': "hammer"}),
    ])
    db.session.commit()


@manager.command
def seed_user(num=None, seed=None):
    params = {
        'results': num or 1,
        'inc': 'name,location,email,login,phone,cell,picture,nat',
    }
    if seed:
        params['seed'] = seed
    res = requests.get('https://randomuser.me/api/', params=params)
    for info in res.json()['results']:
        user = User(
            name=' '.join((v.title() for v in (info['name']['first'], info['name']['last']) if v)),
            username=info['login']['username'],
            email=info['email'],
            phone=int(info['phone'].replace('-', '')),
            secondary_phone=int(info['cell'].replace('-', '')),
            bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            association=rchance(0.05, lambda: random.choice(ASSOCIATIONS)),
            primary_role=random.choice(list(dict(PRIMARY_ROLE).keys())),
        )
        user.set_password('password')
        user.language, user.country = random.choice(LOCALES)
        db.session.add(user)
        db.session.commit()
        user.picture = FileWrapper(info['picture']['large'])
        db.session.add(user)
        db.session.commit()


@manager.command
def seed_resource(num=None):
    cats = [c for c in Category.query if not len(c.children)]
    users = User.query.all()
    # for _ in range(num or 1):
    #     type_ = random.choice([v[0] for v in USER_RESOURCE_TYPES])
    #     resource = Resource(
    #         category=random.choice(cats),
    #         user=random.choice(users),
    #         type=type_,
    #         quantity_available=random.randint(1, 5) if type_ == 'HAVE' else None,
    #         quantity_needed=random.randint(1, 5) if type_ == 'NEED' else None,
    #         fulfilled=random.randint(0, 1) if type_ == 'NEED' else None,
    #         # name = db.Column(db.UnicodeText(), nullable=False)
    #         # picture = db.Column(db.UnicodeText())
    #     )