from utils.modules.parameters import BaseParameter

from money.models import Money
from money.utils import get_user_money, get_configuration
from users.models import User

from .models import ShopItem, BoughtItem


class ShopItemParameter(BaseParameter):
    def normalize(self, value):
        """ Convert the value from the form input to python. """
        return ShopItem.get(ShopItem.id == value)

    def render(self, value):
        """ Convert the python value to a printable one """
        return value.name

    def input(self, value=None):
        """ HTML input rendering. """
        options = []
        for item in ShopItem.select().order_by(ShopItem.name):
            selected = 'selected' if item.id == value else ''
            option = '<option value="{id}" {selected}>{name}</option>'.format(
                id=item.id, name=item.name, selected=selected
            )
            options.append(option)
        select = '<select class="form-control" name="{name}" required>{options}</select>'
        return select.format(name=self.name, options=''.join(options))


def buy_item(response, client, item):
    try:
        user = User.get(User.username == response.response_from)
    except User.DoesNotExist:
        return
    money = get_user_money(user)
    money_config = get_configuration()
    if money.amount < item.price:
        client.send("{0}, you need {1} {2} (currently {3})".format(
            user.username, item.price, money_config.money_name, money.amount)
        )
    else:
        BoughtItem.create(user=user, item=item)
        Money.update(amount=(Money.amount - item.price)).where(Money.user == user.id).execute()
        client.send("{0}, you just bought a {1} for {2} {3}".format(
            user.username, item.name, item.price, money_config.money_name)
        )
