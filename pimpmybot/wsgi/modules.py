from utils.config import Configuration


def get_menu():
    menu = []
    for module in Configuration.get().get_activated_modules():
        menu.extend(module.get_module().menus)
    return menu


def get_dashboard():
    return []
