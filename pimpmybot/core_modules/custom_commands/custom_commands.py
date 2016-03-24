from __future__ import absolute_import, unicode_literals

from peewee import Model, CharField, ForeignKeyField

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


def custom_command_handler(response, client):
    """ Look if the command is a custom one. """
    pass


class CustomCommandModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'custom_commands'
    title = "Custom commands"
    description = "Allow to send custom messages responding to custom commands."

    handlers = [custom_command_handler]

    menus = [{
        "title": "Custom commands",
        "icon": "terminal",
        "view": "custom_commands:settings"
    }]

    def install(self):
        super(CustomCommandModule, self).install()
        db.create_tables([Command])

    def uninstall(self):
        super(CustomCommandModule, self).uninstall()
        db.drop_tables([Command])
