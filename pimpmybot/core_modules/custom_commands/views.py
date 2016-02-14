import os

from bottle import jinja2_view, request, TEMPLATE_PATH

from core_modules.custom_commands.module import Command
from wsgi import app

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__) , 'templates'))
route = app.route


@route('/custom_commands/settings', name='custom_commands:settings')
@jinja2_view('settings')
def custom_commands_settings():
    commands = Command.select()
    return {
        'commands': commands,
    }
