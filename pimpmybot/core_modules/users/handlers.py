from __future__ import absolute_import, unicode_literals

from datetime import datetime
from logging import DEBUG
from multiprocessing.dummy import Pool as ThreadPool

from peewee import IntegrityError

from utils.api import Users
from utils.logging import get_logger
from .models import User

logger = get_logger('users', DEBUG)


def update_user(username, users_module=None):
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
                created=user_data['created'],
                first_watched=datetime.now(),
                last_watched=datetime.now(),
            )
        except IntegrityError:
            # Possible if there is a race condition
            pass
    if users_module is not None:
        # Update current user list
        users_module.current_users[user.username] = user
    return user


def update_user_messages(user):
    if user.first_message is None:
        user.first_message = datetime.now()
    user.last_message = datetime.now()
    user.messages_count += 1
    user.save()


# Avoid hitting the api or the db too much too fast
update_user_pool = None

def handle_users(response, client):
    global update_user_pool
    # We need to initialize it here so we are sure this is done in the right process.
    if update_user_pool is None:
        update_user_pool = ThreadPool(8)

    users_module = client.get_module('users')

    user = response.response_from
    if response.command == '353':
        # NAMES
        for user in response.data:
            update_user_pool.apply_async(update_user, args=(user, users_module))
    elif response.command == 'JOIN':
        # JOIN
        update_user_pool.apply_async(update_user, args=(user, users_module))
    elif response.command == 'MODE':
        # MODE
        user = update_user(response.data['user'], users_module)
        if user.type == 'user' and response.data['action'] == 'add':
            user.type = 'mod'
            user.save()
        elif user.type == 'mod' and response.data['action'] == 'remove':
            user.type = 'user'
            user.save()
    elif response.command == 'PART':
        # PART
        def handle_part(user, users_module):
            update_user(user, users_module)
            del users_module.current_users[user]
        update_user_pool.apply_async(handle_part, args=(user, users_module))
    elif response.command == 'PRIVMSG':
        # PRIVMSG
        # We also look for the user type
        if '#' + user == response.data['target']:
            user_type = "broadcaster"
        elif response.tags['user-type']:
            user_type = response.tags['user-type']
        else:
            user_type = "user"

        def handle_privmsg(user, users_module):
            if user not in users_module.current_users.keys():
                user = update_user(user, users_module)
            update_user_messages(user)
            if user.type != user_type:
                user.type = user_type
                user.save()
        update_user_pool.apply_async(handle_privmsg, args=(user, users_module))
