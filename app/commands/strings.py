from app.main import manager, db
from app.models.common import Category


@manager.command
def strings(potfile='messages.pot', update=False):
    with open(potfile, 'r') as fp:
        existing_strings = [l.strip() for l in fp.readlines() if l.startswith('msgid ')]

    models = [
        (
            Category,
            ['name']
        )
    ]

    out = []
    for model, fields in models:
        for row in model.query.order_by(model.id.asc()):
            for field in fields:
                msgid = 'msgid "{}"'.format(getattr(row, field, ''))
                if msgid in existing_strings:
                    continue
                out.append(f'#: {model.__name__}:{row.id}/{field}')
                out.append(msgid)
                out.append('msgstr ""')
                out.append('')
    out.append('')

    if update:
        with open(potfile, 'a') as fp:
            fp.write('\n'.join(out))
    else:
        print('\n'.join(out))
