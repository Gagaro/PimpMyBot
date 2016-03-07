from __future__ import absolute_import, unicode_literals

import os

from bottle import TEMPLATE_PATH

from wsgi import app
from wsgi.bottle import jinja2_view

from .models import User

TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'templates'))
route = app.route


@route('/users/list', name='users:list')
@jinja2_view('users_list')
def users_list():
    users = User.select()
    return {
        'users': users,
    }
