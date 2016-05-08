""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from utils import db
from utils.modules import BaseModule

from .models import Strawpoll


class StrawpollModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'strawpoll'
    title = "Strawpoll"
    description = "Create polls and show the results on stream in real time"

    menus = [{
        "title": "Strawpoll",
        "icon": "pie-chart",
        "view": "strawpoll:list"
    }]

    def install(self):
        super(StrawpollModule, self).install()
        db.create_tables([Strawpoll])

    def uninstall(self):
        super(StrawpollModule, self).uninstall()
        db.drop_tables([Strawpoll])
