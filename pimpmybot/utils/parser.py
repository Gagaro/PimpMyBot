import re

# Regular expression for fast parsing
RESPONSE_RE = re.compile('^(?:(?P<tags>@[^ ]+) )?(?::(?P<from>[^ ]+) )?(?P<command>\w+) (?P<parameters>.+)$')
PRIVMSG_RE = re.compile('^(?P<target>#?\w+) :(?P<message>.*)$')


def parse_privmsg(response):
    """
    Return a dict with the target, the message and the command if there is one.
    """
    data = PRIVMSG_RE.match(response['parameters']).groupdict()
    if data['message'][0] == '!':
        data['command'] = data['message'][1:].split(' ', 1)[0]
    else:
        data['command'] = None
    return data


# Command to callback method parsing data from the parameters
GET_COMMAND_DATA = {
    'PRIVMSG': parse_privmsg,
}


def parse_irc_response(response_string):
    """
    Parse the irc response and return a dict.

    `parameters` is the raw string after the command.
    `data` is parsed data from the `parameters` string depending on the `command`.

    :example
    {
        'tags': {
            'color': '#0D4200',
        },
        'from': 'twitch_username!twitch_username@twitch_username.tmi.twitch.tv',
        'command': 'PRIVMSG',
        'parameters': '#channel :Kappa Keepo Kappa',
        'data': {
            'target': '#channel',
            'message': 'Kappa Keepo Kappa',
        }
    }
    """
    response = RESPONSE_RE.match(response_string).groupdict()
    if response['command'] in GET_COMMAND_DATA.keys():
        response['data'] = GET_COMMAND_DATA[response['command']](response)
    return response
