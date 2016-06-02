""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from utils import db
from utils.modules import BaseModule
from utils.translations import _

from .models import Money, MoneyConfiguration


def current_user_money(client):
    pass


class MoneyModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'money'
    title = "Money"
    description = _("Allow users to gain moneys (virtual points).")
    dependencies = ['users']

    menus = [{
        "title": _("Money"),
        "icon": "usd",
        "menu": [
            {
                "title": _("Settings"),
                "icon": "cogs",
                "view": "money:settings"
            },
            {
                "title": _("Listing"),
                "icon": "list",
                "view": "money:list"
            },
        ],
    }]

    api = {
        'current_user_money': {
            'title': _('Current user money'),
            'method': current_user_money
        }
    }

    def install(self):
        super(MoneyModule, self).install()
        db.create_tables([Money, MoneyConfiguration])

    def uninstall(self):
        super(MoneyModule, self).uninstall()
        db.drop_tables([Money, MoneyConfiguration])
