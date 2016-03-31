from __future__ import absolute_import, unicode_literals

import os

from bottle import request, TEMPLATE_PATH
from peewee import IntegrityError

from wsgi import app
from wsgi.messages import success, danger
from wsgi.bottle import jinja2_view
from wsgi.modules import get_apis
from utils.commands import Command, Action, CommandAction

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))
route = app.route


@route('/commands/settings', name='commands:settings')
@jinja2_view('commands/settings')
def commands_settings():
    commands = Command.select()
    return {
        'commands': commands,
    }


@route('/commands/add', name='commands:add_command')
@jinja2_view('commands/command_add_form')
def commands_add():
    return {
        'apis': get_apis(),
    }


@route('/commands/action_input', name='commands:action_input')
@jinja2_view('commands/action_input')
def commands_action_input():
    return {}
