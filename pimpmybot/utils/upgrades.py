from __future__ import absolute_import, unicode_literals

from playhouse.migrate import *

from utils import db


def add_lang_to_configuration():
    migrator = SqliteMigrator(db)
    migrate(
        migrator.add_column('configuration', 'lang', CharField(default='en_US'))
    )


upgrades = [
    add_lang_to_configuration,
]
