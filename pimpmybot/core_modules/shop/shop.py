""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

import schedule
from utils import db
from utils.modules import BaseModule
from utils.translations import _

from .models import ShopItem, BoughtItem


class ShopModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'shop'
    title = "Shop"
    description = _("Allow users to buy things with money.")
    dependencies = ['users', 'money']

    menus = [{
        "title": _("Shop"),
        "icon": "shopping-cart",
        "view": "shop:items",
    }]

    api = {
        # 'buy_item': {
        #     'title': _('Buy an item'),
        #     'method': buy_item
        # }
    }

    upgrades = []

    def install(self):
        super(ShopModule, self).install()
        db.create_tables([ShopItem, BoughtItem])

    def uninstall(self):
        super(ShopModule, self).uninstall()
        db.drop_tables([ShopItem, BoughtItem])
