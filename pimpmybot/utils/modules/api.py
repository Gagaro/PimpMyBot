""" Default methods accessible in the modules api. """
from utils.modules.parameters import CharParameter
from utils.translations import _


def send_message(client, message):
    # TODO
    raise NotImplementedError


api = [
    {
        'title': _('Send a message'),
        'method': send_message,
        'parameters': {
            'message': CharParameter(),
        }
    },
]
