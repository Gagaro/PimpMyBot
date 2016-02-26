import re

# Regular expression for fast parsing
RESPONSE_RE = re.compile('^(?:@(?P<tags>[^ ]+) )?(?::(?P<from>[^ ]+) )?(?P<command>\w+)(?: (?P<parameters>.+))?$')
PRIVMSG_RE = re.compile('^(?P<target>#?\w+) :(?P<message>.*)$')


class Response(object):
    """
    Class responsible for the parsing of the irc response.
    """

    __slots__ = ['tags', 'response_from', 'command', 'parameters', '_data']

    def __init__(self, response):
        response = RESPONSE_RE.match(response).groupdict()
        self.tags = self.parse_tags(response['tags'])
        self.response_from = response['from']
        self.command = response['command']
        self.parameters = response['parameters']
        self._data = None

    def parse_tags(self, tags):
        tags_dict = {}
        if tags is None:
            return tags_dict
        tags = tags.split(';')
        for tag in tags:
            key, value = tag.split('=', 1)
            tags_dict[key] = value
        return tags_dict

    @property
    def data(self):
        """ Data is calculated only if needed and only once. """
        if self._data is None and self.command in self.GET_COMMAND_DATA.keys():
            self._data = self.GET_COMMAND_DATA[self.command](self)
        return self._data

    def _parse_privmsg(self):
        """
        Return a dict with the target, the message and the command if there is one.

        :example:

        PRIVMSG #channel :!test a message

        {
            'target': '#channel',
            'message': '!test a message',
            'command': 'test',
        }
        """
        data = PRIVMSG_RE.match(self.parameters).groupdict()
        if data['message'][0] == '!':
            data['command'] = data['message'][1:].split(' ', 1)[0]
        else:
            data['command'] = None
        return data

    # Command to callback method parsing data
    GET_COMMAND_DATA = {
        'PRIVMSG': _parse_privmsg,
    }
