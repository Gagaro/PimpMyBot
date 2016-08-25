import datetime

from peewee import Model, TextField, ForeignKeyField, CharField, BooleanField, DateTimeField, IntegerField

from utils import db

from users.models import User


class Bet(Model):
    class Meta:
        database = db

    started = DateTimeField(default=datetime.datetime.now)
    question = CharField()
    options = TextField(help_text="One per line. Leave them in the same order if voting already occured.")
    end_time = DateTimeField(null=True)

    active = BooleanField(default=True)  # Betting is possible if True
    ended = BooleanField(default=False)  # Ended and prizes given if True

    initial_pot = IntegerField(help_text="Base winnable amount.", default=0)
    min_amount = IntegerField(null=True)
    max_amount = IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_options(self):
        return self.options.replace('\r', '').split('\n')


class Answer(Model):
    class Meta:
        database = db

    bet = ForeignKeyField(Bet, related_name='answers')
    user = ForeignKeyField(User, related_name='bet_answers')
    options = IntegerField()