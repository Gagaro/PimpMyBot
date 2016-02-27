from operator import attrgetter
from utils.config import Configuration, WidgetConfiguration


def get_menu():
    menu = []
    for module in Configuration.get().get_activated_modules():
        menu.extend(module.get_module().menus)
    return menu


def get_dashboard():
    dashboard = {
        'deactivated': [],
        'left': [],
        'middle': [],
        'right': [],
    }
    for module in Configuration.get().get_activated_modules():
        for identifier, widget in module.get_module().widgets.items():
            config = WidgetConfiguration.get_or_create(identifier=identifier)[0]
            widget.update({
                'config': config,
                'identifier': identifier,
            })
            if config.column in ['left', 'middle', 'right']:
                dashboard[config.column].append(widget)
            else:
                dashboard['deactivated'].append(widget)
    for column, widgets_list in dashboard.items():
        dashboard[column] = sorted(widgets_list, key=lambda d: d['config'].order)
    return dashboard
