from __future__ import absolute_import, unicode_literals

from peewee import Model, CharField, ForeignKeyField, IntegerField

from utils.modules import BaseModule, modules
from utils.modules.api import api as pmb_api
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

    def get_actions(self):
        return (
            Action
                .select()
                .join(CommandAction)
                .join(Command)
                .where(Command.id == self.id)
                .order_by(CommandAction.order)
        )


class CommandAction(Model):
    class Meta:
        database = db

    command = ForeignKeyField(Command)
    action = ForeignKeyField(Action)
    order = IntegerField(default=0)


def get_method_from_module(module, command):
    if module == '__pmb':
        api = pmb_api
    else:
        api = modules[module].api
    return api[command]
