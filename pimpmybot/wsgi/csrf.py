from __future__ import absolute_import, unicode_literals

import hashlib
import os

from bottle import request, abort, response


ROOT = '/'
CSRF_TOKEN = '_csrf_token'
EXPIRES = 600  # seconds
ENCODING = 'utf8'
SECRET = None


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
    global SECRET

    if SECRET is None:
        # Avoid circular import
        from utils.config import Configuration
        SECRET = Configuration.get().secret

    sha256 = hashlib.sha256()
    sha256.update(os.urandom(8))
    token = sha256.hexdigest().encode(ENCODING)
    response.set_cookie(CSRF_TOKEN, token, path=ROOT,
                        secret=SECRET, max_age=EXPIRES)
    request.csrf_token = token.decode(ENCODING)


def require_csrf(callback):
    """ Bottle module to automatically check csrf protection """
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            token_csrf = request.get_cookie(CSRF_TOKEN, secret=SECRET, default=b'').decode('utf8')
            csrf = request.headers.get('X-CsrfToken', None)
            if csrf is None:
                csrf = request.forms.get(CSRF_TOKEN, None)
            if csrf is None or csrf != token_csrf:
                abort(400)
        generate_csrf_token()
        body = callback(*args, **kwargs)
        return body

    return wrapper
