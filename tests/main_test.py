#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""

from models.Execution import Execution
from google.appengine.ext import testbed
from google.appengine.ext import ndb
# import py_utils.facebook_auth
from SpiffWorkflow import *

from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
import unittest
import json
import webtest

import main
from mock import patch, Mock, MagicMock
import sys
# sys.path.append('./py_utils')
# from facebook_auth import *
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

    def tearDown(self):
        self.testbed.deactivate()

    @patch('py_utils.facebook_auth.facebook_auth.get_user_id')
    def api(self, mock_get_user_id=None, uri='', method='get', args=None, status_code=200,
            content_type='application/json', user_id=None):
        """ helper to make api calls """
        uri = "/api" + uri
        if args is None:
            args = {}

        mock_get_user_id.return_value = user_id

        if method == 'get':
            response = self.app_client.get(uri, args)

        elif method == 'post':
            response = self.app_client.post(uri, args)

        elif method == 'delete':
            response = self.app_client.delete(uri, args)

        elif method == 'options':
            response = self.app_client.options(uri, args)

        self.assertEqual(response.content_type, content_type)
        self.assertEqual(response.status_code, status_code)
        if response.content_type == "application/json" and status_code is 200:
            json_obj = json.loads(response.data)
            self.assertEquals(json_obj[json_obj.keys()[0]]['version'], 1.0)
            return json_obj
        else:
            return response

    def test_root_route(self):
        """ check that we can get the api router """
        resp = self.api(uri='')
        self.assertEquals(resp.keys()[0], "collection")
        self.assertEquals(len(resp['collection']['items']), 1)
        self.assertIn('executions', resp['collection']['items'])

    def test_list_executions_requires_auth(self):
        """ check that list executions requires authentication """
        resp = self.api(uri='/executions', status_code=400)
        self.assertEqual({"message": "User not authenticated"}, json.loads(resp.data))

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        keys_to_expect = []
        keys_to_expect.append(Execution(owner=1234).put().urlsafe())
        keys_to_expect.append(Execution(owner=1234).put().urlsafe())
        keys_to_expect.append(Execution(owner=1234).put().urlsafe())

        key_not_to_expect = Execution(owner=300).put().urlsafe()

        resp = self.api(uri='/executions', user_id=1234)

        self.assertEquals(resp.keys()[0], "collection")
        self.assertIn("/api/executions/create", resp['collection']['_links']['create']['href'])
        self.assertEquals(len(resp['collection']['items']), 3)

        for item in resp['collection']['items']:
            self.assertEqual('Execution', item['type'])
            self.assertIn(item['execution_id'], keys_to_expect)
            self.assertIn('/api/executions/' + item['execution_id'], item['href'])
            self.assertIn('href', item.keys())
            self.assertIn('created', item.keys())
            self.assertIn('execution_id', item.keys())
            self.assertNotEqual(key_not_to_expect, item['execution_id'])

    def test_page_not_found(self):
        resp = self.api(uri='/notfound', status_code=404)
        self.assertEqual({"message": "Sorry, Nothing at this URL."}, json.loads(resp.data))

    def test_execution_new(self):
        """ check that we can create a new execution"""
        resp = self.api(uri='/executions/create', user_id=1234, status_code=302, content_type='text/html; charset=utf-8')
        self.assertIn('You should be redirected automatically', resp.data)
        self.assertIn('api/executions/', resp.headers['Location'])

    def test_get_execution(self):
        execution_object = Execution(owner=1234)
        spec_file = main.get_workflow_spec_file_handler().read()
        spec = JSONSerializer().deserialize_workflow_spec(spec_file)
        execution = Workflow(spec)
        execution.complete_all()
        execution_object.data = execution.serialize(DictionarySerializer())
        execution_id = execution_object.put().urlsafe()
        resp = self.api(uri='/executions/' + execution_id, user_id=1234)
        print resp
        self.fail()
    def test_get_inputs_required(self):
        """ tests json schema load"""
        pass

    def test_execution_delete(self):
        """ test deleting an execution """
        pass

    def test_execution_resume(self):
        """ check that we can resume an execution"""
        pass



if __name__ == '__main__':
    unittest.main()  # pragma: no cover
