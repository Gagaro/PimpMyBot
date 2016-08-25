from __future__ import absolute_import, unicode_literals

import json

import requests
from bottle import redirect, request, HTTPResponse

from utils.translations import _
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success, danger

from .models import Bet, Answer

route = app.route


@route('/bets/', name='bet:list')
@jinja2_view('bets_list')
def bets_list():
    bets = Bet.select().order_by(Bet.id.desc())
    return {
        'bets': bets
    }


@route('/bets/', name='bet:detail', method='POST')
def bet_add_bet():
    question = request.forms['question']
    options = request.forms['options']
    initial_pot = int(request.forms['initial-pot'])
    try:
        min_amount = int(request.forms['min-amount'])
    except ValueError:
        min_amount = None
    try:
        max_amount = int(request.forms['max-amount'])
    except ValueError:
        max_amount = None
    try:
        bet = Bet.create(question=question, options=options, initial_pot=initial_pot,
                         min_amount=min_amount, max_amount=max_amount)
        app.irc_send(action="message", parameters="New bet! {0}".format(bet.question))
        for index, option in enumerate(bet.get_options(), start=1):
            app.irc_send(action="message", parameters="{0}. {1}".format(index, option))
        success(_("Bet created successfully"))
    except Exception as e:
        danger(_("Error while creating bet: {0}.").format(e))
    return redirect(app.get_url('bet:list'))


@route('/bets/<bet_id:int>/', name='bet:detail')
@jinja2_view('bet_detail')
def bet_detail(bet_id):
    bet = Bet.get(id=bet_id)
    return {
        'bet': bet
    }
