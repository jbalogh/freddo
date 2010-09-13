#!/usr/bin/env python
import os
import site
import sys

site.addsitedir('vendor')

# Make sure we have our local settings, then tell Celery about it.
# For best results, this happens before any 3rd-party imports.
SETTINGS = 'settings_local.py'
ROOT = os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(os.path.join(ROOT, 'settings_local.py')):
    sys.exit("ERROR: You've gotta have a {0!r}. Try this:\n\n"
             "  echo 'from settings import *' > {0}".format(SETTINGS))

os.environ['CELERY_CONFIG_MODULE'] = SETTINGS.split('.')[0]


from flaskext.script import Manager, Server, Shell

from app import app, db
import celeryd


manager = Manager(app)
manager.add_command('runserver', Server(port=8888))
manager.add_command('shell', Shell())
manager.add_command('celeryd', celeryd.celeryd())


@manager.command
def syncdb():
    db.create_all()


if __name__ == '__main__':
    manager.run()
