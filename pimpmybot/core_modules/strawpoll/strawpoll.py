""" Import the Base Module, A module is part of the bot who manage some stuff """
from __future__ import absolute_import, unicode_literals

from utils import db
from utils.modules import BaseModule
from utils.translations import _

from .models import Strawpoll


def last_poll(client):
    poll = Strawpoll.select().order_by(Strawpoll.id.desc()).get()
    url = 'http://www.strawpoll.me/{0}'.format(poll.id)
    client.send(_('Last poll is {title} : {url}').format(title=poll.title, url=url))


class StrawpollModule(BaseModule):
    """ Module for the ping handler """
    identifier = 'strawpoll'
    title = "Strawpoll"
    description = _("Create polls and show the results on stream in real time")

    menus = [{
        "title": _("Strawpoll"),
        "icon": "pie-chart",
        "view": "strawpoll:list"
    }]

    api = {
        'last_poll': {
            'title': _('Last poll'),
            'method': last_poll
        }
    }

    def install(self):
        super(StrawpollModule, self).install()
        db.create_tables([Strawpoll])

    def uninstall(self):
        super(StrawpollModule, self).uninstall()
        db.drop_tables([Strawpoll])
