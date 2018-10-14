#! /usr/bin/env python

import logging
import sys
import os

from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand


# Create the app/init plugins before we can import commands
from app.main import get_app
app = get_app()

from app.main import (
    manager,
    db,
    )
logger = logging.getLogger('app')

from app.commands import seed, strings

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    try:
        manager.run()
    except Exception as e:
        logger.critical("Uncaught exception: %s: %s", e.__class__.__name__, str(e), exc_info=True)
        raise
