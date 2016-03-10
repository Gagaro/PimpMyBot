from __future__ import absolute_import, unicode_literals

from utils.api import Users
from .models import User


def get_user(username):
    user_data = Users.get(username)
    try:
        user = User.get(User.username == username)
        if user.display_name != user_data['display_name']\
                or user.type != user_data['type']:
            user.display_name = user_data['display_name']
            user.type = user_data['type']
            user.save()
    except User.DoesNotExist:
        user = User.create(
            username=user_data['username'],
            twitch_id=user_data['twitch_id'],
            display_name=user_data['display_name'],
            type=user_data['type'],
            created=user_data['created'],
        )
    return user


def handle_users(response, client):
    if response.command == '353':  # NAMES
        for username in response.data:
            get_user(username)
    elif response.command == 'JOIN':
        get_user(response.response_from)
    elif response.command == 'PART':
        pass
