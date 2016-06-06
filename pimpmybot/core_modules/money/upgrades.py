from playhouse.migrate import SqliteMigrator, migrate

from utils import db

from .models import MoneyConfiguration

migrator = SqliteMigrator(db)


def fix_money_configuration():
    db.create_table(MoneyConfiguration)
