from __future__ import absolute_import, unicode_literals

from wsgi.app import app


class Message(object):
    """ Represent a message to show to the user """

    def __init__(self, message, level):
        self.message = message
        self.level = level

    def __str__(self):
        return self.message


def add_message(message, level):
    app.add_message(Message(message, level))


def success(message):
    add_message(message, 'success')


def info(message):
    add_message(message, 'info')


def warning(message):
    add_message(message, 'warning')


def danger(message):
    add_message(message, 'danger')
