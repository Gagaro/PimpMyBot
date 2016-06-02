from .models import Money
from core_modules.users.models import User  # TODO find a better way to import modules


def get_user_money(user):
    money = Money.get_or_create(user=user)
    return money
