from peewee import Model, CharField, BooleanField, ForeignKeyField, IntegerField

from core_modules import install_core_modules
from utils import db
from utils.modules import modules


class Configuration(Model):
    class Meta:
        database = db

    username = CharField(default="")
    oauth = CharField(default="")
    channel = CharField(default="")

    def get_activated_modules(self):
        return self.modules.select().where(ModuleConfiguration.activated == True)


class ModuleConfiguration(Model):
    class Meta:
        database = db

    identifier = CharField()
    activated = BooleanField(default=False)
    installed = BooleanField(default=False)
    configuration = ForeignKeyField(Configuration, related_name='modules', default=lambda: Configuration.get())

    def get_module(self):
        return modules[self.identifier]


class DashboardConfiguration(Model):
    class Meta:
        database = db

    identifier = CharField()
    order = IntegerField(default=0)
    column = CharField(default=None, null=True)


if 'configuration' not in db.get_tables():
    # The database has not been created yet, let's do it.
    db.create_tables([Configuration, ModuleConfiguration, DashboardConfiguration])
    Configuration.create()
    install_core_modules()
db.close()
