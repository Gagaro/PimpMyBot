from __future__ import absolute_import, unicode_literals

from logging import DEBUG
import socket

import six

from irc.parser import Response
from irc.sender import Sender
from utils.config import Configuration
from utils.logging import get_logger


logger = get_logger('irc', DEBUG)

HOST = 'irc.twitch.tv'
#HOST = 'localhost'
PORT = 6667


def handle_connexion(response, client):
    """
    Activate twitch capabilities and join channel.
    """
    if response.command != '001':
        return

    client.send(None, type='join')
    client.send('CAP REQ :twitch.tv/membership', type='raw')
    client.send('CAP REQ :twitch.tv/commands', type='raw')
    client.send('CAP REQ :twitch.tv/tags', type='raw')
    client.remove_handler(handle_connexion)


class Client(object):
    """ Connect to IRC and dispatch the messages to the handlers. """

    def __init__(self, pipe):
        self.pipe = pipe
        self.config = Configuration.get()
        self.socket = None
        self.handlers = []
        self.sender = Sender(self.config.channel)
        self.load_modules()

    def connect(self):
        if not self.config.oauth:
            logger.warning('No oauth token configured.')
            return
        if not self.config.username:
            logger.warning('No username configured.')
            return
        if not self.config.channel:
            logger.warning('No channel configured.')
            return

        if self.socket is not None:
            self.socket.close()

        self.socket = socket.socket()
        logger.debug('Connecting to {0}:{1}'.format(HOST, PORT))
        self.add_handler(handle_connexion)
        self.socket.connect((HOST, PORT))
        self.send('PASS {0}'.format(self.config.oauth), type='raw')
        self.send('NICK {0}'.format(self.config.username), type='raw')

    def send(self, message, type='privmsg'):
        self.sender.send(self.socket, type, message)

    def send_buffer(self):
        """ Send message if we have some buffered. """
        # Test socket to avoid race condition
        if self.socket is not None:
            self.sender.send_buffer(self.socket)

    def run(self):
        while True:
            self.send_buffer()
            try:
                response = self.socket.recv(1024).decode()
            except OSError:
                # Socket is probably close, let's wait until it's connected
                # FIXME Find a way to handle this cleanly
                import time
                time.sleep(5)
                continue
            for line in response.split('\n'):
                line = line.strip()
                if line:
                     logger.debug('< {0}'.format(line))
                     self.handle(Response(line))

    def load_modules(self):
        for module in self.config.get_activated_modules():
            self.load_module(module)

    def load_module(self, module):
        logger.debug('Loading module "{0}"'.format(module.identifier))
        module = module.get_module()
        for handler in module.handlers:
            self.add_handler(handler)

    def unload_module(self, module):
        for handler in module.handlers:
            self.remove_handler(handler)

    def add_handler(self, handler):
        self.handlers.append(handler)

    def remove_handler(self, handler):
        self.handlers.remove(handler)

    def handle(self, response):
        for handler in self.handlers:
            if handler(response, self):
                return


def run(pipe):
    client = Client(pipe)
    client.connect()
    client.run()
