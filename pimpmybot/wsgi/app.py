from multiprocessing import Pipe, Process
import os

from bottle import TEMPLATE_PATH, Bottle, debug

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


app = App()
