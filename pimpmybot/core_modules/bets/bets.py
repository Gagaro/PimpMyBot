""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

import schedule
from utils import db
from utils.modules import BaseModule
from utils.translations import _

from .models import Bet, Answer


class BetsModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'bet'
    title = "Bet"
    description = _("Allow users to place bets with money.")
    dependencies = ['users', 'money']

    menus = [{
        "title": _("Bet"),
        "icon": "trophy",
        "view": "bet:list",
    }]

    api = {
        # 'bet': {
        #     'title': _('Buy an item'),
        #     'method': buy_item,
        #     'parameters': [
        #         ShopItemParameter('item', title="Shop item"),
        #     ]
        # }
    }

    upgrades = []

    def install(self):
        super(BetsModule, self).install()
        db.create_tables([Bet, Answer])

    def uninstall(self):
        super(BetsModule, self).uninstall()
        db.drop_tables([Bet, Answer])
