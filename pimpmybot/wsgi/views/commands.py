from __future__ import absolute_import, unicode_literals

import json
import os

from bottle import request, TEMPLATE_PATH, redirect
from peewee import IntegrityError

from utils import db
from utils.commands import Command, Action, CommandAction, get_action_info
from utils.translations import _
from wsgi import app
from wsgi.messages import success, danger
from wsgi.bottle import jinja2_view
from wsgi.modules import get_apis

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))
route = app.route


@route('/commands/', name='commands:list')
@jinja2_view('commands/list')
def commands_list():
    commands = Command.select()
    return {
        'commands': commands,
        'get_action_info': get_action_info,
    }


@route('/commands/add', name='commands:add')
@jinja2_view('commands/add')
def commands_add():
    return {
        'apis': get_apis(),
    }


@route('/commands/add', name='commands:add', method="POST")
def commands_add_post():
    data = request.forms
    with db.atomic():
        command = Command.create(command=data['command'])
        for i in range(int(data['actions_number'])):
            # Each action has actionX prepended to its inputs
            namespace = 'action{0}'.format(i)
            module, method = data['{0}_action_type'.format(namespace)].split('|')
            parameters = {
                key[len(namespace):]: value
                for key, value in data.items()
                if key.startswith(namespace) and not key.endswith('_action_type')
            }
            action = Action.create(module=module, method=method, parameters=json.dumps(parameters))
            CommandAction.create(command=command, action=action, order=i)
        success(_("Command created."))
    return redirect(app.get_url('commands:list'))


@route('/commands/edit/<id:int>', name='commands:edit')
@jinja2_view('commands/edit')
def command_edit(id):
    command = Command.get(id=id)
    return {'command': command}


@route('/commands/delete/<id:int>', name='commands:delete')
@jinja2_view('commands/delete')
def command_delete(id):
    command = Command.get(id=id)
    return {'command': command}


@route('/commands/delete/<id:int>', name='commands:delete', method="POST")
@jinja2_view('commands/delete')
def command_delete(id):
    if Command.get(id=id).delete_instance():
        success(_("Command deleted."))
    else:
        danger(_("Error while deleting command."))
    return redirect(app.get_url('commands:list'))


@route('/commands/action_input', name='commands:action_input')
@jinja2_view('commands/action_input')
def commands_action_input():
    module, method = request.query['action'].split('|')
    action = get_apis()[module]['api'][method]
    return {
        'action_type': request.query['action'],
        'action': action
    }
