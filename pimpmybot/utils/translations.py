import os

from babel.support import Translations

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')


translation = Translations.load(
    TRANSLATIONS_DIR,
    locales='fr_FR',
    domain='pimpmybot'
)

_ = translation.gettext
