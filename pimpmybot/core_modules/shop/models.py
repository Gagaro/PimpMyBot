from peewee import Model, IntegerField, ForeignKeyField, CharField, BooleanField, DateTimeField

from utils import db

from core_modules.users.models import User  # TODO find a better way to import modules


class ShopItem(Model):
    class Meta:
        database = db

    name = CharField(unique=True)
    price = IntegerField(null=False, default=0)
    active = BooleanField(default=True)


class BoughtItem(Model):
    class Meta:
        database = db

    user = ForeignKeyField(User, related_name='bought_items')
    item = ForeignKeyField(ShopItem, related_name='bought_items')
    datetime = DateTimeField()
    validated = BooleanField(default=False)
