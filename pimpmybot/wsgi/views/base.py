import os

from bottle import jinja2_view, request, static_file, redirect

from utils.config import Configuration
from wsgi import BASE_DIR, app
from wsgi.messages import success

route = app.route


@route('/', name='index')
def index_view():
    return redirect(app.get_url('dashboard'))


@route('/status', name='status')
@jinja2_view('status')
def status_view():
    return {}


@route('/status', name='status', method="POST")
@jinja2_view('status')
def status_view_post():
    if 'restart' in request.forms.keys():
        app.restart_irc_bot()
    return {}


@route('/configuration', name='configuration')
@jinja2_view('configuration')
def configuration_view():
    return {'config': Configuration.get()}


@route('/configuration', name='configuration', method="POST")
@jinja2_view('configuration')
def configuration_view_post():
    configuration = Configuration.get()
    configuration.username = request.forms['username']
    configuration.oauth = request.forms['oauth']
    configuration.channel = request.forms['channel']
    configuration.save()
    success('Configuration saved')
    return {
        'config': configuration
    }


@route('/static/<filepath:path>')
def server_static(filepath):
    root_path = os.path.join(BASE_DIR, 'static')
    return static_file(filepath, root=root_path)
