CORE_MODULES = ['ping', 'custom_commands']


def install_core_modules():
    from utils.modules import modules

    for module in CORE_MODULES:
        modules[module].activate()
