from __future__ import absolute_import, unicode_literals

import json

import requests
from bottle import redirect, request

from utils.translations import _
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success, danger

from .models import Strawpoll

route = app.route

API_URL = 'https://strawpoll.me/api/v2/polls'


@route('/strawpoll', name='strawpoll:list')
@jinja2_view('strawpoll_list')
def strawpoll_list():
    polls = Strawpoll.select().order_by(Strawpoll.id.desc())
    return {
        'polls': polls,
    }


@route('/strawpoll', name='strawpoll:list', method="POST")
def strawpoll_create():
    """ View to create a new post """
    if 'goto' in request.forms.keys():
        return redirect(app.get_url('strawpoll:stream_detail', id=request.forms['poll_id']))
    url = API_URL
    data = {
        'title': request.forms['title'],
        'options': request.forms['options'].replace('\r', '').split('\n'),
        'multi': bool(request.forms.get('multi', False)),
        # 'dupcheck': 'disabled',
    }
    r = requests.post(url, data=json.dumps(data))
    if r.ok:
        data = r.json()
        Strawpoll.create(id=data['id'], title=data['title'])
        success(_('Poll created successfully.'))
    else:
        danger(_('Error while creating poll: {0}'.format(r.json().get('errorMessage', 'Unkown'))))
    return redirect(app.get_url('strawpoll:list'))


@route('/strawpoll/stream/<id:int>', name='strawpoll:stream_detail')
@jinja2_view('strawpoll_stream_detail')
def strawpoll_clr_detail(id):
    """ View to get detail on a single poll to show in clr browser """
    try:
        poll = Strawpoll.get(id=id)
    except Strawpoll.DoesNotExist:
        poll = None
    return {'poll': poll, 'poll_id': id, 'api_url': API_URL}


@route('/strawpoll/stream/last', name='strawpoll:stream_detail_last')
@jinja2_view('strawpoll_stream_detail')
def strawpoll_clr_detail_last():
    """ View to get detail on a last poll to show in clr browser """
    poll = Strawpoll.select().order_by(Strawpoll.id.desc())[:1][0]
    return {'poll': poll, 'api_url': API_URL}


@route('/strawpoll/ajax/<id:int>', name='strawpoll:ajax_detail')
def strawpoll_ajax_detail(id):
    """ View to get detail on a single poll to show in clr browser """
    return requests.get('{0}/{1}'.format(API_URL, id)).json()