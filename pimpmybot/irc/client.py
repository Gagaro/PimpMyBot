from logging import DEBUG
import socket

import six

from common.config import Configuration
from common.logging import get_logger

logger = get_logger('irc', DEBUG)

HOST = 'irc.twitch.tv'
PORT = 6667


class Client(object):
    """ Connect to IRC and dispatch the messages to the handlers. """
    def __init__(self):
        self.config = Configuration.get_or_create()[0]
        self.socket = socket.socket()
        self.handlers = []

    def connect(self):
        self.socket.close()
        self.socket = socket.socket()

        if not self.config.oauth:
            logger.warning('No oauth token configured.')
            return
        if not self.config.username:
            logger.warning('No username configured.')
            return

        logger.debug('Connecting to {0}:{1}'.format(HOST, PORT))
        self.socket.connect((HOST, PORT))
        self.send('PASS {0}\r\n'.format(self.config.oauth))
        self.send('NICK {0}\r\n'.format(self.config.username))

    def send(self, message):
        logger.debug('> {0}'.format(message))
        if isinstance(message, six.text_type):
            message = message.encode('utf8')
        self.socket.send(message)

    def run(self):
        while True:
            try:
                response = self.socket.recv(1024).decode().strip()
            except OSError:
                # Socket is probably close, let's wait until it's connected
                # FIXME Find a way to handle this cleanly
                import time
                time.sleep(5)
                continue
            if response:
                logger.debug('< {0}'.format(response))
                self.handle(response)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def remove_handler(self, handler):
        self.handlers.remove(handler)

    def handle(self, response):
        for handler in self.handlers:
            if handler.handle(response, self):
                return

def run(pipe):
    client = Client()
    client.connect()
    client.run()
