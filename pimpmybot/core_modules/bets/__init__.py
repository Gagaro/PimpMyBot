""" Import the bet module """
from __future__ import absolute_import, unicode_literals

import os

from bottle import TEMPLATE_PATH

from .bets import BetsModule

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))

# necessary to set a 'module' var to detect this specific module
# on irc.client.py (see def load_module)
module = BetsModule()

from . import views
