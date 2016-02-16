import os

from bottle import jinja2_view, request, TEMPLATE_PATH

from core_modules.custom_commands.module import Command
from peewee import IntegrityError
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


@route('/custom_commands/settings', name='custom_commands:settings', method="POST")
@jinja2_view('settings')
def custom_commands_settings():
    message = None
    # Create
    if 'create' in request.forms.keys():
        if request.forms['new-command'] and request.forms['new-message']:
            try:
                Command.create(command=request.forms['new-command'], message=request.forms['new-message'])
            except IntegrityError:
                message = 'Command "{0}" already exists.'.format(request.forms['new-command'])
            else:
                message = 'Command "{0}" created successfully.'.format(request.forms['new-command'])
    # Update
    elif 'update' in request.forms.keys():
        id = request.forms['update']
        command = request.forms['command-{0}'.format(id)]
        command_message = request.forms['message-{0}'.format(id)]
        if command and command_message:
            try:
                Command.update(command=command, message=command_message).where(Command.id == id).execute()
            except IntegrityError:
                message = 'Command "{0}" already exists.'.format(command)
            else:
                message = 'Command "{0}" updated successfully.'.format(command)
    # Delete
    elif 'delete' in request.forms.keys():
        id = request.forms['delete']
        command = request.forms['command-{0}'.format(id)]
        Command.delete().where(Command.id == id).execute()
        message = 'Command "{0}" deleted successfully.'.format(command)
    commands = Command.select()
    return {
        'message': message,
        'commands': commands,
    }
