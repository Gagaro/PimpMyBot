def update_users_time_watched(current_users):
    """ Called every 60 seconds for now. """
    for user in current_users.values():
        user.time_watched += 60
        user.save()
