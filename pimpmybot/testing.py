import os
import unittest
import mock

from playhouse.sqlite_ext import SqliteExtDatabase

# FIXME Need to import app to avoid circular import
from wsgi import app


if __name__ == '__main__':
    with mock.patch('utils.db', SqliteExtDatabase(':memory:')):
        loader = unittest.TestLoader()
        tests = loader.discover(os.path.dirname(__file__))
        testRunner = unittest.runner.TextTestRunner()
        testRunner.run(tests)
