#!/usr/bin/env python
# coding=utf-8
""" facebook authentication tests """

from py_utils_tests.facebook_auth import *

import unittest
import base64
from mock import MagicMock


class TestFacebookAuth(unittest.TestCase):
    signed_request = 'vAa5ctS3c9yXVlczIkcVWnV6UL__pZH64TQdaKsg-jc.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUFuNGpkRG91cGYxNmNhQndOc0xMa3ZhSHZnRVlDUURXbmhjSDRwQmp0ZWxaclZxZkpNazRkUmtuZmkzVXZwQkM1cEZsNU5jNkxhMURlOGlERGJPZWtab24tTDdFdThIWmlfNHdSWngwdUJ1Z0pmaGFrNUxsZWp3VkszUS00TTVFX09MLWhuWEttVDJqdno3ZjRHYWZGeHdibkJvc2dGZlBXYV9fVVNNTWZ5ckhNbmhyZFJfcHo2TEV0UjBzcUREQzlUZUJlaE9hRUlMWWxPbHdDakY1V1JVdlNFd1I1LVlybTFBcFhFV1pHc3dUT1QzVUVDZXVWRUpLd1VweW1xd3phalp5dldmRno2eWZpaFlHazl4eENKd0xNeUpOT1Y2R3VvdDBKSUktMUNqTjByS1RELUdBUWxpNVlkSW9kU1pyYyIsImlzc3VlZF9hdCI6MTQwMzUyMDM2MCwidXNlcl9pZCI6IjczOTE0OTA4MiJ9'
    secret = '0089bed38bc2aced1cd85020ffc4e527'
    fake_request = MagicMock()
    fake_request.cookies.get.return_value = signed_request

    def test_parse_signed_request_success(self):
        """ test that we can decrypt a signed request successfully """
        expected = {
            'issued_at': 1403520360,
            'algorithm': 'HMAC-SHA256',
            'user_id': '739149082',
            'code': 'AQAn4jdDoupf16caBwNsLLkvaHvgEYCQDWnhcH4pBjtelZrVqfJMk4dRknfi3UvpBC5pFl5Nc6La1De8iDDbOekZon-L7Eu8HZi_4wRZx0uBugJfhak5LlejwVK3Q-4M5E_OL-hnXKmT2jvz7f4GafFxwbnBosgFfPWa__USMMfyrHMnhrdR_pz6LEtR0sqDDC9TeBehOaEILYlOlwCjF5WRUvSEwR5-Yrm1ApXEWZGswTOT3UECeuVEJKwUpymqwzajZyvWfFz6yfihYGk9xxCJwLMyJNOV6Guot0JII-1CjN0rKTD-GAQli5YdIodSZrc'}
        actual = parse_signed_request(self.signed_request, self.secret)
        self.assertEqual(expected, actual)

    def test_parse_signed_request_malformed(self):
        """ check we error if signed request is malformed """
        with self.assertRaises(SignedRequestError) as ex:
            parse_signed_request('malformed', 'secret')
        self.assertEqual('Malformed signed request', ex.exception.message)

    def test_parse_signed_request_not_json(self):
        """ check we error if there is no json in payload """
        payload_raw = 'not_json'
        payload = base64.urlsafe_b64encode(
            payload_raw.ljust(len(payload_raw) + len(payload_raw) % 4, "="))
        sig = base64.urlsafe_b64encode(
            hmac.new(self.secret, payload, hashlib.sha256).digest())
        signed_request = sig + '.' + payload_raw
        with self.assertRaises(SignedRequestError) as ex:
            parse_signed_request(signed_request, self.secret)
        self.assertEqual('Payload is not a json string', ex.exception.message)

    def test_parse_signed_request_algo_failure(self):
        """ test that we error on algorithm fails """
        bad_secret = '0089bed38bc2aced1cd85020ffc4e528'
        with self.assertRaises(SignedRequestError) as ex:
            parse_signed_request(self.signed_request, bad_secret)
        self.assertEqual('Not HMAC-SHA256 encrypted', ex.exception.message)

    def test_urlsafe_b64decode(self):
        """ test base 64 decode """
        expected = 'm\xb7\x1fi\xf6\x9f'
        actual = urlsafe_b64decode('bbcfafaf')
        self.assertEqual(expected, actual)

    def test_get_user_id(self):
        """ test we can get a user id from a mocked request """
        expected = '739149082'
        actual = get_user_id_from_request(self.fake_request)
        self.assertEqual(expected, actual)

    def test_signed_request_error_exception(self):
        """ test our exception handler """
        expected = {
            'status_code': 123,
            'message': 'error message',
            'payload': None
        }
        with self.assertRaises(SignedRequestError) as ex:
            raise SignedRequestError("error message", status_code=123)
        actual = ex.exception.__dict__
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
