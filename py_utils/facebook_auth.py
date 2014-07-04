#!/usr/bin/env python
# coding=utf-8

import base64
import hashlib
import hmac
import json

class facebook_auth:
    def get_user_id(self, request):
        """
        Get the user id based on the request
        @param request: flask request object
        @return: integer of user id
        """
        parsed = parse_signed_request(
            request.cookies.get('fbsr_665447500158300'),
            '0089bed38bc2aced1cd85020ffc4e527'
        )
        return parsed['user_id']


    def urlsafe_b64decode(self, b64string):
        """Perform Base 64 decoding for strings with missing padding.
        @param b64string:
        """

        l = len(b64string)
        pl = l % 4
        return base64.urlsafe_b64decode(b64string.ljust(l + pl, "="))


    def parse_signed_request(self, signed_request, secret):
        """
        Parse signed_request given by Facebook (usually via POST),
        decrypt with app secret.

        @param signed_request: Facebook's signed request given through POST
        @param secret: Application's app_secret required to decrpyt signed_request
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
    """
    Exception handler for invalid signed requests
    @param message:
    @param status_code:
    @param payload:
    """
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
