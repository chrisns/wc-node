#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""

import unittest
import json

from google.appengine.ext import testbed
from google.appengine.ext import ndb
from SpiffWorkflow import Workflow
from SpiffWorkflow.storage import JSONSerializer
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.Task import *

from models.Execution import Execution
from WorkflowSpecs.UserInput import UserInput
from py_utils.NDBSerializer import NDBSerializer
from tests.TestWorkflowSpec import TestWorkflowSpec

class TestWorkflowFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.spec = TestWorkflowSpec()
        self.workflow = Workflow(self.spec)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.spec = None
        self.workflow = None
        self.testbed.deactivate()

    def test_valid_json_spec(self):
        """test the basics of the json serializer/deserializer on the spec"""
        json_serialized_spec = self.spec.serialize(JSONSerializer())
        self.assertTrue(json.loads(json_serialized_spec))

        self.assertIn('nose', json_serialized_spec)
        self.assertIn('face', json_serialized_spec)
        self.assertIn('mildrid', json_serialized_spec)

        json_deserialized_spec = JSONSerializer().deserialize_workflow_spec(
            json_serialized_spec)
        self.assertTrue(json_deserialized_spec)

    def test_valid_json_workflow(self):
        """test the basics of the json serializer/deserializer on the workflow
            we don't do this in the real world"""
        json_serialized_wf = self.workflow.serialize(JSONSerializer())
        self.assertTrue(json.loads(json_serialized_wf))

    def test_valid_pickle_workflow(self):
        """test the basics of the pickling serializer/deserializer on the workflow storing to ndb"""
        data = self.workflow.serialize(NDBSerializer())
        urlsafe_key = Execution(owner=100, data=data).put().urlsafe()
        restored_data = ndb.Key(urlsafe=urlsafe_key).get().data
        self.assertEqual(data, restored_data)
        restored_execution = NDBSerializer().deserialize_workflow(restored_data)
        self.assertEqual(restored_execution.get_tasks(
            Task.READY)[0].task_spec.name, 'Start')
        self.fail()

    def test_simple_workflow_flight(self):
        """test a flight through the workflow"""
        # check we have a start
        self.assertEqual(self.workflow.get_tasks(
            Task.READY)[0].task_spec.name, 'Start')
        # move past the start
        self.workflow.complete_all()

        # check we have our task named correctly and with the inputs we want in
        # the workflow
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        # try to move forwards
        self.workflow.complete_all()

        # check we are still waiting on the input after trying to proceed
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertEqual(
            my_task.task_spec.args, ['name', 'face', 'nose', 'pets'])
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)
        # set some data
        dummy_data = {
            'nose': 3,
            'face': 'false',
            'name': 'hello'
        }
        self.assertIsNone(my_task.set_data(**dummy_data))
        self.assertEqual(my_task.get_data('nose'), 3)
        self.assertEqual(my_task.get_data('face'), 'false')
        self.assertEqual(my_task.get_data('name'), 'hello')

        self.workflow.complete_all()

        # check we are still waiting on the input after trying to proceed with
        # partial info
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        self.assertIsNone(my_task.set_data(**{'pets': 'ha'}))
        self.assertEqual(my_task.get_data('pets'), 'ha')
        self.workflow.complete_all()

        # check that the now waiting task has moved on to the next thing in the
        # workflow
        my_task = self.workflow._get_waiting_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a2')
        self.assertIsInstance(my_task.task_spec, UserInput)
        self.assertEqual(my_task._state, Task.WAITING)

        # check that the new task has inherited the data from the previous
        self.assertEqual(my_task.get_data('nose'), 3)
        self.assertEqual(my_task.get_data('face'), 'false')
        self.assertEqual(my_task.get_data('name'), 'hello')
        self.assertEqual(my_task.get_data('pets'), 'ha')

        # check that an exclusive choice will listen to the data given above it
        # and choose the non-default option
        self.assertEqual(
            self.workflow.get_tasks_from_spec_name('task_b1')[0]._state, Task.LIKELY)
        self.assertEqual(
            self.workflow.get_tasks_from_spec_name('task_b2')[0]._state, Task.MAYBE)
        self.assertIsNone(my_task.set_data(**{'sid': 'ha', "mildrid": "va"}))
        self.workflow.complete_all()
        self.assertEqual(self.workflow.get_tasks_from_spec_name(
            'task_b2')[0]._state, Task.COMPLETED)
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b1'), [])

        self.assertTrue(self.workflow.is_completed())


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
