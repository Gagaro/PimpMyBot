test:
    python pimpmybot/testing.py

extract:
    pybabel.exe extract -F babel.ini -o pimpmybot/locales/pimpmybot.pot pimpmybot
