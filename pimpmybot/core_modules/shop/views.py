from __future__ import absolute_import, unicode_literals

import json

import requests
from bottle import redirect, request, HTTPResponse

from utils.translations import _
from wsgi import app
from wsgi.bottle import jinja2_view
from wsgi.messages import success, danger

from .models import ShopItem, BoughtItem

route = app.route


@route('/shop/', name='shop:items')
@jinja2_view('shop_items')
def shop_items():
    items = ShopItem.select().order_by(ShopItem.name.desc())
    return {
        'items': items
    }


@route('/shop/item', name='shop:item', method='POST')
def shop_add_item():
    name = request.forms['name']
    price = int(request.forms['price'])
    active = bool(request.forms.get('active', False))
    try:
        ShopItem.create(name=name, price=price, active=active)
        success(_("Item created successfully"))
    except:
        danger(_("Error while creating item."))
    return redirect(app.get_url('shop:items'))


@route('/shop/item/<item_id:int>/', name='shop:item_detail', method='PUT')
def shop_edit_item(item_id):
    # TODO
    return {}


@route('/shop/item/<item_id:int>/', name='shop:item_detail')
@jinja2_view('shop_item_detail')
def shop_list_item_detail(item_id):
    item = ShopItem.get(id=item_id)
    return {
        'item': item
    }


@route('/shop/bought/<bought_id:int>/', name='shop:ajax:bought_toggle', method='PUT')
def shop_validate_bought_item(bought_id):
    bought_item = BoughtItem.get(id=bought_id)
    bought_item.validated = not bought_item.validated
    bought_item.save()
    return HTTPResponse('OK')
