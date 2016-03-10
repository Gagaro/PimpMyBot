from __future__ import absolute_import, unicode_literals

import os

from babel import Locale
from babel.support import Translations
from peewee import OperationalError

from utils.config import Configuration

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')

try:
    locale = Configuration.get().lang
except OperationalError:
    locale = 'en_US'

translation = Translations.load(
    TRANSLATIONS_DIR,
    locales=locale,
    domain='pimpmybot'
)

_ = translation.gettext


languages = [
    Locale('en', 'US'),
    Locale('fr', 'FR')
]

