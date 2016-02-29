from __future__ import absolute_import, unicode_literals

import os

from babel import Locale
from babel.support import Translations
from utils.config import Configuration

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')

translation = Translations.load(
    TRANSLATIONS_DIR,
    locales=Configuration.get().lang,
    domain='pimpmybot'
)

_ = translation.gettext


languages = [
    Locale('en', 'US'),
    Locale('fr', 'FR')
]

