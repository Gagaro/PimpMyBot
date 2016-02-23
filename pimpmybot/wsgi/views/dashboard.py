from bottle import jinja2_view

from wsgi import app
from wsgi.modules import get_dashboard

route = app.route


@route('/dashboard', name='dashboard')
@jinja2_view('dashboard')
def dashboard_view():
    return {
        'dashboards': get_dashboard()
    }
