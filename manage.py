from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import create_app
from app.extensions import db

app = create_app('config.development')  # TODO: config var

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
