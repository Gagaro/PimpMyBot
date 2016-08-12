import datetime

from peewee import Model, IntegerField, ForeignKeyField, CharField, BooleanField, DateTimeField

from utils import db

from users.models import User


class ShopItem(Model):
    class Meta:
        database = db

    name = CharField(unique=True)
    price = IntegerField(null=False, default=0)
    active = BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def transactions(self):
        return self.bought_items.select().order_by(BoughtItem.datetime.desc())


class BoughtItem(Model):
    class Meta:
        database = db

    user = ForeignKeyField(User, related_name='bought_items')
    item = ForeignKeyField(ShopItem, related_name='bought_items')
    datetime = DateTimeField(default=datetime.datetime.now)
    validated = BooleanField(default=False)
