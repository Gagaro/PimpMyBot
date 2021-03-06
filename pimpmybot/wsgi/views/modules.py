from __future__ import absolute_import, unicode_literals

from bottle import request

from utils.config import ModuleConfiguration
from utils.modules import modules, get_activated_modules, get_deactivated_modules
from utils.translations import _
from wsgi import app
from wsgi.messages import success, danger
from wsgi.bottle import jinja2_view

route = app.route


@route('/modules', name='modules')
@jinja2_view('modules')
def modules_view():
    return {
        'modules': modules,
    }


@route('/modules', name='modules', method='POST')
@jinja2_view('modules')
def modules_view_post():
    if 'uninstall' in request.forms.keys():
        module = ModuleConfiguration.get(ModuleConfiguration.identifier == request.forms['uninstall'])
        if module.activated:
            danger(_('Module is activated.'))
        else:
            module.get_module().uninstall()
            success(_('Module uninstalled successfully.'))
    else:
        activated_modules = set([module.identifier for module in get_activated_modules()])
        deactivated_modules = set([module.identifier for module in get_deactivated_modules()])

        new_activated_modules = set(request.forms.keys())
        to_activate = new_activated_modules & deactivated_modules
        to_deactivate = activated_modules - new_activated_modules

        for identifier in to_activate:
            modules[identifier].activate()
        for identifier in to_deactivate:
            modules[identifier].deactivate()

        if to_activate or to_deactivate:
            success(_('Module changed successfully.'))
    return {
        'modules': modules,
    }


@route('/upgrades', name='upgrades')
@jinja2_view('upgrades')
def upgrades_view():
    for module in get_activated_modules():
        if module.need_upgrades():
            module.run_upgrades()
            success('Module "{0}" upgraded.'.format(module.title))
    success('All upgrades done.')
    return {}
