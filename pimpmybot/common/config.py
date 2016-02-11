from peewee import Model, CharField, BooleanField, ForeignKeyField

from core_modules import install_core_modules
from common import db
from common.modules import modules


class Configuration(Model):
    class Meta:
        database = db

    username = CharField(default="")
    oauth = CharField(default="")


class ModuleConfiguration(Model):
    class Meta:
        database = db

    identifier = CharField()
    activated = BooleanField(default=False)
    installed = BooleanField(default=False)
    configuration = ForeignKeyField(Configuration, related_name='modules', default=lambda: Configuration.get())

    def get_module(self):
        return modules[self.identifier]


if 'configuration' not in db.get_tables():
    # The database has not been created yet, let's do it.
    db.create_tables([Configuration, ModuleConfiguration])
    Configuration.create()
    install_core_modules()
db.close()
