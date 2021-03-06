from __future__ import absolute_import, unicode_literals

from tests.base import BaseFunctionalTestCase
from wsgi import app


class TestWsgi(BaseFunctionalTestCase):

    def test_configuration_post(self):
        from utils.config import Configuration

        self.app.post(app.get_url('configuration'), {
            'username': 'USERNAME',
            'oauth': 'OAUTH',
            'channel': 'CHANNEL',
            'lang': 'en_US',
        })

        config = Configuration.get()
        self.assertEqual(config.username, 'USERNAME')
        self.assertEqual(config.oauth, 'OAUTH')
        self.assertEqual(config.channel, 'CHANNEL')
