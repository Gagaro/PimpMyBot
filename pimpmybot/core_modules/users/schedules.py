def update_users_time_watched(users_module):
    """ Called every 60 seconds for now. """
    current_users = users_module.current_users.copy()
    for user in current_users.values():
        user.time_watched += 60
        user.save()
