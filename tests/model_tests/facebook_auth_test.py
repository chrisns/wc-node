#!/usr/bin/env python
"""This is for testing facebook authentication with mocks"""

import endpoints
import unittest
import json
import wc_api
from mock import patch, Mock
from collections import namedtuple


class FacebookAuthTests(unittest.TestCase):

    @patch('wc_api.urllib2.urlopen')
    def test_facebook_auth_fail_non_same_id(self, mock_urlopen):
        """ test that authentication fails when the token isn't for the user_id given """
        request_structure = namedtuple('MyStruct', 'user_id token')
        request = request_structure(user_id=1234, token='lala')
        mock = Mock()
        mock.read.side_effect = [json.dumps({'id': 12342})]
        mock_urlopen.return_value = mock
        self.assertRaises(
            endpoints.UnauthorizedException, wc_api.check_authentication, request)

    @patch('wc_api.urllib2.urlopen')
    def test_facebook_auth_fail_no_response(self, mock_urlopen):
        request_structure = namedtuple('MyStruct', 'user_id token')
        request = request_structure(user_id=1234, token='lala')
        mock = Mock()
        mock.read.side_effect = ['no_json']
        mock_urlopen.return_value = mock
        self.assertRaises(
            endpoints.UnauthorizedException, wc_api.check_authentication, request)

    @patch('wc_api.urllib2.urlopen')
    def test_facebook_auth_success(self, mock_urlopen):
        request_structure = namedtuple('MyStruct', 'user_id token')
        request = request_structure(user_id=1234, token='lala')
        mock = Mock()
        mock.read.side_effect = [json.dumps({'id': 1234})]
        mock_urlopen.return_value = mock
        self.assertIsNone(wc_api.check_authentication(request))


if __name__ == '__main__':
    unittest.main()
