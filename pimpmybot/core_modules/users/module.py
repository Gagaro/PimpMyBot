from __future__ import absolute_import, unicode_literals

from utils.modules import BaseModule
from utils.translations import _
from utils import db

from .handlers import handle_users
from .models import User


class UsersModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'users'
    title = _("Users")
    description = _("Track users watching and interacting with the stream.")

    handlers = [handle_users]

    menus = [{
        "title": "Users",
        "icon": "users",
        "view": "users:list"
    }]

    @property
    def widgets(self):
        return {
            'current_users': {
                'title': 'Current users',
                'html': '<strong>TODO</strong>'
            },
            'users_top5': {
                'title': 'Top 5 users',
                'html': '<strong>TODO</strong>'
            },
        }

    def install(self):
        super(UsersModule, self).install()
        db.create_tables([User])

    def uninstall(self):
        super(UsersModule, self).uninstall()
        db.drop_tables([User])
