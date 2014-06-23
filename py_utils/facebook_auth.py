#!/usr/bin/env python

import base64
import hashlib
import hmac
import json


def get_user_id(request):
    parsed = parse_signed_request(
        request.cookies.get('fbsr_665447500158300'),
        '0089bed38bc2aced1cd85020ffc4e527'
    )
    return parsed['user_id']


def urlsafe_b64decode(str):
    """Perform Base 64 decoding for strings with missing padding."""

    l = len(str)
    pl = l % 4
    return base64.urlsafe_b64decode(str.ljust(l + pl, "="))


def parse_signed_request(signed_request, secret):
    """
    Parse signed_request given by Facebook (usually via POST),
    decrypt with app secret.

    Arguments:
    signed_request -- Facebook's signed request given through POST
    secret -- Application's app_secret required to decrpyt signed_request
    """
    try:
        esig, payload = signed_request.split(".")
    except Exception:
        raise SignedRequestError("Malformed signed request", status_code=410)

    sig = urlsafe_b64decode(str(esig))
    try:
        data = json.loads(urlsafe_b64decode(str(payload)))
    except ValueError:
        raise SignedRequestError(
            "Payload is not a json string", status_code=410)

    if data["algorithm"].upper() != "HMAC-SHA256" or hmac.new(secret, payload, hashlib.sha256).digest() != sig:
        raise SignedRequestError("Not HMAC-SHA256 encrypted", status_code=410)

    return data


class SignedRequestError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
