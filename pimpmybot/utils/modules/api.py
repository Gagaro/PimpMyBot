""" Default methods accessible in the modules api. """
from utils.modules.parameters import CharParameter
from utils.translations import _


def send_message(response, client, message):
    client.send(message)


api = {
    'send_message': {
        'title': _('Send a message'),
        'method': send_message,
        'parameters': [
            CharParameter('message', title="Message"),
        ]
    },
}
