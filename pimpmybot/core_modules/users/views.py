from __future__ import absolute_import, unicode_literals

from wsgi import app
from wsgi.bottle import jinja2_view

from .models import User

route = app.route


@route('/users/list', name='users:list')
@jinja2_view('users_list')
def users_list():
    users = User.select()
    return {
        'users': users,
    }
