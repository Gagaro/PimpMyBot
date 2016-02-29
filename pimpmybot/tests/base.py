from __future__ import absolute_import, unicode_literals

import unittest

from webtest import TestApp

from utils import db
from wsgi import app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self._transaction = db.transaction()
        self._transaction.__enter__()

    def tearDown(self):
        self._transaction.__exit__(True, None, None)


class BaseFunctionalTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        import wsgi.views

    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()
        self.app = TestApp(app)
