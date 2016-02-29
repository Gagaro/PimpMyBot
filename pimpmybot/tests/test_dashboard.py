from __future__ import absolute_import, unicode_literals

import mock
import unittest

from tests.base import BaseTestCase
from utils.config import ModuleConfiguration
from utils.modules import BaseModule


class Module(BaseModule):
    """ Mock module """
    identifier = 'test'

    widgets = {
            'widget1': {
                'title': 'Widget 1',
                'html': '<strong>widget1</strong>'
            },

            'widget2': {
                'title': 'Widget 2',
                'html': '<strong>widget2</strong>'
            },
        }


class Module2(BaseModule):
    """ Mock module """
    identifier = 'test2'

    widgets = {
            'widget3': {
                'title': 'Widget 1',
                'html': '<strong>widget1</strong>'
            },
        }


modules = {
    'test': Module(),
    'test2': Module2(),
}

@mock.patch('utils.modules.modules', modules)
@mock.patch('utils.config.modules', modules)
class TestDashboard(BaseTestCase):
    def setUp(self):
        super(TestDashboard, self).setUp()
        ModuleConfiguration.update(activated=False).execute()
        ModuleConfiguration.create(identifier='test', activated=False, installed=True)
        ModuleConfiguration.create(identifier='test2', activated=True, installed=True)

    def test_get_dashboard(self):
        from wsgi.modules import get_dashboard

        dashboard = get_dashboard()
        self.assertEqual(len(dashboard['deactivated']), 1)
        self.assertEqual(len(dashboard['left']), 0)
        self.assertEqual(len(dashboard['middle']), 0)
        self.assertEqual(len(dashboard['right']), 0)


@mock.patch('utils.modules.modules', modules)
@mock.patch('utils.config.modules', modules)
class TestViews(BaseTestCase):
    def setUp(self):
        super(TestViews, self).setUp()
        ModuleConfiguration.update(activated=False).execute()
        ModuleConfiguration.create(identifier='test', activated=True, installed=True)
        ModuleConfiguration.create(identifier='test2', activated=False, installed=True)

    def test_get(self):
        from wsgi.views.dashboard import dashboard_view

        self.assertIn('Dashboard', dashboard_view())
