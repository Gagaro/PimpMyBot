test:
    python pimpmybot/testing.py

extract:
    pybabel extract -F babel.ini -o pimpmybot/locales/pimpmybot.pot pimpmybot

compile:
    pybabel compile -D pimpmybot -d pimpmybot/locales/

pyinstaller:
    pyinstaller pimpmybot.spec