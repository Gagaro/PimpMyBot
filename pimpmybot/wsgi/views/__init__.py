from bottle import Jinja2Template, request

from wsgi import app
from wsgi.csrf import csrf_tag
from wsgi.modules import get_menu

# Jinja2 configuration
Jinja2Template.settings = {
    'autoescape': True,
}
Jinja2Template.defaults = {
    'request': request,
    'url': app.get_url,
    'irc_bot_is_alive': app.is_bot_alive,
    'get_messages': app.get_messages,
    'menu': get_menu,
    'csrf_tag': csrf_tag,
}


import wsgi.views.base
import wsgi.views.dashboard
import wsgi.views.modules
