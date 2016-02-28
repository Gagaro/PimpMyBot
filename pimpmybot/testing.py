import sys

import os
import unittest
import mock

from playhouse.sqlite_ext import SqliteExtDatabase

from wsgi import app
from wsgi.csrf import require_csrf

app.uninstall(require_csrf)

if __name__ == '__main__':
    db = SqliteExtDatabase(':memory:', autocommit=False)
    with mock.patch('utils.db', db):
        loader = unittest.TestLoader()
        tests = loader.discover(os.path.dirname(__file__))
        testRunner = unittest.runner.TextTestRunner()
        failures, errors = testRunner.run(tests)

    if errors:
        sys.exit(2)
    elif failures:
        sys.exit(1)

    sys.exit(0)