import os

from bottle import (
    TEMPLATE_PATH, Jinja2Template,
    debug, jinja2_view, request, route,
    run as bottle_run, static_file, url
)

from common.config import Configuration

# Bottle configuration
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH[:] = [os.path.join(BASE_DIR, 'templates')]

# Jinja2 configuration
Jinja2Template.defaults = {
    'url': url,
}
Jinja2Template.settings = {
    'autoescape': True,
}


@route('/', name='index')
@jinja2_view('index')
def index_view():
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
    configuration.save()
    return {
        'message': 'Configuration saved',
        'config': configuration
    }


@route('/static/<filepath:path>')
def server_static(filepath):
    root_path = os.path.join(BASE_DIR, 'static')
    return static_file(filepath, root=root_path)


def run(pipe=None):
    debug(True)
    bottle_run(host='localhost', port=8000)


if __name__ == '__main__':
    run()
