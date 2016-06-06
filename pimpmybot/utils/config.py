from __future__ import absolute_import, unicode_literals

from peewee import Model, CharField, BooleanField, ForeignKeyField, IntegerField

from utils import db
from utils.modules import modules


class Configuration(Model):
    class Meta:
        database = db

    username = CharField(default="")
    oauth = CharField(default="")
    channel = CharField(default="")
    secret = CharField()
    upgrades = IntegerField()
    lang = CharField(default='en_US')
    send_as_me = BooleanField(default=True)

    def get_activated_modules(self):
        return self.modules.select().where(ModuleConfiguration.activated == True)


class ModuleConfiguration(Model):
    class Meta:
        database = db

    identifier = CharField()
    activated = BooleanField(default=False)
    installed = BooleanField(default=False)
    upgrades = IntegerField(default=0)
    configuration = ForeignKeyField(Configuration, related_name='modules', default=lambda: Configuration.get())

    def get_module(self):
        return modules[self.identifier]


class WidgetConfiguration(Model):
    class Meta:
        database = db

    identifier = CharField()
    order = IntegerField(default=0)
    column = CharField(default=None, null=True)

