from __future__ import absolute_import, unicode_literals

import gettext
import os

from appdirs import user_data_dir
from playhouse.sqlite_ext import SqliteExtDatabase

DATA_DIRECTORY = user_data_dir('PimpMyBot')
DATABASE_PATH = os.path.join(DATA_DIRECTORY, 'database.db')

if not os.path.exists(DATA_DIRECTORY):
    os.makedirs(DATA_DIRECTORY)
db = SqliteExtDatabase(
    DATABASE_PATH,
    pragmas=(
        ('journal_mode', 'WAL'),
        ('busy_timeout', 5000),
    )
)
