#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""
import unittest
import json
import pprint
import random
import string

from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from google.appengine.ext import ndb
from mock import patch

from models.Execution import Execution
from py_utils.NDBBPMNSerializer import NDBBPMNSerializer
import main
from WorkflowGenerate import BpmnHelper

from tests.BaseTestClass import BaseTestClass

pprint.PrettyPrinter(indent=2)


# noinspection PyTypeChecker
class MainTests(BaseTestClass):
    def setUp(self):
        self.setup_testbed()
        self.app = main.app
        self.app.testing = True
        self.app_client = self.app.test_client()
        self.spec = BpmnHelper().load_workflow_spec('tests/TestWorkflowSpec.bpmn', 'workflow')

    def tearDown(self):
        self.testbed.deactivate()
        try:
            del self.execution_object
            del self.execution
            del self.execution_id
        except AttributeError:
            pass

    @patch('main.get_schema')
    @patch('main.get_workflow_spec')
    @patch('py_utils.facebook_auth.get_user_id_from_request')
    def api(self, mock_get_user_id=None, workflow_mock=None, schema_mock=None, uri='', method='GET', data=None,
            status_code=200,
            content_type='application/json', user_id=None):
        """ helper to make api calls """
        global response
        workflow_mock.return_value = self.spec
        schema_mock.return_value = json.loads(open("tests/test_schema.json").read())
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
        self.assertEquals(len(resp['collection']['items']), 2)
        self.assertIn('executions', resp['collection']['items'])
        self.assertIn('queries', resp['collection']['items'])

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
            # self.assertEqual({'company': 'test', 'face' : 'test'}, item['values'])
            self.assertNotEqual(key_not_to_expect, item['execution_id'])

    def test_page_not_found(self):
        resp = self.api(uri='/notfound', status_code=404)
        self.assertEqual("Sorry, Nothing at this URL.", resp['error']['message'])

    def test_execution_new(self):
        """ check that we can create a new execution"""
        resp = self.api(uri='/executions/create', user_id=1234, status_code=302,
                        content_type='text/html; charset=utf-8', method='POST')
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

    def atest_post_execution(self):
        """ test getting an execution"""
        self._create_execution_object()
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
        redirect_resp = self.api(uri='/executions/' + self.execution_id,
                                 user_id=1234,
                                 method='POST',
                                 data=data,
                                 status_code=302,
                                 content_type='text/html; charset=utf-8')
        self.assertIn("You should be redirected automatically", redirect_resp.data)
        self.assertIn('api/executions/', redirect_resp.headers['Location'])

        resp = self.api(uri='/executions/' + self.execution_id, user_id=1234)
        self.assertIn('execution', resp)
        self.assertIn('schema', resp['execution'])
        self.assertIn('mildrid', resp['execution']['schema']['properties'])

        # self.assertIn(StoredValues(k='name', v='John Smith'), self.execution_object.values)
        # self.assertIn(StoredValues(k='pets', v=[{u'type': u'dog', u'name': u'Walter'}]), self.execution_object.values)

    def test_post_invalid_execution(self):
        """ test posting an execution with invalid input"""
        self._create_execution_object()
        data = {
            "name": "Joh",
        }
        with self.assertRaises(Exception) as ex:
            self.api(uri='/executions/' + self.execution_id,
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
        self.execution_object = Execution(owner=owner)
        self.execution = BpmnWorkflow(self.spec)
        self.execution.complete_all()
        self.execution_object.data = NDBBPMNSerializer().serialize_workflow(self.execution, include_spec=False)
        self.execution_object.variableone = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.execution_object.variabletwo = ['ff', 'bb']
        self.execution_object.variablethree = [{'ff':'aa'}, {'ff':'aa'}]
        self.execution_object.variablefour = {'ff':'aa', 'faf':'aa'}
        self.execution_id = self.execution_object.put().urlsafe()

        return self.execution_id

    def test_execution_delete(self):
        """ test deleting an execution """
        self._create_execution_object()
        self.api(uri='/executions/' + self.execution_id, user_id=1234, method='DELETE')
        self.assertEqual(None, ndb.Key(urlsafe=self.execution_id).get())

    def test_get_workflow_spec(self):
        """
        test we can load the spec without mocks
        """
        spec = main.get_workflow_spec()
        self.assertIsInstance(spec, object)

    def test_queries_companies(self):
        self._create_execution_object()
        self._create_execution_object()

        response = self.api(uri='/queries/companies')
        print response
        # for prop in self.execution_object._properties.values():
        #     if isinstance(prop, ndb.GenericProperty) or isinstance(prop, ndb.StructuredProperty):
        #         print prop._code_name
        # self.fail()



if __name__ == '__main__':
    unittest.main()  # pragma: no cover
