""" Import the Base Module, A module is part of the bot who manage some stuff """
from utils.modules import BaseModule


def ping_handler(response, client):
    """ Handle the ping and send back a pong. """
    if response.command == 'PING':
        client.send('PONG {0}'.format(response.parameters), type='raw')
        return True


class PingModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'ping'
    title = "Ping"
    description = "Send Pong in response to the Pings"

    handlers = [ping_handler]
