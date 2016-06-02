from .models import Money, MoneyConfiguration


def get_user_money(user):
    money, created = Money.get_or_create(user=user)
    return money


def get_configuration():
    config, created = MoneyConfiguration.get_or_create()
    return config
