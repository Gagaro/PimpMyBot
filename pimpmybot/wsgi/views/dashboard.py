from __future__ import absolute_import, unicode_literals

import json

from bottle import HTTPResponse, request

from utils.config import WidgetConfiguration
from wsgi import app
from wsgi.modules import get_dashboard
from wsgi.bottle import jinja2_view

route = app.route


@route('/dashboard', name='dashboard')
@jinja2_view('dashboard')
def dashboard_view():
    return {
        'dashboard': get_dashboard()
    }


@route('/dashboard', name='dashboard', method='POST')
def dashboard_ajax_post_view():
    data = json.loads(request.forms['data'])
    for column in ['deactivated', 'left', 'middle', 'right']:
        order = 0
        for identifier in data.get(column, []):
            config = WidgetConfiguration.get(WidgetConfiguration.identifier == identifier)
            config.column = column
            config.order = order
            order += 1
            config.save()
    return HTTPResponse('OK')
