from bottle import request

from utils.config import Configuration
from utils.translations import languages
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success

route = app.route


@route('/configuration', name='configuration')
@jinja2_view('configuration')
def configuration_view():
    return {
        'config': Configuration.get(),
        'languages': languages,
    }


@route('/configuration', name='configuration', method="POST")
@jinja2_view('configuration')
def configuration_view_post():
    configuration = Configuration.get()
    configuration.username = request.forms['username']
    configuration.oauth = request.forms['oauth']
    configuration.channel = request.forms['channel']
    configuration.lang = request.forms['lang']
    configuration.save()
    success('Configuration saved')
    return {
        'config': configuration,
        'languages': languages,
    }

