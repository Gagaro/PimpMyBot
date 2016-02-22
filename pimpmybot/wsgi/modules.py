from utils.config import Configuration, DashboardConfiguration


def get_menu():
    menu = []
    for module in Configuration.get().get_activated_modules():
        menu.extend(module.get_module().menus)
    return menu


def get_dashboard():
    dashboards = {
        'deactivated': [],
        'left': [],
        'middle': [],
        'right': [],
    }
    for module in Configuration.get().get_activated_modules():
        for identifier, dashboard in module.get_module().dashboards:
            config = DashboardConfiguration.get_or_create(DashboardConfiguration.identifier == identifier)[0]
            if config.column in ['left', 'middle', 'right']:
                dashboards[config.column].append(dashboard)
            else:
                dashboards['deactivated'].append(dashboard)
    return dashboards
