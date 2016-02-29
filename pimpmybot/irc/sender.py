from __future__ import absolute_import, unicode_literals

from logging import DEBUG
import time

import six

from utils.logging import get_logger

logger = get_logger('irc_sender', DEBUG)

# Max message per window
MAX_MESSAGE = 20
# Moderators can send 100 message per 30 seconds
MAX_MESSAGE_MOD = 100
# In seconds
WINDOW_SIZE = 30


class Sender(object):
    def __init__(self, channel):
        self.channel = channel
        self.buffer = []
        self.sent = {}

    # Handlers which generate the raw messages

    def raw(self, message, **kwargs):
        return message

    def who(self, message, **kwargs):
        return 'WHO #{0}'.format(self.channel)

    def join(self, message, **kwargs):
        return 'JOIN #{0}'.format(self.channel)

    def part(self, message, **kwargs):
        return 'PART #{0}'.format(self.channel)

    def privmsg(self, message, **kwargs):
        return 'PRIVMSG #{0} :{1}'.format(self.channel, message)

    def send(self, socket, type, message):
        """
        Prepare the message, add it to the buffer and try to send it.
        """
        if type not in ['raw', 'who', 'join', 'part', 'privmsg']:
            logger.warning('Unknown type: "{0}"'.format(type))
            return
        message = getattr(self, type)(message)
        logger.debug('> {0}'.format(message))
        if isinstance(message, six.text_type):
            message = message.encode('utf8')
        if message[-2:] != b'\r\n':
            message = message + b'\r\n'
        self.buffer.append(message)
        self.send_buffer(socket)

    def send_buffer(self, socket):
        """"
        Try to send all message in buffer without sending too much.
        """
        if not self.buffer:
            return

        # Update
        current_window = int(time.time()) - WINDOW_SIZE
        self.sent = {
            msg_time: count
            for msg_time, count in self.sent.items()
            if msg_time >= current_window
        }
        messages_allowed = MAX_MESSAGE - sum(self.sent.values())  # TODO Test if the bot is mod or not

        while self.buffer and messages_allowed > 0:
            # Update current messages count
            current_time = int(time.time())
            current_sent = self.sent.setdefault(current_time, 0)
            self.sent[current_time] = current_sent + 1

            # Send message
            messages_allowed -= 1
            message = self.buffer.pop(0)
            socket.send(message)
