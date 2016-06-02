from __future__ import absolute_import, unicode_literals

import json

import requests
from bottle import redirect, request

from utils.translations import _
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success, danger

route = app.route


@route('/money/settings', name='money:settings')
@jinja2_view('money_settings')
def money_settings():
    return {}


@route('/money/list', name='money:list')
@jinja2_view('money_list')
def money_list():
    return {}
