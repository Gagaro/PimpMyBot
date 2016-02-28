import functools
import os

from bottle import Jinja2Template, request, view

from wsgi import app
from wsgi.modules import get_menu

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'locales')

def need_upgrades():
    """ Avoid circular import """
    from utils.modules import get_activated_modules
    return any([module.need_upgrades() for module in get_activated_modules()])


# Jinja2 configuration
class PmbJinja2Template(Jinja2Template):
    settings = {
        'autoescape': True,
        'extensions': ['jinja2.ext.i18n'],
    }

    defaults = {
        'request': request,
        'url': app.get_url,
        'irc_bot_is_alive': app.is_bot_alive,
        'get_messages': app.get_messages,
        'menu': get_menu,
        'need_upgrades': need_upgrades
    }

    def prepare(self, *args, **kwargs):
        from babel.support import Translations

        super(PmbJinja2Template, self).prepare(*args, **kwargs)
        translation = Translations.load(
            TRANSLATIONS_DIR,
            locales='fr_FR',
            domain='pimpmybot'
        )
        self.env.install_gettext_translations(translation)

jinja2_view = functools.partial(view, template_adapter=PmbJinja2Template)


import wsgi.views.base
import wsgi.views.dashboard
import wsgi.views.modules
