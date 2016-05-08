""" Import the strawpoll module """
from __future__ import absolute_import, unicode_literals

import os

from bottle import TEMPLATE_PATH

from .strawpoll import StrawpollModule

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

# necessary to set a 'module' var to detect this specific module
# on irc.client.py (see def load_module)
module = StrawpollModule()

from . import views
