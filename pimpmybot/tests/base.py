import unittest

from webtest import TestApp

from utils import db
from wsgi import app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        db.begin()

    def tearDown(self):
        db.rollback()


class BaseFunctionalTestCase(BaseTestCase):
    def setUp(self):
        super(BaseFunctionalTestCase, self).setUp()
        self.app = TestApp(app)