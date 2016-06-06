from __future__ import absolute_import, unicode_literals

from peewee import BooleanField
from playhouse.migrate import SqliteMigrator, migrate

from utils import db

migrator = SqliteMigrator(db)


def add_send_as_me():
    migrate(migrator.add_column('configuration', 'send_as_me', BooleanField(default=True)))


upgrades = [
    add_send_as_me
]
