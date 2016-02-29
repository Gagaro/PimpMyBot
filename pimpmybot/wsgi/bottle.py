from __future__ import absolute_import, unicode_literals

import functools

from bottle import Jinja2Template, request, view

from wsgi import app
from wsgi.modules import get_menu


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
        from utils.translations import TRANSLATIONS_DIR
        from utils.config import Configuration

        translation = Translations.load(
            TRANSLATIONS_DIR,
            locales=Configuration.get().lang,
            domain='pimpmybot'
        )
        super(PmbJinja2Template, self).prepare(*args, **kwargs)
        self.env.install_gettext_translations(translation)

jinja2_view = functools.partial(view, template_adapter=PmbJinja2Template)
