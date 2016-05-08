from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField

from utils import db


class Strawpoll(Model):
    class Meta:
        database = db

    id = IntegerField(unique=True, null=False)
    title = CharField(null=False)
