#!/usr/bin/env python
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying to figure why things are broken"""

from models.Execution import Execution
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from SpiffWorkflow.specs import *
from SpiffWorkflow.operators import *
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.Task import *

import endpoints
import unittest
import json
import webtest

import wc_api
from mock import patch, Mock

from tests.TestWorkflowSpec import TestWorkflowSpec
import pprint
pprint.PrettyPrinter(indent=2)


class TestApiTests(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        # needed because endpoints expects a . in this value
        self.testbed.setup_env(current_version_id='testbed.version')
        self.testbed.activate()
        self.testbed.init_all_stubs()
        app = endpoints.api_server([wc_api.WCApi], restricted=False)
        self.app = webtest.TestApp(app)

    @patch('wc_api.get_workflow_spec_file_handler')
    @patch('urllib2.urlopen')
    def api(self, mock_urlopen=None, mock_file_open=None, method=None, args=None, status_code=200, content_type='application/json', auth_required=False):
        """ helper to make api calls """
        if args is None:
            args = {}
        if auth_required is True:
            args['user_id'] = 1234
            args['token'] = 'lala'
            mock = Mock()
            mock.read.side_effect = [json.dumps({'id': 1234})]
            mock_urlopen.return_value = mock
        # mock the workflow open
        file_mock = Mock()
        file_mock.read.side_effect = [
            TestWorkflowSpec().serialize(JSONSerializer())]
        mock_file_open.return_value = file_mock
        response = self.app.post_json('/_ah/spi/WCApi.' + method, args)
        self.assertEqual(response.headers['content-type'], content_type)
        self.assertEqual(response.status_code, status_code)
        if content_type == "application/json":
            return json.loads(response.body)
        else:
            return response.body

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        Execution(owner=1234).put()
        Execution(owner=1234).put()
        key_to_check_is_present = Execution(owner=1234).put().urlsafe()
        key_to_check_is_not_present = Execution(owner=300).put().urlsafe()
        resp = self.api(method='execution_list', auth_required=True)
        self.assertEqual(len(resp['executions']), 3)
        self.assertNotIn(
            {'execution_id': key_to_check_is_not_present}, resp['executions'])
        self.assertIn(
            {'execution_id': key_to_check_is_present}, resp['executions'])

    def tearDown(self):
        self.testbed.deactivate()

    def test_execution_new(self):
        """ check that we can create a new execution"""
        resp = self.api(method='execution_new', auth_required=True)
        self.assertIn('inputs_required', resp)
        self.assertTrue(len(resp['inputs_required']) > 0)

    def test_get_inputs_required(self):
        """ tests json schema load"""
        execution = wc_api.get_execution_new()
        actual = wc_api.get_filtered_schema(execution)
        self.assertIn('nose', actual)
        self.assertNotEqual(len(actual), 0)

    def test_execution_delete(self):
        """ test deleting an execution """
        key = Execution(owner=1234).put().urlsafe()
        self.api(method='execution_delete',
                        auth_required=True, args={'execution_id': key})
        self.assertIsNone(ndb.Key(urlsafe=key).get())

    def test_execution_resume(self):
        """ check that we can resume an execution"""
        data = [{
            'key': 'name',
            'value': 'hi'
        }, {
            'key': 'face',
            'value': ['hi', 'there']
        }, {
            'key': 'nose',
            'value': ['hi', 'there']
        }, {
            'key': 'pets',
            'value': ['hi', 'there']
        }]
        resp = self.api(method='execution_resume',
                        auth_required=True, args={'data': data})
        print resp

    def test_service_status(self):
        """ check that we can resume an execution"""
        expected = dict(fb='1', ndb='1')
        actual = self.api(method='service_status')
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
