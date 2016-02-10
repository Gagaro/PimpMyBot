class BaseHandler(object):
    """ Base class for IRC messages handler. """

    def handle(self, response, client):
        """
        This should return True if the message shouldn't be handled
        by remaining handlers.
        """
        raise NotImplementedError()


class PingHandler(BaseHandler):
    """ Handle the ping and send back a pong. """
    def handle(self, response, client):
        if response[:4] == 'PING':
            client.send('PONG {0}'.fomat(response[5:]))
            return True
