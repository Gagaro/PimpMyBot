from peewee import Model, CharField

from common.modules import BaseModule
from common import db


class Command(Model):
    class Meta:
        database = db

    command = CharField()
    message = CharField()


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
