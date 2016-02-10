from peewee import Model, CharField

from . import db


class Configuration(Model):
    class Meta:
        database = db

    username = CharField(default="")
    oauth = CharField(default="")


if 'configuration' not in db.get_tables():
    # The database has not been created yet, let's do it.
    db.create_table(Configuration)
db.close()
