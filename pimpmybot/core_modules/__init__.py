from common.modules import modules

CORE_MODULES = ['ping']


def install_core_modules():
    for module in CORE_MODULES:
        modules[module].install()