from playhouse.migrate import SqliteMigrator, migrate

from utils import db

migrator = SqliteMigrator(db)
