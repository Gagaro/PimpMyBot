import os

import bottle
from bottle import route, run as bottle_run, jinja2_view

BASE_DIR = os.path.dirname(__file__)

bottle.TEMPLATE_PATH = [os.path.join(BASE_DIR, './templates/')]


@route('/')
@jinja2_view('index')
def index():
    return {}


@route('/settings')
@jinja2_view('settings')
def index():
    return {}


@route('/static/<filepath:path>')
def server_static(filepath):
    root_path = os.path.join(BASE_DIR, 'static')
    return bottle.static_file(filepath, root=root_path)


def run(pipe=None):
    bottle_run(host='localhost', port=8000)


if __name__ == '__main__':
    run()
