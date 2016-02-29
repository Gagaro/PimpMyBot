""" Import the pingModule """
from __future__ import absolute_import, unicode_literals

from .ping import PingModule

# necessary to set a 'module' var to detect this specific module
# on irc.client.py (see def load_module)
module = PingModule()
