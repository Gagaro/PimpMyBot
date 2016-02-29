from __future__ import absolute_import, unicode_literals

import hashlib
from multiprocessing import Pipe, Process
import os

from bottle import TEMPLATE_PATH, Bottle, debug

from utils import db
from utils.config import Configuration, ModuleConfiguration, WidgetConfiguration
from utils.upgrades import upgrades
from wsgi.csrf import require_csrf

# Bottle configuration
debug(True)
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH.append(os.path.join(BASE_DIR, 'templates'))


class App(Bottle):
    """ Main class used to handle the website and the bot. """

    def __init__(self):
        super(App, self).__init__()
        self.irc_pipe = None
        self.pipe = None
        self.irc_process = None
        self._messages = []

    def run(self):
        import wsgi.views

        self.update_db()
        self.restart_irc_bot()
        super(App, self).run()

    def get_messages(self):
        while self._messages:
            yield self._messages.pop()

    def add_message(self, message):
        self._messages.append(message)

    def is_bot_alive(self):
        return self.irc_process is not None and self.irc_process.is_alive()

    def restart_irc_bot(self):
        from irc.client import run as irc_run

        if self.irc_pipe is not None:
            self.irc_pipe.close()
        if self.pipe is not None:
            self.pipe.close()
        if self.irc_process is not None:
            self.irc_process.terminate()
        self.irc_pipe, self.pipe = Pipe(duplex=False)
        self.irc_process = Process(target=irc_run, args=(self.irc_pipe,))
        self.irc_process.start()

    def update_db(self):
        """ Install or upgrade DB if needed. """
        if 'configuration' not in db.get_tables():
            # The database has not been created yet, let's do it.
            from core_modules import install_core_modules

            db.create_tables([Configuration, ModuleConfiguration, WidgetConfiguration])
            Configuration.create(
                secret=hashlib.sha256(os.urandom(16)).hexdigest(),
                upgrades=len(upgrades),
            )
            install_core_modules()
        else:
            # Upgrade if needed
            upgrades_done = Configuration.select(Configuration.upgrades).get().upgrades
            if upgrades_done < len(upgrades):
                for upgrade in upgrades[upgrades_done:]:
                    upgrade()
                Configuration.update(upgrades=len(upgrades)).execute()


app = App()
app.install(require_csrf)
