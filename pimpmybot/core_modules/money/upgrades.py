from peewee import IntegerField
from playhouse.migrate import SqliteMigrator, migrate

from utils import db

from .models import MoneyConfiguration

migrator = SqliteMigrator(db)


def fix_money_configuration():
    db.create_table(MoneyConfiguration)


def add_gain_interval():
    migrate(
        migrator.add_column('moneyconfiguration', 'gain_interval', IntegerField(null=False, default=300)),
    )
