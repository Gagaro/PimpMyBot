import json

from bottle import jinja2_view, HTTPResponse, request

from utils.config import DashboardConfiguration
from wsgi import app
from wsgi.modules import get_dashboard

route = app.route


@route('/dashboard', name='dashboard')
@jinja2_view('dashboard')
def dashboard_view():
    return {
        'dashboards': get_dashboard()
    }


@route('/dashboard', name='dashboard', method='POST')
def dashboard_ajax_post_view():
    data = json.loads(request.forms['data'])
    for column in ['deactivated', 'left', 'middle', 'right']:
        order = 0
        for identifier in data.get(column, []):
            config = DashboardConfiguration.get(DashboardConfiguration.identifier == identifier)
            config.column = column
            config.order = order
            order += 1
            config.save()
    return HTTPResponse('OK')
