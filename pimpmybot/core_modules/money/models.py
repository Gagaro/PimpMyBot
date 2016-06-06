from peewee import Model, IntegerField, ForeignKeyField, CharField

from utils import db

from core_modules.users.models import User  # TODO find a better way to import modules


class Money(Model):
    class Meta:
        database = db

    user = ForeignKeyField(User, related_name='money', primary_key=True)
    amount = IntegerField(null=False, default=0)

    def add(self, amount):
        self.amount += amount
        self.save()

    def remove(self, amount):
        self.amount -= amount
        self.save()


class MoneyConfiguration(Model):
    class Meta:
        database = db

    money_name = CharField(default="Magic Point", null=False)

    # Amount gained every 5 minutes
    amount_gain_inactive = IntegerField(null=False, default=1)

    # Amount gained every 5 minutes if the user talked in the chat
    amount_gain_active = IntegerField(null=False, default=2)
