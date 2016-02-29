import sys

import os
import unittest
import mock

from playhouse.sqlite_ext import SqliteExtDatabase

if __name__ == '__main__':
    db = SqliteExtDatabase(':memory:', autocommit=False)
    with mock.patch('utils.db', db):
        from wsgi import app
        from wsgi.csrf import require_csrf

        app.uninstall(require_csrf)
        app.update_db()
        loader = unittest.TestLoader()
        tests = loader.discover(os.path.dirname(__file__))
        testRunner = unittest.runner.TextTestRunner()
        result = testRunner.run(tests)
        if result.errors:
            sys.exit(2)
        elif result.failures:
            sys.exit(1)
        sys.exit(0)