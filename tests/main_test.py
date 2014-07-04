#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""

from models.Execution import Execution
from google.appengine.ext import testbed
from google.appengine.ext import ndb


import unittest
import json
import webtest

import main
from mock import patch, Mock

import pprint

pprint.PrettyPrinter(indent=2)


class MainTests(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        # needed because endpoints expects a . in this value
        self.testbed.setup_env(current_version_id='testbed.version')
        self.testbed.activate()
        self.testbed.init_all_stubs()
        self.app = main.app
        self.app.testing = True
        self.app_client = self.app.test_client()

    def api(self, uri='', method='get', args=None, status_code=200,
            content_type='application/json', auth_required=False):
        """ helper to make api calls """
        uri = "/api/" + uri
        if args is None:
            args = {}
        if auth_required is True:
            pass

        if method == 'get':
            response = self.app_client.get(uri, args)

        elif method == 'post':
            response = self.app_client.post(uri, args)

        elif method == 'delete':
            response = self.app_client.delete(uri, args)

        elif method == 'options':
            response = self.app_client.options(uri, args)

        # self.assertEqual(response.content_type, content_type)
        # self.assertEqual(response.status_code, status_code)
        if content_type == "application/json":
            json_obj = json.loads(response.data)
            self.assertEquals(json_obj[json_obj.keys()[0]]['version'], 1.0)
            return json_obj
        else:
            return response.data

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        Execution(owner=1234).put()
        Execution(owner=1234).put()
        key_to_check_is_present = Execution(owner=1234).put().urlsafe()
        key_to_check_is_not_present = Execution(owner=300).put().urlsafe()
        resp = self.api(uri='executions/', auth_required=True)
        self.assertEquals(resp.keys()[0], "collection")
        self.assertIn("/api/executions/create", resp['collection']['_links']['create']['href'])
        self.assertEquals(len(resp['collection']['items']), 3)

        # self.assertEquals(resp['collection']['_links'])
        print resp['collection']['items'][0]
        self.fail()
        # self.assertNotIn(
        #     {'execution_id': key_to_check_is_not_present}, resp['executions'])
        # self.assertIn(
        #     {'execution_id': key_to_check_is_present}, resp['executions'])


    def tearDown(self):
        self.testbed.deactivate()

    def test_execution_new(self):
        """ check that we can create a new execution"""
        pass

    def test_get_inputs_required(self):
        """ tests json schema load"""
        pass

    def test_execution_delete(self):
        """ test deleting an execution """
        pass

    def test_execution_resume(self):
        """ check that we can resume an execution"""
        pass

    def ftest_service_status(self):
        """ check that we can resume an execution"""
        expected = dict(fb='1', ndb='1')
        actual = self.api(uri='service_status')
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
