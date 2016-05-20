from __future__ import absolute_import, unicode_literals

import hashlib
import os

import six
from bottle import request, abort, response


ROOT = '/'
CSRF_TOKEN = '_csrf_token'
EXPIRES = 1800  # seconds
ENCODING = 'utf8'
SECRET = None


def get_secret():
    """ Get secret """
    global SECRET

    if SECRET is None:
        # Avoid circular import
        from utils.config import Configuration
        SECRET = Configuration.get().secret
    return SECRET


def get_csrf_token():
    """ Get the csrf_token and return it. """
    token_csrf = request.get_cookie(CSRF_TOKEN, secret=get_secret(), default=b'')
    if isinstance(token_csrf, six.binary_type):
        token_csrf = token_csrf.decode(ENCODING)
    return token_csrf


def generate_csrf_token():
    """
    Generate and set new CSRF token in cookie. The generated token is set to
    ``request.csrf_token`` attribute for easier access by other functions.
    It is generally not necessary to use this function directly.
    .. warning::
       This function uses ``os.urandom()`` call to obtain 8 random bytes when
       generating the token. It is possible to deplete the randomness pool and
       make the random token predictable.

    From https://github.com/Outernet-Project/bottle-utils/blob/master/bottle_utils/csrf.py
    """
    sha256 = hashlib.sha256()
    sha256.update(os.urandom(8))
    token = sha256.hexdigest().encode(ENCODING)
    response.set_cookie(CSRF_TOKEN, token, path=ROOT,
                        secret=get_secret(), max_age=EXPIRES)


def require_csrf(callback):
    """ Bottle module to automatically check csrf protection """
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            token_csrf = get_csrf_token()
            csrf = request.headers.get('X-CsrfToken', None)
            if csrf is None:
                csrf = request.forms.get(CSRF_TOKEN, None)
            if csrf is None or csrf != token_csrf:
                # Regenerate token to avoid deadlocking in case of bad formatted cookie
                generate_csrf_token()
                abort(400, 'CSRF')
        elif not request.get_cookie(CSRF_TOKEN, secret=SECRET, default=b''):
            generate_csrf_token()
        # set token on request to have it in the template
        request.csrf_token = get_csrf_token()
        body = callback(*args, **kwargs)
        return body

    return wrapper
