from multiprocessing import Pipe, Process
import os

from bottle import TEMPLATE_PATH, Bottle, debug

from irc.main import run as irc_run

# Bottle configuration
debug(True)
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH[:] = [os.path.join(BASE_DIR, 'templates')]


class App(Bottle):
    """ Main class used to handle the website and the bot. """

    def __init__(self):
        super(App, self).__init__()
        self.irc_pipe = None
        self.pipe = None
        self.irc_process = None

    def run(self):
        super(App, self).run()
        self.restart_irc_bot()

    def is_bot_alive(self):
        return self.irc_process is not None and self.irc_process.is_alive()

    def restart_irc_bot(self):
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
