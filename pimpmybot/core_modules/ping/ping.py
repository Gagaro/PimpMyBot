""" Import the Base Module, A module is part of the bot who manage some stuff """
from common.modules import BaseModule

def ping_handler(response, client):
    """ Handle the ping and send back a pong. """
    if response[:4] == 'PING':
        client.send('PONG {0}'.format(response[5:]))
        return True


class PingModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'ping'
    title = "Ping"
    description = "Send Pong in response to the Pings"

    handlers = [ping_handler]
