from __future__ import absolute_import, unicode_literals

CORE_MODULES = ['ping', 'users']


def install_core_modules():
    from utils.modules import modules

    for module in CORE_MODULES:
        modules[module].activate()
