from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField

from utils import db


class Strawpoll(Model):
    class Meta:
        database = db

    id = IntegerField(unique=True, null=False)
    title = CharField(null=False)

    def get_url(self):
        return "http://www.strawpoll.me/{0}".format(self.id)
