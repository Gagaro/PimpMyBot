from __future__ import absolute_import, unicode_literals

import json

import requests
from bottle import redirect, request, HTTPResponse

from utils.translations import _
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success, danger

from .models import Money
from .utils import get_configuration

route = app.route


@route('/money/settings', name='money:settings')
@jinja2_view('money_settings')
def money_settings():
    return {'config': get_configuration()}

@route('/money/settings', name='money:settings', method="POST")
@jinja2_view('money_settings')
def money_settings_post():
    configuration = get_configuration()
    configuration.money_name = request.forms['money_name']
    configuration.amount_gain_inactive = int(request.forms['amount_gain_inactive'])
    configuration.amount_gain_active = int(request.forms['amount_gain_active'])
    configuration.gain_interval = int(request.forms['gain_interval'])
    configuration.save()
    success('Configuration saved')
    return {
        'config': configuration,
    }


@route('/money/list', name='money:list')
@jinja2_view('money_list')
def money_list():
    return {
        'moneys': Money.select()
    }


@route('/money/user/', name='money:ajax:user', method='POST')
def money_user_edit_ajax():
    id = int(request.forms['user_id'])
    amount = int(request.forms['amount'])
    Money.update(amount=amount).where(Money.user == id).execute()
    return HTTPResponse('OK')
