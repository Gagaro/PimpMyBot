from __future__ import absolute_import, unicode_literals

from .module import UsersModule

# necessary to set a 'module' var to detect this specific module
# on irc.client.py (see def load_module)
module = UsersModule()

from . import views
