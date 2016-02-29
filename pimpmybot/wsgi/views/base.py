from __future__ import absolute_import, unicode_literals

import os

from bottle import request, static_file, redirect

from wsgi import BASE_DIR, app
from wsgi.bottle import jinja2_view

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


@route('/static/<filepath:path>')
def server_static(filepath):
    root_path = os.path.join(BASE_DIR, 'static')
    return static_file(filepath, root=root_path)
