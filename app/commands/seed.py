from app.main import manager, db
from app.models.common import Category


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
        get_or_create({'name': "Lamp", 'parent': furnishings}, {'fontawesome_icon': "lamp"}),
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
