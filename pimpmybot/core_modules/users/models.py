from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField

from utils import db


class User(Model):
    class Meta:
        database = db

    username = CharField(unique=True)
    created = DateTimeField()
    follower = BooleanField()
    subscriber = BooleanField()
    status = CharField()
    first_watched = DateTimeField()
    last_watched = DateTimeField()
    time_watched = DateTimeField()
    last_message = DateTimeField()
    messages_count = IntegerField()
