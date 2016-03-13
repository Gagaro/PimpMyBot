from __future__ import absolute_import, unicode_literals

import dateutil
import functools

from babel.dates import format_datetime
from bottle import Jinja2Template, request, view

from utils.translations import locale
from wsgi import app
from wsgi.modules import get_menu


def need_upgrades():
    """ Avoid circular import """
    from utils.modules import get_activated_modules
    return any([module.need_upgrades() for module in get_activated_modules()])


# Filters

def datetimeformat(value, format='short'):
    if isinstance(value, str):
        value = dateutil.parser.parse(value)
    return format_datetime(value, format=format, locale=locale)


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
        from utils.translations import TRANSLATIONS_DIR
        from utils.config import Configuration

        translation = Translations.load(
            TRANSLATIONS_DIR,
            locales=Configuration.get().lang,
            domain='pimpmybot'
        )
        kwargs['filters'] = {
            'datetimeformat': datetimeformat
        }
        super(PmbJinja2Template, self).prepare(*args, **kwargs)
        self.env.install_gettext_translations(translation)

jinja2_view = functools.partial(view, template_adapter=PmbJinja2Template)
