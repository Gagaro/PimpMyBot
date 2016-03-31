from __future__ import absolute_import, unicode_literals

from peewee import Model, CharField, ForeignKeyField, IntegerField

from utils.modules import BaseModule
from utils import db


class Action(Model):
    class Meta:
        database = db

    # Name of the module or "__pmb" for the global one
    module = CharField()
    # Name of the method to call
    method = CharField()
    # JSON encoded parameters
    parameters = CharField()


class Command(Model):
    class Meta:
        database = db

    command = CharField(unique=True)


class CommandAction(Model):
    class Meta:
        database = db

    command = ForeignKeyField(Command)
    action = ForeignKeyField(Action)
    order = IntegerField(default=0)
