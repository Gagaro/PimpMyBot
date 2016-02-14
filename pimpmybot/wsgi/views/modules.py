from bottle import jinja2_view, request

from utils.modules import modules
from wsgi import app

route = app.route


@route('/modules', name='modules')
@jinja2_view('modules')
def modules_view():
    activated_modules = [module for module in modules.values() if module.config.activated]
    deactivated_modules = [module for module in modules.values() if not module.config.activated]
    return {
        'activated_modules': activated_modules,
        'deactivated_modules': deactivated_modules
    }
