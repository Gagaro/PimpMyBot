from bottle import jinja2_view, request

from utils.modules import modules, get_activated_modules, get_deactivated_modules
from wsgi import app
from wsgi.messages import success

route = app.route


@route('/modules', name='modules')
@jinja2_view('modules')
def modules_view():
    return {
        'activated_modules': get_activated_modules(),
        'deactivated_modules': get_deactivated_modules()
    }


@route('/modules', name='modules', method='POST')
@jinja2_view('modules')
def modules_view_post():
    activated_modules = set([module.identifier for module in get_activated_modules()])
    deactivated_modules = set([module.identifier for module in get_deactivated_modules()])

    new_activated_modules = set(request.forms.keys())
    to_activate = new_activated_modules & deactivated_modules
    to_deactivate = activated_modules - new_activated_modules

    for identifier in to_activate:
        modules[identifier].install()
    for identifier in to_deactivate:
        modules[identifier].uninstall()

    if to_activate or to_deactivate:
        success('Module changed successfully.')
    return {
        'activated_modules': get_activated_modules(),
        'deactivated_modules': get_deactivated_modules()
    }
