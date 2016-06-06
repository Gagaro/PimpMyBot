""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta

import schedule
from utils import db
from utils.modules import BaseModule
from utils.translations import _

from .models import Money, MoneyConfiguration, User
from .utils import get_configuration, get_user_money
from .upgrades import fix_money_configuration


def current_user_money(response, client):
    try:
        user = User.get(User.username == response.response_from)
    except User.DoesNotExist:
        return
    money = get_user_money(user)
    config = get_configuration()
    client.send('{0}, you have {1} {2}'.format(user.username, money.amount, config.money_name))


def update_users_money():
    from utils.modules import modules

    users_ids = [user.id for user in modules['users'].current_users.values()]
    # First create the money for the user missing it
    in_db = set(user.user_id for user in Money.select(Money.user).filter(Money.user << users_ids))
    missing_ids = set(users_ids) ^ in_db
    missing_moneys = [{'user': user_id, 'amount': 0} for user_id in missing_ids]
    with db.atomic():
        for idx in range(0, len(missing_moneys), 100):
            Money.insert_many(missing_moneys[idx:idx + 100]).execute()
    # Next, update everything
    config = get_configuration()
    active_time = datetime.now() - timedelta()

    active_ids = [user.id for user in User.select(User.id).where(User.id << users_ids, User.last_message >= active_time.isoformat(' '))]
    inactive_ids = list(set(users_ids) ^ set(active_ids))
    with db.atomic():
        Money.update(amount=Money.amount + config.amount_gain_active).where(Money.user << active_ids).execute()
        Money.update(amount=Money.amount + config.amount_gain_inactive).where(Money.user << inactive_ids).execute()


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

    upgrades = [fix_money_configuration]

    def load(self):
        super(MoneyModule, self).load()
        schedule.every(5).minutes.do(update_users_money)

    def install(self):
        super(MoneyModule, self).install()
        db.create_tables([Money, MoneyConfiguration])

    def uninstall(self):
        super(MoneyModule, self).uninstall()
        db.drop_tables([Money, MoneyConfiguration])
