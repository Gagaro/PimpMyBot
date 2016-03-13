from __future__ import absolute_import, unicode_literals

from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool

from peewee import IntegrityError

from utils import db
from utils.api import Users
from .models import User

# FIXME avoid importing module in each method


def update_user(username, current=True):
    from . import module as users_module

    user_data = Users.get(username)
    try:
        user = User.get(User.username == username)
        if user.display_name != user_data['display_name']\
                or user.type != user_data['type']:
            user.display_name = user_data['display_name']
            user.type = user_data['type']
        user.last_watched = datetime.now()
        user.save()
    except User.DoesNotExist:
        try:
            user = User.create(
                username=user_data['username'],
                twitch_id=user_data['twitch_id'],
                display_name=user_data['display_name'],
                type=user_data['type'],
                created=user_data['created'],
                first_watched=datetime.now(),
                last_watched=datetime.now(),
            )
        except IntegrityError:
            # Possible if there is a race condition
            pass
    if current:
        # Update current user list
        users_module.current_users[user.username] = user

# Avoid hitting the api or the db too much too fast
update_user_pool = ThreadPool(8)


def update_user_messages(user):
    if user.first_message is None:
        user.first_message = datetime.now()
    user.last_message = datetime.now()
    user.messages_count += 1
    user.save()


def handle_users(response, client):
    from . import module as users_module

    user = response.response_from
    if response.command == '353':  # NAMES
        update_user_pool.imap_unordered(update_user, response.data)
    elif response.command == 'JOIN':
        update_user_pool.apply_async(update_user, user)
    elif response.command == 'PART':
        update_user(user)
        del users_module.current_users[user]
    elif response.command == 'PRIVMSG':
        if user not in users_module.current_users.keys():
            update_user(user)
        update_user_messages(users_module.current_users[user])


def update_users_time_watched():
    """ Called every 60 seconds for now. """
    from . import module as users_module

    current_users = users_module.current_users.copy()
    for user in current_users.values():
        user.time_watched += 60
        user.save()
