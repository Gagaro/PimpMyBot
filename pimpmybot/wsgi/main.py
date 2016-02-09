import os

import bottle
from bottle import route, run as bottle_run, template

BASE_DIR = os.path.dirname(__file__)

bottle.TEMPLATE_PATH = [os.path.join(BASE_DIR, './templates/')]


@route('/')
def index():
    return template('index')


def run(pipe=None):
    bottle_run(host='localhost', port=8000)


if __name__ == '__main__':
    run()
