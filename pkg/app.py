# -*- coding: utf-8 -*-
from __future__ import absolute_import
import hashlib
import hmac
import logging
from functools import wraps

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request
from flask import Response

from .config import webhook_secret
from .exceptions import SkipUpdate
from .update import update_package


log = logging.getLogger(__name__)

app = Flask(__name__.split('.', 1)[0])


def require_secret(f):
    fail_response = Response('Secret mismatch', 400)

    def signatures_match(request, key):
        h = hmac.new(key, request.data, hashlib.sha1)
        return hmac.compare_digest('sha1=' + h.hexdigest(),
                                   str(request.headers['X-Hub-Signature']))

    @wraps(f)
    def wrapper(*args, **kwargs):
        if webhook_secret:
            if 'X-Hub-Signature' not in request.headers or \
               not signatures_match(request, webhook_secret):
                return fail_response
        else:
            if 'X-Hub-Signature' in request.headers:
                return fail_response
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    return 'Hello, world'


@app.route('/webhook', methods=['POST'])
@require_secret
def post_webhook():
    commit = request.get_json()
    try:
        update_package(commit)
    except SkipUpdate as e:
        resp = {'status': 'skipped', 'message': repr(e)}
        status = 400
    except Exception as e:
        log.exception('Error processing commit message')
        resp = {'status': 'error', 'message': repr(e)}
        status = 400
    else:
        resp = {'status': 'success', 'message': 'package updated'}
        status = 200
    return make_response(jsonify(resp), status)
