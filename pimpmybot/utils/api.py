"""
Class helpers to help interacting with Twitch api.
"""
import dateutil.parser
import requests

CLIENT_ID = 'fv6qtw5h3065oncwqpyzud1bb9s10ld'


class BaseApi(object):

    _oauth = None

    @property
    @classmethod
    def oauth(cls):
        if cls._oauth is None:
            from utils.config import Configuration

            cls._oauth = Configuration.get().oauth
        return cls._oauth

    @classmethod
    def _get(self, path, version=3):
        if path[0] != '/':
            path = '/' + path
        url = 'https://api.twitch.tv/kraken{0}'.format(path)
        headers = {
            'Accept': 'application/vnd.twitchtv.v{0}+json'.format(version),
            'Authorization': 'OAuth {0}'.format(self.oauth),
            'Client-ID': CLIENT_ID,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response


class Users(BaseApi):
    _users = {}

    @classmethod
    def get(cls, username):
        # FIXME This method needs to be thread safe
        if username not in cls._users.keys():
            data = cls._get('/users/{0}'.format(username)).json()
            cls._users[username] = {
                'username': data['name'],
                'display_name': data['display_name'],
                'created': dateutil.parser.parse(data['created_at']),
                'twitch_id': data['_id'],
                'type': data.get('type', 'user'),
            }
        return cls._users[username]
