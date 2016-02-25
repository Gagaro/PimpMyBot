import time
import six

from utils.logging import get_logger
from logging import DEBUG

logger = get_logger('irc_sender', DEBUG)

MAX_MESSAGE = 20
PER_X_SECONDS = 30

class Sender(object):

    def __init__(self):
        self.is_active = False
        self.irc_client = None
        self.channel = None
        self.buffer = []
        self.last_reset = time.time() #just for init (time in sec)
        self.nb_send_since_reset = 0

    def configure(self, irc_client):

        if irc_client is None:
            logger.debug('ERROR - irc_client is null, sender configuration abort')
            return
        elif irc_client.socket is None:
            logger.debug('ERROR - irc_client not connected, sender configuration abort')
            return

        self.is_active = True
        self.irc_client = irc_client
        self.channel = irc_client.config.channel

    def send_list(self):

        logger.debug('buffer = {0}'.format(self.buffer))

        if len(self.buffer) <= 0:
            return

        #each X seconds, reset counter
        timeElapsed = time.time() - self.last_reset
        if timeElapsed >= PER_X_SECONDS:
            self.nb_send_since_reset = 0
            timeElapsed = 0
            self.last_reset = time.time()

        #can't send message because of mess limit
        if self.nb_send_since_reset >= MAX_MESSAGE:
                return

        #send all mess in the buffer with
        for mess in self.buffer[:]:
            if  self.nb_send_since_reset < MAX_MESSAGE:
                self.nb_send_since_reset = self.nb_send_since_reset + 1
                self.send(mess)
                self.buffer.remove(mess)
            else:
                break

    def send(self,message):
        """
        Send a raw message to the IRC channel.
        """
        if self.is_active:
            logger.debug('> {0}'.format(message))
            if isinstance(message, six.text_type):
                message = message.encode('utf8')
            if message[-2:] != b'\r\n':
                message = message + b'\r\n'
            self.irc_client.socket.send(message)
        else:
             logger.debug('WARNING - irc_sender is not active')

    def raw(self, raw_message):
        self.buffer.append(raw_message)

    def who(self):
        self.buffer.append('WHO #{0}'.format(self.irc_client.config.channel))

    def join(self):
        self.buffer.append('JOIN #{0}'.format(self.irc_client.config.channel))

    def part(self):
        self.buffer.append('PART #{0}'.format(self.irc_client.config.channel))

    def msg(self, msg):
        self.buffer.append('PRIVMSG #{0} :{1}'.format(self.irc_client.config.channel, msg))

