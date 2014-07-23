#!/usr/bin/env python
# coding=utf-8
"""This is for asserting some principals of how we use workflow so is a good resource to refer to if you're trying
to figure why things are broken"""

import unittest
import json
import os
from google.appengine.ext import testbed
from google.appengine.ext import ndb
from SpiffWorkflow.storage import DictionarySerializer
from SpiffWorkflow.Task import *

from models.Execution import Execution
from WorkflowSpecs.UserInput import UserInput
from py_utils.NDBBPMNSerializer import NDBBPMNSerializer
from py_utils.NDBSerializer import NDBSerializer
from tests.TestWorkflowSpec import TestWorkflowSpec
from SpiffWorkflow.bpmn.BpmnWorkflow import BpmnWorkflow
from SpiffWorkflow.bpmn.storage.BpmnSerializer import BpmnSerializer

from tests.PackagerForTests import PackagerForTests


class TestBPMNWorkflowFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.spec = self.load_workflow_spec('TestWorkflowSpec.bpmn', 'workflow')
        self.workflow = BpmnWorkflow(self.spec)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.spec = None
        self.workflow = None
        self.testbed.deactivate()


    def test_valid_pickle_workflow(self):
        """test the basics of the pickling serializer/deserializer on the workflow storing to ndb"""
        # data = self.workflow.serialize(CompactWorkflowSerializer())
        self.workflow.do_engine_steps()
        self.workflow.refresh_waiting_tasks()
        data = NDBBPMNSerializer().serialize_workflow(self.workflow, include_spec=False)
        urlsafe_key = Execution(owner=100, data=data).put().urlsafe()
        restored_data = ndb.Key(urlsafe=urlsafe_key).get().data
        self.assertEqual(data, restored_data)
        restored_execution = NDBBPMNSerializer().deserialize_workflow(restored_data, wf_spec=self.spec)
        self.assertEqual(restored_execution.get_tasks(
            Task.READY)[0].task_spec.name, 'task_a1')

    def test_simple_workflow_flight(self):
        """test a flight through the workflow"""
        # check we have a start
        self.assertEqual(self.workflow.get_tasks(
            Task.READY)[0].task_spec.name, 'Start')
        # move past the start
        self.workflow.do_engine_steps()
        tasks = self.workflow.get_tasks(Task.READY)
        # check we have our task named correctly and with the inputs we want in the workflow
        my_task = self.workflow.get_ready_user_tasks()[0]

        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertEqual(type(my_task.task_spec).__name__, 'UserTask')
        self.assertEqual(my_task._state, Task.READY)

        # try to move forwards
        self.workflow.do_engine_steps()

        # check we are still waiting on the input after trying to proceed
        my_task = self.workflow.get_ready_user_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a1')
        self.assertEqual(
            my_task.task_spec.args, ['name', 'face', 'nose', 'pets'])
        self.assertEqual(type(my_task.task_spec).__name__, 'UserTask')

        self.assertEqual(my_task._state, Task.READY)
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
        my_task.complete()
        self.workflow.do_engine_steps()

        # check we are still waiting on the input after trying to proceed with partial info
    #     my_task = self.workflow._get_waiting_tasks()[0]
    #     self.assertEqual(my_task.task_spec.name, 'task_a1')
    #     self.assertIsInstance(my_task.task_spec, UserInput)
    #     self.assertEqual(my_task._state, Task.WAITING)
    #
        # self.assertIsNone(my_task.set_data(**{'pets': 'ha'}))
    #     self.assertEqual(my_task.get_data('pets'), 'ha')
    #     self.workflow.complete_all()
    #
        # check that the now waiting task has moved on to the next thing in the
        # workflow
        my_task = self.workflow.get_ready_user_tasks()[0]
        self.assertEqual(my_task.task_spec.name, 'task_a2')

        self.assertEqual(type(my_task.task_spec).__name__, 'UserTask')
        self.assertEqual(my_task._state, Task.READY)

        # check that the new task has inherited the data from the previous
        self.assertEqual(my_task.get_data('nose'), 3)
        self.assertEqual(my_task.get_data('face'), 'false')
        self.assertEqual(my_task.get_data('name'), 'hello')
        # self.assertEqual(my_task.get_data('pets'), 'ha')

        # check that an exclusive choice will listen to the data given above it
        # and choose the non-default option
        self.assertEqual(
            self.workflow.get_tasks_from_spec_name('task_b1')[0]._state, Task.LIKELY)
        self.assertEqual(
            self.workflow.get_tasks_from_spec_name('task_b2')[0]._state, Task.MAYBE)
        self.assertIsNone(my_task.set_data(**{'sid': 'ha', "mildrid": "va"}))
        my_task.complete()
        self.workflow.do_engine_steps()
        self.assertEqual(self.workflow.get_tasks_from_spec_name(
            'task_b2')[0]._state, Task.COMPLETED)
        self.assertEqual(self.workflow.get_tasks_from_spec_name('task_b1'), [])

        self.assertTrue(self.workflow.is_completed())
        self.save_restore()


    def load_workflow_spec(self, filename, process_name):
        f = os.path.join(os.path.dirname(__file__), filename)

        return BpmnSerializer().deserialize_workflow_spec(
            PackagerForTests.package_in_memory(process_name, f))

    def assertTaskNotReady(self, step_name):
        tasks = list([t for t in self.workflow.get_tasks(Task.READY) if t.task_spec.name == step_name or t.task_spec.description == step_name])
        self.assertEquals([], tasks)

    def save_restore(self):
        before_dump = self.workflow.get_dump()
        state = NDBBPMNSerializer().serialize_workflow(self.workflow, include_spec=False)
        self.restore(state)
        # We should still have the same state:
        after_dump = self.workflow.get_dump()

        self.assertEquals(after_dump, before_dump)

    def restore(self, state):
        self.workflow = NDBBPMNSerializer().deserialize_workflow(state, wf_spec=self.spec)


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
