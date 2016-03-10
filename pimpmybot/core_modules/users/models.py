from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField

from utils import db


class User(Model):
    class Meta:
        database = db

    username = CharField(unique=True, null=False)
    twitch_id = IntegerField(unique=True, null=False)
    display_name = CharField(null=False)
    type = CharField(null=False)
    created = DateTimeField(null=False)

    # TODO
    follower = BooleanField(default=False)
    subscriber = BooleanField(default=False)
    first_watched = DateTimeField(null=True)
    last_watched = DateTimeField(null=True)
    time_watched = DateTimeField(null=True)
    first_message = DateTimeField(null=True)
    last_message = DateTimeField(null=True)
    messages_count = IntegerField(default=0)
