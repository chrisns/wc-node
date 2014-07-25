#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""
import unittest
import json
import pprint

from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from mock import patch

from models.Execution import Execution
from py_utils.NDBBPMNSerializer import NDBBPMNSerializer
import main
from workflow import BpmnHelper


pprint.PrettyPrinter(indent=2)


# noinspection PyTypeChecker
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
        self.spec = BpmnHelper().load_workflow_spec('tests/TestWorkflowSpec.bpmn', 'workflow')

    def tearDown(self):
        self.testbed.deactivate()

    @patch('main.get_workflow_spec')
    @patch('py_utils.facebook_auth.get_user_id_from_request')
    def api(self, mock_get_user_id=None, workflow_mock=None, uri='', method='GET', data=None, status_code=200,
            content_type='application/json', user_id=None):
        """ helper to make api calls """
        global response
        workflow_mock.return_value = self.spec
        uri = "/api" + uri
        if data is None:
            data = {}

        mock_get_user_id.return_value = user_id

        if method == 'GET':
            response = self.app_client.get(uri)

        elif method == 'POST':
            response = self.app_client.post(uri, data=json.dumps(data), content_type='Content-Type: application/json')

        elif method == 'DELETE':
            response = self.app_client.delete(uri)

        self.assertEqual(response.content_type, content_type)
        self.assertEqual(response.status_code, status_code)
        if response.content_type == "application/json":
            json_obj = json.loads(response.data)
            self.assertEquals(json_obj[json_obj.keys()[0]]['version'], 1.0)
            return json_obj
        else:
            return response

    def test_root_route(self):
        """ check that we can get the api router """
        resp = self.api()
        self.assertEquals(resp.keys()[0], "collection")
        self.assertEquals(len(resp['collection']['items']), 1)
        self.assertIn('executions', resp['collection']['items'])

    def test_list_executions_requires_auth(self):
        """ check that list executions requires authentication """
        resp = self.api(uri='/executions', status_code=400)
        self.assertEqual('Authentication required', resp['error']['message'])

    def test_list_executions(self):
        """ check that we can list executions belonging to a user and no other"""
        keys_to_expect = [
            self._create_execution_object(),
            self._create_execution_object(),
            self._create_execution_object()
        ]
        key_not_to_expect = self._create_execution_object(owner=456)

        resp = self.api(uri='/executions', user_id=1234)
        # self.fail()
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
        self.assertEqual("Sorry, Nothing at this URL.", resp['error']['message'])

    def test_execution_new(self):
        """ check that we can create a new execution"""
        resp = self.api(uri='/executions/create', user_id=1234, status_code=302,
                        content_type='text/html; charset=utf-8')
        self.assertIn('You should be redirected automatically', resp.data)
        self.assertIn('api/executions/', resp.headers['Location'])

    def test_get_execution_authentication_denies(self):
        execution_id = self._create_execution_object()
        resp = self.api(uri='/executions/' + execution_id, user_id=4567, status_code=404)
        self.assertNotIn('execution', resp)
        self.assertIn('error', resp)

    def test_get_execution(self):
        """ test getting an execution"""
        execution_id = self._create_execution_object()
        resp = self.api(uri='/executions/' + execution_id, user_id=1234)
        self.assertIn('execution', resp)
        self.assertIn('schema', resp['execution'])

    def test_post_execution(self):
        """ test getting an execution"""
        execution_id = self._create_execution_object()
        data = {
            "name": "John Smith",
            "face": "Jude Smith",
            "nose": "mr",
            "pets": [
                {
                    "type": "dog",
                    "name": "Walter"
                }
            ]
        }
        redirect_resp = self.api(uri='/executions/' + execution_id,
                                 user_id=1234,
                                 method='POST',
                                 data=data,
                                 status_code=302,
                                 content_type='text/html; charset=utf-8')
        self.assertIn('You should be redirected automatically', redirect_resp.data)
        self.assertIn('api/executions/', redirect_resp.headers['Location'])

        resp = self.api(uri='/executions/' + execution_id, user_id=1234)
        self.assertIn('execution', resp)
        self.assertIn('schema', resp['execution'])
        self.assertIn('mildrid', resp['execution']['schema']['properties'])

    def test_post_invalid_execution(self):
        """ test posting an execution with invalid input"""
        execution_id = self._create_execution_object()
        data = {
            "name": "Joh",
        }
        with self.assertRaises(Exception) as ex:
            self.api(uri='/executions/' + execution_id,
                     user_id=1234,
                     method='POST',
                     data=data,
                     status_code=302,
                     content_type='text/html; charset=utf-8')
        self.assertEqual('schema/input mismatch', ex.exception.message)

    def _create_execution_object(self, owner=1234):
        """
        Helper to make a valid execution object and return the execution_id
        """
        execution_object = Execution(owner=owner)
        execution = BpmnWorkflow(self.spec)
        execution.complete_all()
        execution_object.data = NDBBPMNSerializer().serialize_workflow(execution, include_spec=False)
        execution_id = execution_object.put().urlsafe()
        return execution_id

    def test_execution_delete(self):
        """ test deleting an execution """
        execution_id = Execution(owner=1234).put().urlsafe()
        self.api(uri='/executions/' + execution_id, user_id=1234, method='DELETE')
        self.assertEqual(None, ndb.Key(urlsafe=execution_id).get())


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
