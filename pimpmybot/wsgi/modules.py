from __future__ import absolute_import, unicode_literals

from utils.modules.api import api as pmb_api
from utils.config import Configuration, WidgetConfiguration


def get_menu():
    """ Get the additional menu items. """
    menu = []
    for module in Configuration.get().get_activated_modules():
        menu.extend(module.get_module().menus)
    return menu


def get_dashboard():
    """ Get all widgets in the correct columns. """
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


def get_apis():
    """ Get all the available methods exposed by activated modules. """
    apis = {
        '__pmb': {
            'title': 'Pimp My Bot',
            'api': pmb_api
        }
    }
    for module in Configuration.get().get_activated_modules():
        module = module.get_module()
        if module.api:
            apis[module.identifier] = {
               'title': module.title,
               'api': module.api
            }
    return apis
