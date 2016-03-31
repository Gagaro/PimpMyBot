from __future__ import absolute_import, unicode_literals

import schedule

from utils.modules import BaseModule
from utils.modules.parameters import CharParameter
from utils.translations import _
from utils import db

from .handlers import handle_users
from .models import User
from .schedules import update_users_time_watched


class UsersModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'users'
    title = _("Users")
    description = _("Track users watching and interacting with the stream.")

    menus = [{
        "title": "Users",
        "icon": "users",
        "view": "users:list"
    }]

    current_users = {}

    handlers = [handle_users]

    def __init__(self):
        schedule.every().minute.do(update_users_time_watched, self)

    @property
    def widgets(self):
        users_top5 = User.select().order_by(User.time_watched.desc())[:5]
        return {
            'users_top5': {
                'title': 'Top 5 users',
                'template': 'users_widget_top5',
                'context': {'users': users_top5}
            },
        }

    def install(self):
        super(UsersModule, self).install()
        db.create_tables([User])

    def uninstall(self):
        super(UsersModule, self).uninstall()
        db.drop_tables([User])
